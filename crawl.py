import asyncio
import sys
from urllib.parse import urljoin, urlparse
import json

import aiohttp  # pyright: ignore[reportMissingImports]
from bs4 import BeautifulSoup as soup  # pyright: ignore[reportMissingImports]


def normalize_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path.rstrip("/")


def get_heading_from_html(html: str) -> str:
    parsed = soup(html, "html.parser")
    for tag in ["h1", "h2"]:
        if h_tag := parsed.find(tag):
            return h_tag.get_text(strip=True)
    return ""


def get_first_paragraph_from_html(html: str) -> str:
    parsed = soup(html, "html.parser")
    if main := parsed.find("main"):
        if p_tag := main.find("p"):
            return p_tag.get_text(strip=True)
    return ""


def get_urls_from_html(html, base_url):
    parsed = soup(html, "html.parser")
    if a_tags := parsed.find_all("a"):
        urls = [urljoin(base_url, a.get("href")) for a in a_tags if a.get("href")]
        return urls
    return []


def get_images_from_html(html, base_url):
    parsed = soup(html, "html.parser")
    if img_tags := parsed.find_all("img"):
        urls = [urljoin(base_url, img.get("src")) for img in img_tags if img.get("src")]
        return urls
    return []


def extract_page_data(html: str, page_url: str):
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


def command_line_arguments():
    if len(sys.argv) < 4:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"starting crawl of: {sys.argv[1]}")


# def get_html(url):
# url_request = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
# if url_request.status_code != 200:
#     print(f"error fetching {url}: status code {url_request.status_code}")
#     return None
# elif not url_request.headers.get('content-type', "").startswith("text/html"):
#     print(f"error fetching {url}: content type {url_request.headers.get('Content-Type')} is not text/html")
#     return None
# else:
#     return url_request.text

# def crawl_page(base_url, current_url=None, page_data=None):
#     if current_url is None:
#         current_url = base_url
#     if page_data is None:
#         page_data = {}
#     html = get_html(current_url)
#     normalized = normalize_url(current_url)
#     print(f"Crawling: {current_url}")
#     if html and normalized not in page_data and urlparse(current_url).netloc == urlparse(base_url).netloc:
#         page_data[normalized] = extract_page_data(html, current_url)
#         for url in get_urls_from_html(html, current_url):
#             crawl_page(base_url, url, page_data)
#         return page_data


class AsyncCrawler:
    def __init__(
        self,
        base_url,
        base_domain,
        page_data,
        lock,
        max_concurrency,
        semaphore,
        session,
        max_pages,
        should_stop,
        all_tasks,
    ):
        self.base_url = base_url
        self.base_domain = base_domain
        self.page_data = page_data
        self.lock = lock
        self.max_concurrency = max_concurrency
        self.semaphore = semaphore
        self.session = session
        self.max_pages = max_pages
        self.should_stop = should_stop
        self.all_tasks = all_tasks

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        if self.should_stop:
            return False
        if len(self.page_data) == self.max_pages:
            self.should_stop = True
            print("Reached maximum number of pages to crawl.")
            for task in self.all_tasks:
                task.cancel()
            return False
        async with self.lock:
            if normalized_url not in self.page_data:
                return True
            return False

    async def get_html(self, url):
        async with self.session.get(
            url, headers={"User-Agent": "BootCrawler/1.0"}
        ) as res:
            if res.status != 200:
                print(f"error fetching {url}: status code {res.status}")
                return None
            elif not res.headers.get("content-type", "").startswith("text/html"):
                print(
                    f"error fetching {url}: content type {res.headers.get('Content-Type')} is not text/html"
                )
                return None
            else:
                return await res.text()

    async def crawl_page(self, base_url, current_url=None):
        if current_url is None:
            current_url = base_url

        if self.should_stop:
            return

        if not await self.add_page_visit(current_url):
            return

        async with self.semaphore:
            html = await self.get_html(current_url)

        if html:
            normalized = normalize_url(current_url)
            print(f"Crawling: {current_url}")
            if (
                normalized not in self.page_data
                and urlparse(current_url).netloc == urlparse(base_url).netloc
            ):
                async with self.lock:
                    self.page_data[normalized] = extract_page_data(html, current_url)
                tasks = []
                try:
                    for url in get_urls_from_html(html, current_url):
                        tasks.append(
                            asyncio.create_task(self.crawl_page(base_url, url))
                        )
                        self.all_tasks.add(tasks[-1])
                    await asyncio.gather(*tasks, return_exceptions=True)
                finally:
                    for task in tasks:
                        self.all_tasks.remove(task)

    async def crawl(self, base_url):
        await self.crawl_page(base_url)
        return self.page_data


async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(
        base_url,
        urlparse(base_url).netloc,
        {},
        asyncio.Lock(),
        max_concurrency,
        asyncio.Semaphore(max_concurrency),
        None,
        max_pages,
        False,
        set(),
    ) as crawler:
        final_page_data = await crawler.crawl(base_url)
        return final_page_data

def write_json_report(page_data, filename="report.json"):
    pages = sorted(page_data.values(), key=lambda x: x["url"])
    with open(filename, "w") as f:
        json.dump(pages, f, indent=2)
