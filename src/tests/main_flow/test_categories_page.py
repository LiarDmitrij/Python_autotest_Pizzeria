import allure

from src.actions.cart_page import CartPage
from src.actions.checkout_page import CheckoutPage
from src.utils.text import clean


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestCategoriesPage:

    @allure.story("Категории товаров")
    @allure.title("TC-13: Фильтрация десертов по бюджету до 135 руб.")
    def test_filter_by_price(self, categories_page):
        categories_page.open_desserts_filtered(135)

        with allure.step("Проверить, что все десерты не дороже 135 руб."):
            for price in categories_page.get_prices():
                assert price <= 135

    @allure.story("Категории товаров")
    @allure.title("TC-14: Добавление десерта в корзину")
    def test_add_dessert_to_cart(self, products_filtered, selenium):
        with allure.step("Запомнить название первого десерта"):
            dessert_name = products_filtered.get_first_product_name()

        with allure.step("Добавить первый десерт в корзину"):
            products_filtered.add_first_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page = CartPage(selenium).open_by_header_link()

        with allure.step("Проверить, что в корзине одна позиция"):
            cart_names = cart_page.get_item_names()
            assert len(cart_names) == 1, \
                f"В корзине {len(cart_names)} позиций, ожидалась 1"

        with allure.step("Проверить, что в корзине нужный десерт"):
            assert clean(cart_names[0]) == clean(dessert_name), \
                f"В корзине «{cart_names[0]}», ожидался «{dessert_name}»"

    @allure.story("Оформление заказа")
    @allure.title("TC-15: Запрос авторизации при оформлении заказа")
    def test_checkout_requires_login(self, products_filtered, selenium):
        cart_page = CartPage(selenium)
        checkout_page = CheckoutPage(selenium)

        products_filtered.add_first_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        checkout_page.click_checkout()
        login_toggle = checkout_page.wait_login_request()

        with allure.step("Проверить, что отображается запрос авторизации"):
            assert login_toggle.is_displayed(), \
                "Запрос авторизации не отображается при оформлении заказа"

        with allure.step("Проверить текст сообщения о необходимости входа"):
            message = checkout_page.get_login_message()
        with allure.step("Сравнить"):
            assert "Авторизуйтесь" in message, \
                f"Сообщение «{message}» не содержит «Авторизуйтесь»"
