import asyncio
import os
import sys

from crawl import command_line_arguments, crawl_site_async, write_json_report
from notify import send_email_report
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

# def main():
#     command_line_arguments()
#     print(get_html(sys.argv[1]))
#     crawl_page(sys.argv[1])

async def main_async():
    command_line_arguments()
    res = await crawl_site_async(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    write_json_report(res, base_url=sys.argv[1])
    send_email_report(os.getenv("RECIPIENT_EMAIL"), "report.json")

    # print(res.values())
    # for data in res.values():
    #     print(data)


if __name__ == "__main__":
    asyncio.run(main_async())
