import allure


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestAccountPage:

    @allure.story("Мой аккаунт")
    @allure.title("TC-16: Переход к регистрации через вкладку «Мой аккаунт»")
    def test_open_registration(self, account_page, go_to_url):
        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url('https://pizzeria.skillbox.cc/')

        with allure.step("Перейти во вкладку «Мой аккаунт»"):
            account_page.open_by_header_link()

        with allure.step("Проверить, что отображается кнопка «Зарегистрироваться»"):
            assert account_page.is_register_button_visible(), \
                "Кнопка «Зарегистрироваться» не отображается"

        with allure.step("Нажать кнопку «Зарегистрироваться»"):
            account_page.click_register()

        with allure.step("Проверить, что открылась форма регистрации"):
            current_url = account_page.driver.current_url
            assert "/register/" in current_url, \
                f"Открылась страница {current_url}, " \
                f"ожидалась страница регистрации (/register/)"