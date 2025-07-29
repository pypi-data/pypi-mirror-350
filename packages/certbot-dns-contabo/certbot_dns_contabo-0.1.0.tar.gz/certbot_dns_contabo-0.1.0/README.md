# Certbot Contabo authenticator plugin

This is a Certbot plugin to automate DNS-01 challenges for domains whose DNS is managed by Contabo. It works by
interacting with the Contabo web interface through web scraping, as Contabo does not currently offer an official API for
DNS management.

---

## Important

* **Web Scraping**: This plugin relies on web scraping Contabo's website. If Contabo changes its
  website structure, this plugin may break until it's updated. The plugin is designed based on their current
  interface, which has been relatively stable for years.
* **NO 2FA SUPPORT**: This plugin does not support Contabo accounts with Two-Factor Authentication (2FA) enabled.
  You must use an account without 2FA for this plugin to work. Attempting to use it with a 2FA-enabled account will
  result in login failure (Might be supported in the future, but currently not available).

---

## Installation

You can install the plugin using pip:

```bash
pip install certbot-dns-contabo
```

## Usage

Create a credentials file like this, for example using `nano /etc/letsencrypt/contabo.ini`:

```ini
dns_contabo_email = your-contabo-email@example.com
dns_contabo_password = your-contabo-password
```

Since this file contains sensitive credentials, protect it by restricting its permissions:

```bash
sudo chmod 600  /etc/letsencrypt/contabo.ini
```

(Replace `/etc/letsencrypt/contabo.ini` if you saved it in a different location.)

To request a certificate, use Certbot with the `dns-contabo` authenticator.

**Example for `example.com` and `*.example.com` (wildcard):**

```bash
sudo certbot certonly \
  --authenticator dns-contabo \
  --dns-contabo-credentials /etc/letsencrypt/contabo.ini \
  -d example.com \
  -d "*.example.com" 
```

## Disclaimer
I am not affiliated with Contabo in any way. This plugin can stop working at any time if Contabo changes their website,
which *could* even lead to stuff breaking on your Contabo account. 
```