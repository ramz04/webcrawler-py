import sys
from crawl import get_html, command_line_arguments


def main():
    command_line_arguments()
    print(get_html(sys.argv[1]))


if __name__ == "__main__":
    main()
