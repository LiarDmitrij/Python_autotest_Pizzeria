import allure
import pytest


@pytest.fixture
def go_to_url(selenium):
    @allure.step('Открытие страницы {url}')
    def callback(url):
        selenium.get(url)
    return callback