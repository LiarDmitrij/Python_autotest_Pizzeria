from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestSeleniumDefault:
    def test_open_site(self, go_to_url, selenium):
        go_to_url("https://example.com")
        assert "Example Domain" in selenium.title