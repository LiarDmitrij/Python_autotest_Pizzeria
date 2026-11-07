import allure
import pytest


@pytest.fixture
def go_to_url(selenium):
    @allure.step('Откртие страницы {url}')
    def callback(url):
        selenium.get(url)
    return callback