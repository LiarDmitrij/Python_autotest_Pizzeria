import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.utils.waits import wait_all_visible, wait_clickable, wait_visible

BOARD_SELECT = (By.CSS_SELECTOR, 'select#board_pack')
PRODUCT_TITLE = (By.CSS_SELECTOR, 'h1.product_title')
PIZZA_URL = 'https://pizzeria.skillbox.cc/product/пицца-4-в-1/'

ADD_TO_CART_SINGLE = (By.CSS_SELECTOR, 'button.single_add_to_cart_button')

CART_LINK = (By.CSS_SELECTOR, 'a.cart-contents')
CART_ITEM = (By.CSS_SELECTOR, '.cart_item')
CART_ITEM_OPTION = (By.CSS_SELECTOR, '.cart_item dl.variation dd.variation- p')

@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestPoductPage:

    @allure.story("Cтраница продукта")
    @allure.title("TC-07: Выбор дополнительной опции (сырный борт) на странице пиццы")
    def test_select_border_option(self, selenium, go_to_url):
        with allure.step("Открыть страницу подробностей пиццы"):
            go_to_url(PIZZA_URL)

        with allure.step("Дождаться загрузки страницы подробностей"):
            wait_visible(selenium, PRODUCT_TITLE)

        with allure.step("Дождаться загрузки выпадающего списка бортов"):
            board_element = wait_clickable(selenium, BOARD_SELECT)

        with allure.step("Выбрать опцию «Сырный - 55.00 р.»"):
            board_select = Select(board_element)
            board_select.select_by_visible_text("Сырный - 55.00 р.")

        with allure.step("Проверить, что выбрана опция «Сырный»"):
            selected = board_select.first_selected_option.text.strip()
            assert selected == "Сырный - 55.00 р.", \
                f"Выбрана опция «{selected}», ожидалась " \
                f"«Сырный - 55.00 р.»"

    @allure.story("Страница пиццы")
    @allure.title("TC-08: Добавление пиццы с дополнительной опцией в корзину")
    def test_add_pizza_with_option_to_cart(self, selenium, go_to_url):
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
            cart_link = wait_clickable(selenium, CART_LINK)
            cart_link.click()

        with allure.step("Проверить, что в корзине одна позиция"):
            
            wait_all_visible(selenium, (By.CSS_SELECTOR, 'table.shop_table.cart'))
            cart_items = selenium.find_elements(By.CSS_SELECTOR, ".cart_item")
            assert len(cart_items) == 1, \
                f"В корзине {len(cart_items)} позиций, ожидалась 1"

        with allure.step("Проверить, что в корзине указан «Сырный борт»"):
            option_text = wait_visible(
                selenium, CART_ITEM_OPTION
            ).text.strip()
            assert option_text == "Сырный борт", \
                f"В корзине опция «{option_text}», " \
                f"ожидалась «Сырный борт»"

    # @allure.story("Страница пиццы")
    # @allure.title("TC-09: Проверка состава корзины после добавления пицц")
    # """ТС-03, ТС-08 покрывают"""