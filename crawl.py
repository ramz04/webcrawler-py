from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as soup, Tag


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