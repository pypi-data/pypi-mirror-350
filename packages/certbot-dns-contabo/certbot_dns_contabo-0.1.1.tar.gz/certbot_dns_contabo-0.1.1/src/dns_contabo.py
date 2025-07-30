import logging
import requests
from bs4 import BeautifulSoup
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

CONTABO_BASE_URL = "https://my.contabo.com"
LOGIN_URL = CONTABO_BASE_URL + "/account/login"
DNS_MANAGEMENT_URL_BASE = CONTABO_BASE_URL + "/dns"


class Authenticator(dns_common.DNSAuthenticator):
    """
    DNS Authenticator for Contabo.
    This plugin automates DNS-01 challenges for Contabo by scraping the Contabo web interface,
    as no official API is available.
    """

    description = "Authenticator for Contabo DNS via web scraping."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials = None
        self.s = requests.Session()  # session for cookie persistence
        self.has_logged_in = False  # flag to check if we ever logged in during this session
        self.management_urls = {}  # cache for management URLs to avoid repeated lookups

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds=60):
        super().add_parser_arguments(add, default_propagation_seconds=default_propagation_seconds)
        add("credentials", help="Contabo credentials INI file")

    def more_info(self):
        return (
            "This plugin configures a DNS TXT record to respond to a DNS-01 challenge using "
            "the Contabo web interface. Since this plugin relies on web scraping, "
            "it may break if Contabo changes its website structure (which is unlikely, as they "
            "use the same outdated design for years). "
        )

    def _setup_credentials(self):
        # load credentials
        self.credentials = self._configure_credentials(
            "credentials",
            "Contabo credentials INI file",
            {
                "email": "Contabo account email",
                "password": "Contabo account password",
            },
        )
        logger.debug("Credentials configured.")
        self._login()
        self._fetch_domains()

    def _perform(self, domain, validation_name, validation):
        """
        Logs in to Contabo, finds the DNS management URL for the domain,
        and creates the necessary TXT record.
        """
        if not self._is_logged_in():
            self._login()
        self._create_record(domain, validation_name, validation)
        logger.info("DNS records for %s set successfully.", domain)

    def _cleanup(self, domain, validation_name, validation):
        """
        Logs in to Contabo (if session expired or first time), finds the DNS management URL,
        and removes the TXT record created in _perform.
        """

        if not self._is_logged_in():
            self._login()
            self._fetch_domains()

        management_url = self._get_management_url(domain)
        dns_req = self.s.get(management_url, allow_redirects=False)

        if dns_req.status_code != 200:
            logger.error("Failed to access the DNS management page (%s) for cleanup. Status: %s",
                         management_url, dns_req.status_code)
            raise ValueError(
                "Failed to access the DNS management page for cleanup. Please double check that you've added the"
                " domain to Contabo, else report this issue at "
                "https://github.com/DAMcraft/certbot-dns-contabo"
            )
        logger.debug("DNS management page content fetched for cleanup.")
        dns_soup = BeautifulSoup(dns_req.content, "html.parser")
        page_content = dns_soup.find("div", {"id": "content"})
        if not page_content:
            logger.error("Could not find main content div on DNS management page during cleanup.")
            return

        table = page_content.find("table")
        if not table:
            logger.error("Could not find DNS records table on management page during cleanup.")
            return

        # find the specific TXT record row by its content (validation string)
        td_validation = table.find("td", {"class": "dnsdata"}, string=validation)
        if not td_validation:
            logger.warning("Could not find the validation string '%s' in any TXT record. "
                           "Record may have already been deleted.", validation)
            return

        logger.debug("Found td with validation string %s", validation)
        # the delete form is expected in the next td
        td_delete_form_container = td_validation.find_next_sibling("td")

        delete_form = td_delete_form_container.find("form", {"class": "deleteform"})
        if not delete_form:
            logger.error("Failed to find the delete form for the DNS record: %s. It might have already been deleted.",
                         validation_name)
            return
        logger.debug("Delete form found")

        token_key_input = delete_form.find("input", {"name": "data[_Token][key]"})
        token_fields_input = delete_form.find("input", {"name": "data[_Token][fields]"})

        if not token_key_input or not token_fields_input:
            logger.error("Failed to find CSRF token fields in the delete form")
            return

        token_key = token_key_input.get("value")
        token_fields = token_fields_input.get("value")

        if not token_key or not token_fields:
            logger.error("CSRF token values are empty in the delete form")
            return

        logger.debug("Extracted delete CSRF tokens: key=%s, fields=%s", token_key, token_fields)

        delete_payload = {
            'data[_Token][fields]': token_fields,
            'data[_Token][key]': token_key,
            'data[_Token][unlocked]': '',
            'data[ResourceRecordDelete][name]': validation_name,
            'data[ResourceRecordDelete][type]': 'TXT',
            'data[ResourceRecordDelete][data]': validation,
        }
        delete_url = management_url + "/deleterr"
        logger.info("Deleting the DNS record for %s", domain)

        req = self.s.post(
            delete_url,
            data=delete_payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=False,
        )

        if req.status_code == 302:  # successful deletion redirects
            logger.info("Cleanup process for %s completed.", domain)
        else:
            logger.error("Failed to clean up DNS records for %s.", domain)

    def _login(self):
        logger.info("Attempting to log in to Contabo")
        try:
            login_page_req = self.s.get(LOGIN_URL)
            login_page_req.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch Contabo login page: %s", e)
            raise ValueError("Connection error while fetching Contabo login page. Details: %s" % e)

        logger.debug("Login page fetched successfully. Status: %s", login_page_req.status_code)

        login_soup = BeautifulSoup(login_page_req.content, "html.parser")

        # extract CSRF tokens
        token_key_input = login_soup.find("input", {"name": "data[_Token][key]"})
        token_fields_input = login_soup.find("input", {"name": "data[_Token][fields]"})
        token_unlocked_input = login_soup.find("input", {"name": "data[_Token][unlocked]"})

        if not (token_key_input and token_fields_input and token_unlocked_input):
            raise ValueError(
                "Failed to extract CSRF token input fields from the login page. "
                "Contabo's login page structure might have changed. "
                "Please report this issue at https://github.com/DAMcraft/certbot-dns-contabo"
            )

        token_key = token_key_input.get("value")
        token_fields = token_fields_input.get("value")
        token_unlocked = token_unlocked_input.get("value")

        if not token_key or not token_fields:
            logger.error("CSRF tokens are missing from login page inputs.")
            raise ValueError(
                "Failed to extract CSRF token values from the login page. "
                "Contabo's login page structure might have changed. "
                "Please report this issue at https://github.com/DAMcraft/certbot-dns-contabo"
            )

        logger.debug("Extracted CSRF tokens: key=%s, fields=%s, unlocked=%s", token_key, token_fields, token_unlocked)

        login_payload = {
            'data[Account][username]': self.credentials.conf('email'),
            'data[Account][password]': self.credentials.conf('password'),
            'data[_Token][fields]': token_fields,
            'data[_Token][key]': token_key,
            'data[_Token][unlocked]': token_unlocked
        }
        logger.info("Logging in...")

        try:
            login_post_req = self.s.post(
                LOGIN_URL,
                data=login_payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                allow_redirects=False
            )
        except requests.exceptions.RequestException as e:
            logger.error("Error during login POST request: %s", e)
            raise ValueError("Connection error during login attempt. Details: %s" % e)

        if login_post_req.status_code != 302:
            logger.error("Login failed. Expected status 302, got %s. Check credentials.", login_post_req.status_code)
            raise ValueError("Login failed. Please check your credentials.")

        redirect_location = login_post_req.headers.get("Location")
        expected_redirect = CONTABO_BASE_URL + "/"
        if redirect_location != expected_redirect:
            logger.error("Login redirection incorrect. Expected '%s', got '%s'. "
                         "Credentials might be wrong or login flow changed.", expected_redirect, redirect_location)
            raise ValueError(
                "There was an error during login (unexpected redirect location: %s). Please check your credentials. "
                "If they are correct, the login flow might have changed. "
                "Please report this issue at https://github.com/DAMcraft/certbot-dns-contabo" % redirect_location
            )
        self.has_logged_in = True
        logger.info("Login successful.")

    def _is_logged_in(self):
        """
        Checks if the session is still logged in by fetching the main page.
        """
        if not self.has_logged_in:
            return False

        try:
            main_page_req = self.s.get(CONTABO_BASE_URL)
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch main page to check login status: %s", e)
            return False

        if main_page_req.status_code != 200:
            logger.warning("Main page returned status %s, assuming not logged in.", main_page_req.status_code)
            return False

        return True

    def _fetch_domains(self):
        """
        Navigates to the main DNS management page and finds the URLs
        for managing a given domain.
        """
        logger.info("Fetching DNS overview page")
        try:
            dns_overview_req = self.s.get(DNS_MANAGEMENT_URL_BASE, allow_redirects=False)
            dns_overview_req.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch DNS overview page: %s", e)
            raise ValueError("Connection error while fetching DNS overview page. Details: %s" % e)

        if dns_overview_req.status_code != 200:
            logger.error("Failed to access the DNS overview page. Status: %s. Expected 200.",
                         dns_overview_req.status_code)
            raise ValueError(
                "Failed to access the DNS overview page. Ensure you are logged in and have DNS zones. "
                "If the issue persists, please report it at https://github.com/DAMcraft/certbot-dns-contabo"
            )

        logger.debug("DNS overview page fetched successfully.")
        soup = BeautifulSoup(dns_overview_req.content, "html.parser")
        page_content = soup.find("div", {"id": "content"})
        if not page_content:
            logger.error("Could not find main content div ('id=content') on DNS overview page.")
            raise ValueError("DNS overview page structure seems to have changed (missing content div)."
                             " Please report this issue.")

        table = page_content.find("table")
        if not table:
            logger.error("Could not find the domain list table on the DNS overview page.")
            raise ValueError("DNS overview page structure seems to have changed (missing domain table). "
                             "Please report this issue.")

        rows = table.find_all("tr")
        if len(rows) <= 1:  # only header or no rows
            logger.error("No domains found in the DNS overview table.")
            raise ValueError("No domains found in your Contabo account's DNS list. "
                             "Please ensure you have added domains to your Contabo account. "
                             "Otherwise, please report this issue.")

        logger.debug("Found %s rows in the domain table", len(rows))

        # iterate through rows, skip header row
        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) < 2:  # ensure there are enough cells
                continue

            # domain is in the second cell
            domain_name_cell = cells[1]
            domain_name_text = domain_name_cell.get_text(strip=True)
            link_tag = row.find("a", {"class": "updatezone"})
            relative_link = link_tag.get("href")
            management_url = CONTABO_BASE_URL + relative_link
            self.management_urls[domain_name_text] = management_url

    def _get_management_url(self, domain):
        for d, url in self.management_urls.items():
            if domain == d or domain.endswith("." + d):
                return url
        raise ValueError(
            "Could not find a zone for %s in your Contabo account." % domain
        )

    def _create_record(self, domain, validation_name, validation):
        """
        Fetches the specific DNS zone management page and creates the TXT record.
        """
        management_url = self._get_management_url(domain)

        logger.debug("Fetching DNS zone management page to create record: %s", management_url)
        try:
            dns_zone_page_req = self.s.get(management_url, allow_redirects=False)
            dns_zone_page_req.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch DNS zone page (%s): %s", management_url, e)
            raise ValueError(
                "Connection error while fetching DNS zone page '%s'. Details: %s" % (management_url, e))

        if dns_zone_page_req.status_code != 200:
            logger.error("Failed to access the DNS zone page %s. Status: %s", management_url,
                         dns_zone_page_req.status_code)
            raise ValueError(
                "Failed to access the DNS zone management page (%s). Ensure domain is added and accessible. "
                "If issue persists, report at https://github.com/DAMcraft/certbot-dns-contabo" % management_url
            )
        logger.debug("DNS zone page fetched successfully.")
        dns_soup = BeautifulSoup(dns_zone_page_req.content, "html.parser")
        page_content = dns_soup.find("div", {"id": "content"})
        if not page_content:
            logger.error("Could not find main content div on DNS zone page.")
            raise ValueError(
                "DNS zone page structure seems to have changed. Please report this issue."
            )

        form_data = page_content.find("form", {"id": "ResourceRecordViewForm"})  # form for adding new records
        if not form_data:
            logger.error("Could not find the DNS record creation form.")
            raise ValueError("DNS zone page structure changed (missing record creation form). Report this issue.")

        token_key_input = form_data.find("input", {"name": "data[_Token][key]"})
        if not token_key_input:
            logger.error("Could not find CSRF key input in the record creation form.")
            raise ValueError("CSRF key missing in DNS form. Report this issue.")
        token_key = token_key_input.get("value")

        form_footer_token_input = None
        form_footer_div = page_content.find("div", {"class": "formfooter"})
        if form_footer_div:
            form_footer_token_input = form_footer_div.find("input", {"name": "data[_Token][fields]"})

        if not form_footer_token_input:
            logger.error(
                "Could not find CSRF 'fields' input on the DNS zone page.")
            raise ValueError("CSRF 'fields' token missing on DNS form. Report this issue.")
        token_fields = form_footer_token_input.get("value")

        if not token_key or not token_fields:
            logger.error("CSRF token values for record creation are empty.")
            raise ValueError("CSRF token values missing from DNS form. Report this issue.")

        logger.debug("Extracted CSRF tokens for record creation: key=%s, fields=%s", token_key, token_fields)
        logger.info("Setting DNS record for %s", domain)

        # prepare payload for creating the TXT record
        dns_payload = {
            'data[ResourceRecord][name]': validation_name,
            'data[ResourceRecord][data]': validation,
            'data[ResourceRecord][type]': 'TXT',
            'data[ResourceRecord][ttl]': 14400,
            'data[ResourceRecord][prio]': '0',
            'data[ResourceRecord][weight]': '',
            'data[ResourceRecord][port]': '',
            'data[ResourceRecord][flag]': '0',
            'data[ResourceRecord][tag]': 'issue',
            'data[_Token][fields]': token_fields,
            'data[_Token][key]': token_key,
            'data[_Token][unlocked]': ''
        }
        create_url = management_url + "/createrr"

        try:
            create_req = self.s.post(
                create_url,
                data=dns_payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                allow_redirects=False,
            )
        except requests.exceptions.RequestException as e:
            logger.error("Error during DNS record creation POST request to %s: %s", create_url, e)
            raise ValueError("Connection error while creating DNS record. Details: %s" % e)

        if create_req.status_code != 302:
            logger.error(
                "Failed to create DNS record for %s. Contabo responded with status %s.",
                validation_name, create_req.status_code
            )

            raise ValueError(
                "Failed to create DNS TXT record for %s. Contabo server responded with status %s. "
                "If the issue persists, please report it at https://github.com/DAMcraft/certbot-dns-contabo" %
                (validation_name, create_req.status_code)
            )

