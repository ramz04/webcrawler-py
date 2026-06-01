import unittest
from crawl import get_first_paragraph_from_html, normalize_url, get_heading_from_html

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

if __name__ == '__main__':
    unittest.main()