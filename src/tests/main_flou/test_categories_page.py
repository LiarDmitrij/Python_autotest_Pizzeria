import allure
from selenium.webdriver.common.by import By

from src.utils.text import clean
from src.utils.waits import (
    wait_all_visible,
    wait_clickable,
    wait_present,
    wait_visible,
)

DESSERTS_URL = ('https://pizzeria.skillbox.cc/product-category/menu/deserts/')
DESSERTS_PRODUCT = (By.CSS_SELECTOR, 'li.product.product_cat-deserts')
DESSERTS_PRODUCT_FIRST = (By.CSS_SELECTOR, 'li.product.product_cat-deserts.first')
PRICE_SLIDER_MAX_INPUT = (By.CSS_SELECTOR, 'input#max_price')
PRICE_APPLY_BUTTON = (By.CSS_SELECTOR, '.price_slider_wrapper button[type="submit"]')
PRODUCT_PRICE = (By.CSS_SELECTOR, 'li.product .price .amount')

ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 'li.product.first .add_to_cart_button')
CART_LINK = (By.CSS_SELECTOR, 'a.cart-contents')
CART_ITEM = (By.CSS_SELECTOR, '.cart_item td.product-name')
ADDED_TO_CART = (By.CSS_SELECTOR, 'a.added_to_cart')
CART_TABLE = (By.CSS_SELECTOR, 'table.shop_table.cart')

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

    @allure.story("Меню")
    @allure.title("TC-14: Добавление десерта в корзину")
    def test_add_dessert_to_cart(self, selenium, go_to_url):
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

        with allure.step("Запомнить название первого десерта"):
            first_product = wait_visible(selenium, DESSERTS_PRODUCT_FIRST)
            dessert_name = first_product.find_element(By.CSS_SELECTOR, 'h3').text.strip()

        with allure.step("Добавить первый десерт в корзину"):
            add_button = first_product.find_element(*ADD_TO_CART_BUTTON)
            add_button.click()

        with allure.step("Дождаться подтверждения добавления"):
            wait_all_visible(selenium, ADDED_TO_CART)

        with allure.step("Перейти в корзину"):
            cart_link = wait_visible(selenium, CART_LINK)
            cart_link.click()

        with allure.step("Проверить, что в корзине одна позиция"):
            wait_visible(selenium, CART_TABLE)
            cart_items = selenium.find_elements(*CART_ITEM)
            assert len(cart_items) == 1, \
                f"В корзине {len(cart_items)} позиций, ожидалась 1"

        with allure.step("Проверить, что в корзине нужный десерт"):
            cart_name = cart_items[0].find_element(
                By.CSS_SELECTOR, 'a'
            ).text.strip()
            assert clean(cart_name) == clean(dessert_name), \
                f"В корзине «{cart_name}», ожидался «{dessert_name}»"