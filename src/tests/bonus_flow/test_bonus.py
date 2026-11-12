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