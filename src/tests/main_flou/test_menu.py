import allure


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestMenu:

    @allure.story("Меню")
    @allure.title("TC-12: Переход во вкладку «Меню» и выбор раздела «Десерты»")
    def test_open_desserts_from_menu(self, menu_page, go_to_url):
        with allure.step("Открыть корзину"):
            go_to_url('https://pizzeria.skillbox.cc/cart/')

        # menu_page.open_desserts() - одним движением либо 5 снизу движений
        menu_page.hover_menu()
        menu_page.wait_submenu()
        menu_page.hover_desserts()
        menu_page.click_desserts()
        menu_page.wait_desserts_page()

        with allure.step("Проверить, что заголовок страницы Десерты"):
            title_text = menu_page.get_title()
            assert title_text == "ДЕСЕРТЫ", \
                f"Заголовок страницы «{title_text}», ожидался «Десерты»"
