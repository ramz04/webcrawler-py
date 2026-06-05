import asyncio
import logging
import os
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]

from crawl import crawl_site_async, write_json_report
from notify import send_email_report

load_dotenv()

logging.basicConfig(
    filename="crawler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

URL = os.getenv("CRAWL_URL", "https://crawler-test.com/")
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "3"))
MAX_PAGES = int(os.getenv("MAX_PAGES", "25"))
RECIPIENT = os.environ["RECIPIENT_EMAIL"]
MAX_DEPTH = int(os.getenv("MAX_DEPTH", "20"))


async def run_crawl():
    start = datetime.now()
    logging.info(f"Crawl started — {URL}")
    print(f"[{start}] Starting crawl of {URL}")

    try:
        page_data = await crawl_site_async(URL, MAX_CONCURRENCY, MAX_PAGES, MAX_DEPTH)
        write_json_report(page_data, base_url=URL)

        logging.info(f"Crawl complete — {len(page_data)} pages crawled")
        print(f"Crawled {len(page_data)} pages. Sending email report...")

        send_email_report(RECIPIENT, "report.json")
    except Exception as e:
        logging.error(f"Crawl failed: {e}")
        print(f"Crawl failed: {e}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_crawl, "interval", minutes=5)
    scheduler.start()

    print("Scheduler started. Running first crawl now...")
    await run_crawl()

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
