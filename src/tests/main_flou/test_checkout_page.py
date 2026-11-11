import random
import string

import allure


def _short_suffix(length=6):
    return ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestCheckoutPage:

    @allure.story("Оформление заказа")
    @allure.title(
        "TC-19: Повторное оформление заказа авторизованным пользователем"
    )
    def test_checkout_as_authorized_user(
        self, account_page, categories_page, cart_page,
        checkout_page, go_to_url,
    ):
        suffix = _short_suffix(6)
        username = f"user_{suffix}"
        email = f"u{suffix}@mail.ru"
        password = "Passw0rd!"

        with allure.step("Предусловие: пользователь зарегистрирован"):
            go_to_url('https://pizzeria.skillbox.cc/')
            account_page.register(username, email, password)

        with allure.step("Предусловие: товар в корзине"):
            categories_page.open_page(
                'https://pizzeria.skillbox.cc/'
                'product-category/menu/deserts/'
            ).filter_by_max_price(135)
            categories_page.add_first_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        checkout_page.click_checkout()
        checkout_page.wait_checkout_form()

        checkout_page.fill_billing(
            first_name="Андрей",
            last_name="Тестов",
            address="ул. Тестовая, 1",
            city="Сыктывкар",
            state="Сыктывкар",
            postcode="167001",
            phone="+79991234567",
        )

        with allure.step("Проверить, что все поля заполнены"):
            values = checkout_page.get_billing_values()
            for field, value in values.items():
                assert value, \
                    f"Поле «{field}» пустое после заполнения"