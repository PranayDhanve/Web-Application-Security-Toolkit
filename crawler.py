import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_urls = set()

def get_links(base_url):
    """Crawl a website and return all internal links"""
    to_visit = [base_url]
    internal_links = set()

    while to_visit:
        url = to_visit.pop()
        if url in visited_urls:
            continue
        
        visited_urls.add(url)
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            
            for link in soup.find_all("a", href=True):
                full_url = urljoin(base_url, link["href"])
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    if full_url not in visited_urls:
                        internal_links.add(full_url)
                        to_visit.append(full_url)
        except requests.exceptions.RequestException:
            continue
    
    return internal_links
