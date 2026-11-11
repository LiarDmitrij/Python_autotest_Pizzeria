import datetime
import random
import string

import allure

from src.utils.text import clean, parse_price


def _short_suffix(length=6):
    return ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestCheckoutPage:

    @allure.story("Оформление заказа")
    @allure.title("TC-19: Оформление заказа авторизованным пользователем")
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

    @allure.story("Оформление заказа")
    @allure.title("TC-20: Выбор даты оформления заказа на завтра")
    def test_set_order_date_tomorrow(
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

        with allure.step("Выбрать дату заказа — завтра"):
            tomorrow = (
                datetime.date.today() + datetime.timedelta(days=1)
            ).isoformat()
            checkout_page.set_order_date(tomorrow)

        with allure.step("Проверить, что установлена дата завтра"):
            actual_date = checkout_page.get_order_date()
            assert actual_date == tomorrow, \
                f"Дата заказа «{actual_date}», ожидалась «{tomorrow}»"

    @allure.story("Оформление заказа")
    @allure.title("TC-21: Выбор оплаты при доставке и подтверждение заказа")
    def test_select_cod_and_place_order(
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

        with allure.step("Выбрать дату заказа — завтра"):
            tomorrow = (
                datetime.date.today() + datetime.timedelta(days=1)
            ).isoformat()
            checkout_page.set_order_date(tomorrow)

        checkout_page.select_cod_payment()

        with allure.step(
            "Проверить, что появилась надпись «Оплата наличными "
            "при доставке заказа»"
        ):
            checkout_page.wait_cod_description()
            description = checkout_page.get_cod_description()
            assert description == "Оплата наличными при доставке заказа.", \
                f"Описание оплаты «{description}» не соответствует " \
                f"ожидаемому"

        checkout_page.accept_terms()
        checkout_page.place_order()

    @allure.story("Оформление заказа")
    @allure.title("TC-22: Проверка подтверждения заказа, суммы и личных данных")
    def test_order_received_details(
        self, account_page, categories_page, cart_page,
        checkout_page, go_to_url,
    ):
        suffix = _short_suffix(6)
        username = f"user_{suffix}"
        email = f"u{suffix}@mail.ru"
        password = "Passw0rd!"

        first_name = "Андрей"
        last_name = "Тестов"
        address = "ул. Тестовая, 1"
        city = "Сыктывкар"
        state = "Сыктывкар"
        postcode = "167001"
        phone = "+79991234567"

        with allure.step("Предусловие: пользователь зарегистрирован"):
            go_to_url('https://pizzeria.skillbox.cc/')
            account_page.register(username, email, password)

        with allure.step("Предусловие: товар в корзине"):
            categories_page.open_page(
                'https://pizzeria.skillbox.cc/'
                'product-category/menu/deserts/'
            ).filter_by_max_price(135)
            categories_page.add_first_to_cart()

        with allure.step("Запомнить название десерта и сумму"):
            dessert_name = categories_page.get_first_product_name()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        checkout_page.click_checkout()
        checkout_page.wait_checkout_form()
        checkout_page.fill_billing(
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
        )

        with allure.step("Выбрать дату заказа — завтра"):
            tomorrow = (
                datetime.date.today() + datetime.timedelta(days=1)
            )
            checkout_page.set_order_date(tomorrow.isoformat())

        checkout_page.select_cod_payment()
        checkout_page.accept_terms()

        with allure.step("Запомнить сумму заказа до подтверждения"):
            checkout_total_text = checkout_page.get_checkout_total()

        checkout_page.place_order()
        checkout_page.wait_order_received()

        with allure.step("Проверить сообщение об успешном заказе"):
            message = checkout_page.get_success_message()
            assert "Спасибо! Ваш заказ был получен" in message, \
                f"Сообщение «{message}» не подтверждает заказ"

        with allure.step("Проверить дату заказа — завтра"):
            order_date = checkout_page.get_order_date_received()
            expected_date = tomorrow.strftime("%d.%m.%Y")
            assert order_date == expected_date, \
                f"Дата заказа «{order_date}», ожидалась «{expected_date}»"

        with allure.step("Проверить email"):
            order_email = checkout_page.get_order_email()
            assert order_email == email, \
                f"Email «{order_email}», ожидался «{email}»"

        with allure.step("Проверить сумму заказа"):
            order_total = parse_price(
                checkout_page.get_order_total()
            )
            checkout_total = parse_price(checkout_total_text)
            assert order_total == checkout_total, \
                f"Сумма заказа {order_total}, " \
                f"ожидалась {checkout_total}"

        with allure.step("Проверить метод оплаты"):
            payment = checkout_page.get_order_payment()
            assert payment == "Оплата при доставке", \
                f"Метод оплаты «{payment}», ожидался " \
                f"«Оплата при доставке»"

        with allure.step("Проверить заказанный товар"):
            item_name = checkout_page.get_order_item_name()
            assert clean(item_name) == clean(dessert_name), \
                f"Товар «{item_name}», ожидался «{dessert_name}»"

        with allure.step("Проверить адрес доставки"):
            address_text = checkout_page.get_customer_address()
            assert first_name in address_text, \
                f"В адресе «{address_text}» нет имени «{first_name}»"
            assert last_name in address_text, \
                f"В адресе «{address_text}» нет фамилии «{last_name}»"
            assert address in address_text, \
                f"В адресе «{address_text}» нет адреса «{address}»"
            assert city in address_text, \
                f"В адресе «{address_text}» нет города «{city}»"
            assert postcode in address_text, \
                f"В адресе «{address_text}» нет индекса «{postcode}»"
            assert phone in address_text, \
                f"В адресе «{address_text}» нет телефона «{phone}»"
            assert email in address_text, \
                f"В адресе «{address_text}» нет email «{email}»"