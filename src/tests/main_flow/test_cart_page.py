import allure


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestCartPage:

    @allure.story("Корзина")
    @allure.title("TC-10: Увеличение количества пиццы в корзине")
    def test_cart_item_count(self, product_page, cart_page):
        product_page.open_page(product_page.PIZZA_URL)
        product_page.select_board("Сырный - 55.00 р.")
        product_page.add_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        with allure.step("Запомнить сумму заказа до изменения количества"):
            total_before = cart_page.get_total()

        cart_page.set_quantity(2)
        cart_page.click_update()
        total_after = cart_page.wait_total_changed(total_before)

        with allure.step("Проверить, что количество стало 2"):
            quantity_after = cart_page.get_quantity()
        with allure.step("Сравнить"):
            assert quantity_after == "2", \
                f"Количество {quantity_after}, ожидалось 2"

        with allure.step("Проверить, что сумма заказа пересчитана"):
            assert total_after != total_before, \
                f"Сумма не изменилась: {total_after}"

    @allure.story("Корзина")
    @allure.title("TC-11: Удаление позиции из корзины")
    def test_cart_item_del(self, product_page, cart_page):
        product_page.open_page(product_page.PIZZA_URL)
        product_page.select_board("Сырный - 55.00 р.")
        product_page.add_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        cart_page.remove_item()
        cart_page.wait_item_removed()

        with allure.step("Проверить, что в корзине нет позиций"):
            count = cart_page.get_items_count()
            assert count == 0, \
                f"В корзине осталось {count} позиций"

        with allure.step("Проверить сообщение о пустой корзине"):
            message = cart_page.get_empty_message()
            assert "корзина пуста" in message.lower(), \
                f"Сообщение «{message}» не подтверждает пустую корзину"
