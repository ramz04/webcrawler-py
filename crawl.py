from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as soup, Tag # pyright: ignore[reportMissingImports]
import sys
import requests


def normalize_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path.rstrip('/')

def get_heading_from_html(html: str) -> str:
    parsed = soup(html, 'html.parser')
    for tag in ['h1', 'h2']:
        if h_tag := parsed.find(tag):
            return h_tag.get_text(strip=True)
    return ""

def get_first_paragraph_from_html(html: str) -> str:
    parsed = soup(html, 'html.parser')
    if main := parsed.find('main'):
        if p_tag := main.find('p'):
            return p_tag.get_text(strip=True)
    return ""

def get_urls_from_html(html, base_url):
    parsed = soup(html, 'html.parser')
    if a_tags:= parsed.find_all('a'):
        urls = [urljoin(base_url, a.get('href')) for a in a_tags if a.get('href')]
        return urls
    return []

def get_images_from_html(html, base_url):
    parsed = soup(html, 'html.parser')
    if img_tags:= parsed.find_all('img'):
        urls = [urljoin(base_url, img.get('src')) for img in img_tags if img.get('src')]
        return urls
    return []

def extract_page_data(html: str, page_url:str):
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }

def command_line_arguments():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"starting crawl of: {sys.argv[1]}")

def get_html(url):
    url_request = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if url_request.status_code != 200:
        print(f"error fetching {url}: status code {url_request.status_code}")
        return None
    elif not url_request.headers.get('content-type', "").startswith("text/html"):
        print(f"error fetching {url}: content type {url_request.headers.get('Content-Type')} is not text/html")
        return None 
    else:
        return url_request.text