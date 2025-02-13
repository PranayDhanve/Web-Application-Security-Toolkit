from crawler import get_links
from form_scanner import scan_forms

def main(target_url):
    """Run the web scanner on a given URL"""
    report_data = "=== Web Security Scan Report ===\n\n"
    
    print(f"Crawling {target_url} for internal links...")
    urls = get_links(target_url)

    for url in urls:
        print(f"Scanning: {url}")
        report_data += scan_forms(url)

    with open("report.txt", "w") as file:
        file.write(report_data)

    print("\nScan complete! Check report.txt for results.")

if __name__ == "__main__":
    target = input("Enter target URL: ")
    main(target)
