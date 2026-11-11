import allure

from src.utils.text import parse_price


@allure.epic("Pizzeria")
@allure.feature("Флоу с промокодом")
class TestPromoCode:

    @allure.story("Промокоды")
    @allure.title("TC-23: Применение промокода GIVEMEHALYAVA - скидка 10%")
    def test_apply_promo_code_discount(
        self, account_page, categories_page, cart_page,
        checkout_page, go_to_url,
    ):
        promo_code = "GIVEMEHALYAVA"
        username = "aa"
        password = "qwert"

        with allure.step("Предусловие: пользователь авторизован"):
            go_to_url('https://pizzeria.skillbox.cc/')
            account_page.open_by_header_link()
            account_page.login(username, password)
            account_page.is_logged_in()
            account_page.open_by_header_link_auth()

        with allure.step("Предусловие: товар в корзине"):
            go_to_url('https://pizzeria.skillbox.cc/')
            categories_page.open_page(
                'https://pizzeria.skillbox.cc/'
                'product-category/menu/deserts/'
            ).filter_by_max_price(135)
            categories_page.add_first_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        with allure.step("Нажать кнопку «Перейти к оплате»"):
            checkout_page.click_checkout()
            checkout_page.wait_checkout_form()

        checkout_page.remove_coupon_if_present()

        with allure.step("Запомнить итоговую сумму до применения купона"):
            total_before_text = checkout_page.get_checkout_total()

        checkout_page.show_coupon_form()
        checkout_page.apply_coupon(promo_code)
        checkout_page.wait_coupon_message()

        with allure.step("Проверить сообщение об успешном применении купона"):
            message = checkout_page.get_coupon_message()
            assert "Coupon code applied successfully" in message, \
                f"Сообщение «{message}» не подтверждает применение купона"

        with allure.step("Дождаться пересчёта суммы заказа"):
            total_after_text = checkout_page.wait_total_changed(
                total_before_text
            )

        with allure.step("Проверить, что сумма уменьшилась на 10%"):
            total_before = parse_price(total_before_text)
            total_after = parse_price(total_after_text)
            expected = round(total_before * 0.9, 2)
            assert abs(total_after - expected) <= 0.01, \
                f"Сумма после скидки {total_after}, " \
                f"ожидалась {expected} (10% от {total_before})"

        with allure.step("Проверить сумму скидки — 10% от исходной"):
            discount_text = checkout_page.get_coupon_discount()
            discount = parse_price(discount_text)
            expected_discount = round(total_before * 0.1, 2)
            assert abs(discount - expected_discount) <= 0.01, \
                f"Скидка {discount}, ожидалась {expected_discount}"

    @allure.story("Промокоды")
    @allure.title(
        "TC-24: Применение недействительного промокода DC120 - "
        "скидка не применяется"
    )
    def test_apply_invalid_promo_code(
        self, account_page, categories_page, cart_page,
        checkout_page, go_to_url,
    ):
        promo_code = "DC120"
        username = "aa"
        password = "qwert"

        with allure.step("Предусловие: пользователь авторизован"):
            go_to_url('https://pizzeria.skillbox.cc/')
            account_page.open_by_header_link()
            account_page.login(username, password)
            account_page.is_logged_in()
            account_page.open_by_header_link_auth()

        with allure.step("Предусловие: товар в корзине"):
            go_to_url('https://pizzeria.skillbox.cc/')
            categories_page.open_page(
                'https://pizzeria.skillbox.cc/'
                'product-category/menu/deserts/'
            ).filter_by_max_price(135)
            categories_page.add_first_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        with allure.step("Нажать кнопку «Перейти к оплате»"):
            checkout_page.click_checkout()
            checkout_page.wait_checkout_form()

        checkout_page.remove_coupon_if_present()

        with allure.step("Запомнить итоговую сумму до применения купона"):
            total_before_text = checkout_page.get_checkout_total()

        checkout_page.show_coupon_form()
        checkout_page.apply_coupon(promo_code)
        checkout_page.wait_coupon_error()

        with allure.step("Проверить, что купон не применился"):
            error_text = checkout_page.get_coupon_error()
            assert error_text, \
                "Сообщение об ошибке недействительного купона пустое"
            assert "Coupon code applied successfully" not in error_text, \
                f"Недействительный купон {promo_code} был применён"

        with allure.step("Проверить сообщение «Неверный купон»"):
            error_text = checkout_page.get_coupon_error()
            assert "Неверный купон" in error_text, \
                f"Сообщение «{error_text}» не подтверждает " \
                f"недействительность купона"

        assert checkout_page.is_coupon_row_absent(), \
            "Строка скидки по купону присутствует, " \
            "хотя купон недействителен"

        with allure.step("Проверить, что сумма заказа НЕ изменилась"):
            total_after_text = checkout_page.get_checkout_total()
            total_before = parse_price(total_before_text)
            total_after = parse_price(total_after_text)
            assert total_after == total_before, \
                f"Сумма изменилась с {total_before} на {total_after}, " \
                f"хотя купон {promo_code} недействителен"
