import allure


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestProductPage:

    @allure.story("Страница продукта")
    @allure.title("TC-07: Выбор дополнительной опции (сырный борт) на странице пиццы"
    )
    def test_select_border_option(self, product_page):
        with allure.step("Открыть страницу подробностей пиццы"):
            product_page.open_page(product_page.PIZZA_URL)

        with allure.step("Выбрать опцию «Сырный - 55.00 р.»"):
            product_page.select_board("Сырный - 55.00 р.")

        with allure.step("Проверить, что выбрана опция «Сырный»"):
            selected = product_page.get_selected_board()
            assert selected == "Сырный - 55.00 р.", \
                f"Выбрана опция «{selected}», ожидалась " \
                f"«Сырный - 55.00 р.»"

    @allure.story("Страница продукта")
    @allure.title("TC-08: Добавление пиццы с дополнительной опцией в корзину")
    def test_add_pizza_with_option_to_cart(self, product_page, cart_page):
        with allure.step("Открыть страницу подробностей пиццы"):
            product_page.open_page(product_page.PIZZA_URL)

        with allure.step("Выбрать опцию «Сырный - 55.00 р.»"):
            product_page.select_board("Сырный - 55.00 р.")

        with allure.step("Добавить пиццу с опцией в корзину"):
            product_page.add_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        with allure.step("Проверить, что в корзине одна позиция"):
            item_count = cart_page.get_items_count()
        with allure.step("Сравнить"):
            assert item_count == 1, \
                f"В корзине {item_count} позиций, ожидалась 1"

        with allure.step("Проверить, что в корзине указан «Сырный борт»"):
            option = cart_page.get_item_option()
        with allure.step("Сравнить"):
            assert option == "Сырный борт", \
                f"В корзине опция «{option}», ожидалась «Сырный борт»"