import unittest
from crawl import get_first_paragraph_from_html, get_images_from_html, get_urls_from_html, normalize_url, get_heading_from_html

class TestCrawl(unittest.TestCase):
    def test_normalize_url_https(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected_url = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected_url)
    
    def test_normalize_url_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected_url = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected_url)
    
    def test_normalize_url_https_with_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected_url = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected_url)
    
    def test_normalize_url_http_with_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected_url = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected_url)

    def test_get_heading_from_html_h1(self):
        html = "<html><body><h1>Test Heading</h1></body></html>"
        actual = get_heading_from_html(html)
        expected = "Test Heading"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_h2(self):
        html = "<html><body><h2>Test Heading</h2></body></html>"
        actual = get_heading_from_html(html)
        expected = "Test Heading"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html(self):
        html = "<html><body><p>Test Paragraph</p> <main><p>Inside main paragraph</p></main></body></html>"
        actual = get_first_paragraph_from_html(html)
        expected = "Inside main paragraph"
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Crawler Logo" /></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about">About</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/images/hero.png" alt="Hero" /></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/images/hero.png"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about">About</a><a href="/blog">Blog</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about", "https://crawler-test.com/blog"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo" /><img src="/banner.png" alt="Banner" /></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/banner.png"]
        self.assertEqual(actual, expected)
if __name__ == '__main__':
    unittest.main()