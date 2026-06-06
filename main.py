import asyncio
import os
import sys

from crawl import command_line_arguments, crawl_site_async, write_json_report
from notify import send_email_report
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from visualise import build_graph, save_graph_image

load_dotenv()

URL = os.getenv("CRAWL_URL", "https://crawler-test.com/")
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "3"))
MAX_PAGES = int(os.getenv("MAX_PAGES", "25"))
MAX_DEPTH = int(os.getenv("MAX_DEPTH", "20"))


async def main_async():
    res = {}
    try:
        res = await crawl_site_async(URL, MAX_CONCURRENCY, MAX_PAGES, MAX_DEPTH)
        write_json_report(res, base_url=URL)
        # send_email_report(os.getenv("RECIPIENT_EMAIL"), "report.json")
        graph = build_graph(res, URL)
        save_graph_image(graph, base_url=URL)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down — writing partial report...")
        if res:
            write_json_report(res, base_url=URL, filename="report_partial.json")
            print(f"Partial report saved: {len(res)} pages crawled.")
        sys.exit(0)
    except Exception as e:
        print(f"Crawl failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main_async())
