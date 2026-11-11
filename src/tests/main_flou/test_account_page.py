import random
import string

import allure


def _short_suffix(length=6):
    return ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )


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

    @allure.story("Мой аккаунт")
    @allure.title("TC-17: Регистрация нового пользователя")
    def test_register_new_user(self, account_page, go_to_url):
        suffix = _short_suffix(6)
        username = f"user_{suffix}"
        email = f"u{suffix}@mail.ru"
        password = "Passw0rd!"

        assert len(username) <= 20, "Имя пользователя длиннее 20 символов"
        assert len(email) <= 20, "Email длиннее 20 символов"

        with allure.step("Открыть форму регистрации"):
            go_to_url('https://pizzeria.skillbox.cc/register/')

        with allure.step("Дождаться загрузки формы регистрации"):
            account_page.wait_register_form()

        with allure.step("Заполнить форму регистрации"):
            account_page.fill_register_form(
                username=username,
                email=email,
                password=password,
            )

        with allure.step("Отправить форму регистрации"):
            account_page.submit_register()

        with allure.step("Дождаться сообщения «Регистрация завершена»"):
            message = account_page.wait_registration_complete()

        with allure.step("Проверить, что регистрация завершена"):
            assert "Регистрация завершена" in message.text, \
                f"Сообщение «{message.text}» не подтверждает регистрацию"

    @allure.story("Мой аккаунт")
    @allure.title("TC-18: Вход в «Мой аккаунт» и проверка авторизации")
    def test_login_and_check_authorized(self, account_page, go_to_url):
        suffix = _short_suffix(6)
        username = f"user_{suffix}"
        email = f"u{suffix}@mail.ru"
        password = "Passw0rd!"

        with allure.step("Предусловие: пользователь зарегистрирован"):
            go_to_url('https://pizzeria.skillbox.cc/')
            account_page.register(username, email, password)

        with allure.step("Перейти в «Мой аккаунт» авторизованным"):
            account_page.open_by_header_link_auth()

        with allure.step("Проверить, что пользователь авторизован"):
            assert account_page.is_logged_in(), \
                "Пользователь не авторизован после входа"

        with allure.step("Проверить, что в приветствии имя пользователя"):
            greeting = account_page.get_greeting()
            assert username in greeting, \
                f"В приветствии «{greeting}» нет имени «{username}»"