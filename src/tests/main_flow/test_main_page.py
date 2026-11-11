import allure


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestMainPage:

    @allure.story("Главная страница")
    @allure.title("TC-01: Отображение слайдера с пиццами на главной странице")
    def test_slider_pizza_displayed_on_main_page(self, main_page):
        main_page.open_page()
        main_page.wait_slider()
        image = main_page.wait_pizza_image()

        with allure.step("Проверить, что у изображения есть корректный src"):
            assert image.get_attribute("src"), \
                "У изображения пиццы отсутствует атрибут src"

    @allure.story("Главная страница")
    @allure.title("TC-02: Появление кнопки «В корзину» при наведении на пиццу")
    def test_add_to_cart_button_appears_on_hover(self, main_page):
        main_page.open_page()
        main_page.wait_slider()
        main_page.hover_first_pizza()

        assert main_page.is_add_to_cart_visible(), \
            "Кнопка «В корзину» не отображается при наведении"

    @allure.story("Главная страница")
    @allure.title("TC-03: Добавление нескольких пицц в корзину из слайдера")
    def test_add_several_pizzas_to_cart_from_slider(self, main_page, cart_page):
        main_page.open_page()
        main_page.wait_slider()
        main_page.add_first_pizza_to_cart()
        main_page.add_second_pizza_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        with allure.step("Проверить, что в корзине две позиции"):
            cart_count = cart_page.get_items_count()
        with allure.step("Сравнить количество в корзине"):
            assert cart_count == 2, \
                f"В корзине {cart_count} позиций, ожидалось 2"

    @allure.story("Главная страница")
    @allure.title("TC-04: Переключение слайдера вправо и влево")
    def test_slider_switch(self, main_page):
        main_page.open_page()
        main_page.hover_first_active()

        indexes_before = main_page.get_active_indexes()

        main_page.click_next()
        indexes_after_next = main_page.wait_active_changed(
            indexes_before
        )

        with allure.step("Проверить, что набор активных слайдов изменился"):
            assert indexes_after_next != indexes_before, \
                "После переключения вправо активные слайды не изменились"

        main_page.wait_all_slider()
        main_page.hover_first_active()
        main_page.click_prev()
        indexes_after_prev = main_page.wait_active_changed(
            indexes_after_next
        )

        with allure.step("Проверить, что вернулись к исходному набору"):
            assert indexes_after_prev == indexes_before, \
                f"После next+prev активные {indexes_after_prev}, " \
                f"ожидались исходные {indexes_before}"

    @allure.story("Главная страница")
    @allure.title("TC-05: Добавление пиццы в корзину после переключения слайдера")
    def test_add_pizza_to_cart_after_slider_switch(self, main_page, cart_page):
        main_page.open_page()
        main_page.wait_slider()
        main_page.hover_first_active()
        main_page.click_next()
        main_page.add_second_pizza_to_cart()

        with allure.step("Перейти в корзину"):
            cart_page.open_by_header_link()

        with allure.step("Проверить, что в корзине одна позиция"):
            cart_names = cart_page.get_item_names()
            assert len(cart_names) == 1, \
                f"В корзине {len(cart_names)} позиций, ожидалась 1"

    @allure.story("Главная страница")
    @allure.title(
        "TC-06: Переход на страницу подробностей пиццы "
        "по клику на изображение"
    )
    def test_open_pizza_details_by_click_on_image(self, main_page, product_page):
        main_page.open_page()
        main_page.wait_all_slider()

        pizza_name = main_page.get_pizza_name_in_card()
        main_page.click_first_pizza_image()

        with allure.step("Проверить, что открылась страница нужной пиццы"):
            title_text = product_page.get_title()
            assert title_text == pizza_name, \
                f"Открылась пицца «{title_text}», " \
                f"ожидалась «{pizza_name}»"
