import allure


@allure.epic("Pizzeria")
@allure.feature("Бонусная программа")
class TestBonusPage:

    @allure.story("Бонусная программа")
    @allure.title("TC-27: Регистрация в бонусной программе")
    def test_bonus_program_registration(self, bonus_page):
        name = "Андрей"
        phone = "+79991234567"

        bonus_page.open_page()
        bonus_page.enter_name(name)
        bonus_page.enter_phone(phone)
        bonus_page.submit()
        bonus_page.accept_alert()
        success = bonus_page.wait_success()

        with allure.step("Проверить сообщение об успехе"):
            text = success.text.strip()
            assert "Ваша карта оформлена" in text, \
                f"Сообщение «{text}» не подтверждает оформление карты"

    @allure.story("Бонусная программа")
    @allure.title("TC-28: Валидация полей - обязательность")
    def test_bonus_validation_empty_fields(self, bonus_page):
        with allure.step("Открыть страницу бонусной программы"):
            bonus_page.open_page()

        with allure.step("Не заполнять поля"):
            pass

        bonus_page.submit()

        assert bonus_page.is_alert_absent(), \
            "Появился alert, хотя поля не заполнены"

        with allure.step("Проверить сообщение о необходимости имени"):
            error_text = bonus_page.get_validation_error()
            assert "Поле \"Имя\" обязательно для заполнения" in error_text, \
                f"Сообщение «{error_text}» не содержит ошибку про имя"

        with allure.step("Проверить сообщение о необходимости телефона"):
            assert "Поле \"Телефон\" обязательно для заполнения" in error_text, \
                f"Сообщение «{error_text}» не содержит ошибку про телефон"

        with allure.step("Проверить, что поле «Имя» подсвечено красным"):
            name_border = bonus_page.get_name_border_color().lower()
            assert "red" in name_border or "rgb(255, 0, 0)" in name_border, \
                f"Рамка поля «Имя» не красная: {name_border}"

        with allure.step("Проверить, что поле «Телефон» подсвечено красным"):
            phone_border = bonus_page.get_phone_border_color().lower()
            assert "red" in phone_border or "rgb(255, 0, 0)" in phone_border, \
                f"Рамка поля «Телефон» не красная: {phone_border}"

        with allure.step("Проверить, что карта не оформлена"):
            assert "Ваша карта оформлена" not in error_text, \
                "Появилось сообщение об оформлении карты при пустых полях"

    @allure.story("Бонусная программа")
    @allure.title("TC-29: Валидация поля «Телефон» - некорректный номер")
    def test_bonus_validation_phone_format(self, bonus_page):
        name = "Андрей"
        invalid_phone = "123"

        with allure.step("Открыть страницу бонусной программы"):
            bonus_page.open_page()

        with allure.step("Ввести имя"):
            bonus_page.enter_name(name)

        with allure.step("Ввести телефон в неверном формате"):
            bonus_page.enter_phone(invalid_phone)

        with allure.step("Нажать «Оформить карту»"):
            bonus_page.submit()

        with allure.step("Проверить, что alert не появился"):
            assert bonus_page.is_alert_absent(), \
                "Появился alert, хотя телефон в неверном формате"

        with allure.step("Проверить сообщение о неверном формате телефона"):
            error_text = bonus_page.get_validation_error()
            assert "Введен неверный формат телефона" in error_text, \
                f"Сообщение «{error_text}» не содержит ошибку формата"

        with allure.step("Проверить, что карта не оформлена"):
            assert "Ваша карта оформлена" not in error_text, \
                "Появилось сообщение об оформлении карты при неверном " \
                "формате телефона"

        with allure.step("Проверить, что поле «Телефон» подсвечено красным"):
            border = bonus_page.get_phone_border_color().lower()
            assert "red" in border or "rgb(255, 0, 0)" in border, \
                f"Рамка поля «Телефон» не красная: {border}"
