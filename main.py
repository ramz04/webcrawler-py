import sys
from crawl import get_html, command_line_arguments, crawl_page


def main():
    command_line_arguments()
    # print(get_html(sys.argv[1]))
    crawl_page(sys.argv[1])



if __name__ == "__main__":
    main()
