import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from src.utils.waits import (
    wait_all_visible,
    wait_clickable,
    wait_invisible,
    wait_visible,
)

MAIN_URL = 'https://pizzeria.skillbox.cc/'
CART_URL = 'https://pizzeria.skillbox.cc/cart/'
PIZZA_URL = 'https://pizzeria.skillbox.cc/product/пицца-4-в-1/'
BOARD_SELECT = (By.CSS_SELECTOR, 'select#board_pack')
PRODUCT_TITLE = (By.CSS_SELECTOR, 'h1.product_title')

ADD_TO_CART_SINGLE = (By.CSS_SELECTOR, 'button.single_add_to_cart_button')
CART_LINK = (By.CSS_SELECTOR, 'a.cart-contents')
CART_TABLE = (By.CSS_SELECTOR, 'table.shop_table.cart')
CART_ITEM = (By.CSS_SELECTOR, '.cart_item')
CART_ITEM_REMOVE_BUTTON = (By.CSS_SELECTOR, '.cart_item a[class="remove"]')
CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, '.cart-empty')

QUANTITY_INPUT = (By.CSS_SELECTOR, '.cart_item input.qty')
UPDATE_CART_BUTTON = (By.CSS_SELECTOR, 'button[name="update_cart"]')
ORDER_TOTAL = (By.CSS_SELECTOR, '.order-total .amount')


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestCartPage:

    @allure.story("Корзина")
    @allure.title("TC-10: Увеличение количества пиццы в корзине")
    def test_cart_item_count(self, selenium, go_to_url):
        with allure.step("Открыть страницу подробностей пиццы"):
            go_to_url(PIZZA_URL)

        with allure.step("Дождаться загрузки страницы подробностей"):
            wait_visible(selenium, PRODUCT_TITLE)

        with allure.step("Дождаться загрузки выпадающего списка бортов"):
            board_element = wait_clickable(selenium, BOARD_SELECT)

        with allure.step("Выбрать опцию «Сырный - 55.00 р.»"):
            board_select = Select(board_element)
            board_select.select_by_visible_text("Сырный - 55.00 р.")

        with allure.step("Добавить пиццу с опцией в корзину"):
            add_button = wait_clickable(selenium, ADD_TO_CART_SINGLE)
            add_button.click()

        with allure.step("Перейти в корзину"):
            cart_link = wait_visible(selenium, CART_LINK)
            cart_link.click()

        wait_all_visible(selenium, CART_TABLE)

        with allure.step("Запомнить сумму заказа до изменения количества"):
            total_before = wait_visible(
                selenium, ORDER_TOTAL
            ).text.strip()

        with allure.step("Увеличить количество пиццы до 2"):
            quantity_input = wait_visible(selenium, QUANTITY_INPUT)
            quantity_input.clear()
            quantity_input.send_keys("2")

        with allure.step("Нажать кнопку «Обновить корзину»"):
            wait_clickable(selenium, UPDATE_CART_BUTTON).click()

        with allure.step("Дождаться пересчёта"):
            WebDriverWait(selenium, 10).until(
                lambda d: d.find_element(
                    *ORDER_TOTAL
                ).text.strip() != total_before,
                message="Сумма заказа не пересчиталась",
            )
            total_after = selenium.find_element(*ORDER_TOTAL).text.strip()

        with allure.step("Проверить, что количество стало 2"):
            quantity_after = wait_visible(
                selenium, QUANTITY_INPUT
            ).get_attribute("value")
            assert quantity_after == "2", \
                f"Количество {quantity_after}, ожидалось 2"

        with allure.step("Проверить, что сумма заказа пересчитана"):
            assert total_after != total_before, \
                f"Сумма не изменилась: {total_after}"

    @allure.story("Корзина")
    @allure.title("TC-11: Удаление позиции из корзины")
    def test_cart_item_del(self, selenium, go_to_url):
        with allure.step("Открыть страницу подробностей пиццы"):
            go_to_url(PIZZA_URL)

        with allure.step("Дождаться загрузки страницы подробностей"):
            wait_visible(selenium, PRODUCT_TITLE)

        with allure.step("Дождаться загрузки выпадающего списка бортов"):
            board_element = wait_clickable(selenium, BOARD_SELECT)

        with allure.step("Выбрать опцию «Сырный - 55.00 р.»"):
            board_select = Select(board_element)
            board_select.select_by_visible_text("Сырный - 55.00 р.")

        with allure.step("Добавить пиццу с опцией в корзину"):
            add_button = wait_clickable(selenium, ADD_TO_CART_SINGLE)
            add_button.click()

        with allure.step("Перейти в корзину"):
            cart_link = wait_visible(selenium, CART_LINK)
            cart_link.click()

        wait_all_visible(selenium, CART_TABLE)

        with allure.step("Удалить позицию из корзины"):
            wait_clickable(selenium, CART_ITEM_REMOVE_BUTTON).click()

        with allure.step("Дождаться, что позиция удалена из корзины"):
            wait_invisible(selenium, CART_ITEM)

        with allure.step("Проверить, что в корзине нет позиций"):
            cart_items = selenium.find_elements(*CART_ITEM)
            assert len(cart_items) == 0, \
                f"В корзине осталось {len(cart_items)} позиций"

        with allure.step("Проверить сообщение о пустой корзине"):
            empty_message = wait_visible(selenium, CART_EMPTY_MESSAGE)
            assert "корзина пуста" in empty_message.text.lower(), \
                f"Сообщение «{empty_message.text}» " \
                f"не подтверждает пустую корзину"