import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.waits import (
    wait_all_visible,
    wait_clickable,
    wait_present,
    wait_visible,
    wait_staleness_of
)

DESSERTS_URL = ('https://pizzeria.skillbox.cc/product-category/menu/deserts/')
DESSERTS_PRODUCT = (
    By.CSS_SELECTOR,
    'li.product.product_cat-deserts',
)
PRICE_SLIDER_MAX_INPUT = (By.CSS_SELECTOR, 'input#max_price')
PRICE_APPLY_BUTTON = (
    By.CSS_SELECTOR,
    '.price_slider_wrapper button[type="submit"]',
)
PRODUCT_PRICE = (By.CSS_SELECTOR, 'li.product .price .amount')

@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestCategoriesPage:

    @allure.story("Меню")
    @allure.title("TC-13: Фильтрация десертов по бюджету до 135 руб.")
    def test_filter_by_price(self, selenium, go_to_url):
        selenium.maximize_window()

        with allure.step("Открыть страницу раздела «Десерты»"):
            go_to_url(DESSERTS_URL)

        with allure.step("Дождаться загрузки списка десертов"):
            wait_all_visible(selenium, DESSERTS_PRODUCT)

        with allure.step("Задать максимальную цену 135 руб."):
            max_input = wait_present(selenium, PRICE_SLIDER_MAX_INPUT)
            selenium.execute_script(
                "arguments[0].value = '135';"
                "arguments[0].dispatchEvent(new Event('change'));",
                max_input,
            )

        with allure.step("Нажать кнопку «Применить»"):
            wait_clickable(selenium, PRICE_APPLY_BUTTON).click()

        with allure.step("Дождаться обновления списка десертов"):
            wait_all_visible(selenium, DESSERTS_PRODUCT)

        with allure.step("Проверить, что все десерты стоят не дороже 135 руб."):
            wait_all_visible(selenium, DESSERTS_PRODUCT)
            products_after = selenium.find_elements(*DESSERTS_PRODUCT)
            for product in products_after:
                price_text = product.find_element(
                    *PRODUCT_PRICE
                ).text.strip()
                price_value = float(
                    price_text.replace("₽", "")
                    .replace(",", ".")
                    .replace("\u00a0", "")
                    .strip()
                )
                assert price_value <= 135, \
                    f"Десерт «{price_text}» дороже 135 руб."