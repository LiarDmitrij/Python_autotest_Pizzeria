import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.waits import wait_all_visible, wait_clickable, wait_visible

MAIN_URL = 'https://pizzeria.skillbox.cc/'
PIZZA_URL = 'https://pizzeria.skillbox.cc/product/пицца-4-в-1/'
PIZZA_SECTION = (By.XPATH, '//*[@id="product1"]')
PIZZA_IMAGE   = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] img.wp-post-image')
ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] a.add_to_cart_button')
PIZZA_NAME_IN_CARD = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] a[title]')

PIZZA_IMAGE_2 = (By.CSS_SELECTOR, '#product1 li[data-slick-index="1"] img.wp-post-image')
ADD_TO_CART_BUTTON_2 = (By.CSS_SELECTOR,'#product1 li[data-slick-index="1"] a.add_to_cart_button')
ADDED_TO_CART_2 = (By.CSS_SELECTOR,'#product1 li[data-slick-index="1"] a.added_to_cart')
CART_LINK = (By.CSS_SELECTOR, 'a.cart-contents')
CART_ITEM = (By.CSS_SELECTOR, '.cart_item')

ACTIVE_SLIDES = (By.CSS_SELECTOR, '#product1 li.slick-active')
SLIDER_NEXT = (By.CSS_SELECTOR, '#product1 .slick-next')
SLIDER_PREV = (By.CSS_SELECTOR, '#product1 .slick-prev')


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestMainPage:

    @allure.story("Главная страница")
    @allure.title("TC-01: Отображение слайдера с пиццами на главной странице")
    def test_slider_pizza_displayed_on_main_page(self, selenium, go_to_url):
        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url(MAIN_URL)

        with allure.step("Дождаться загрузки слайдера с пиццами"):
            slide_section = wait_visible(selenium, PIZZA_SECTION)
            assert slide_section.is_displayed(), \
                "Секция слайдера с пиццами не отображается"

        with allure.step("Дождаться загрузки изображения пиццы в слайде"):
            pizza_image = wait_visible(selenium, PIZZA_IMAGE)
            WebDriverWait(selenium, 10).until(
                lambda d: d.execute_script(
                    "return arguments[0].complete"
                    " && arguments[0].naturalWidth > 0",
                    pizza_image,
                ),
                message="Изображение пиццы не загрузилось",
            )

        with allure.step("Проверить, что у изображения есть корректный src"):
            assert pizza_image.get_attribute("src"), \
                "У изображения пиццы отсутствует атрибут src"

    @allure.story("Главная страница")
    @allure.title("TC-02: Появление кнопки «В корзину» при наведении на пиццу")
    def test_add_to_cart_button_appears_on_hover(self, selenium, go_to_url):
        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url(MAIN_URL)

        with allure.step("Дождаться загрузки слайда с пиццами"):
            slide_item = wait_visible(selenium, PIZZA_IMAGE)

        with allure.step("Навести курсор мыши на карточку пиццы"):
            ActionChains(selenium).move_to_element(slide_item).perform()

        with allure.step("Дождаться появления кнопки «В корзину»"):
            add_button = wait_visible(selenium, ADD_TO_CART_BUTTON)

        with allure.step("Проверить, что кнопка «В корзину» отображается"):
            assert add_button.is_displayed(), \
                "Кнопка «В корзину» не отображается при наведении на пиццу"

    @allure.story("Главная страница")
    @allure.title("TC-03: Добавление нескольких пицц в корзину из слайдера")
    def test_add_several_pizzas_to_cart_from_slider(self, selenium, go_to_url):
        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url(MAIN_URL)

        with allure.step("Дождаться загрузки первой пиццы в слайдере"):
            first_pizza = wait_visible(selenium, PIZZA_IMAGE)

        with allure.step("Навести курсор на первую пиццу"):
            ActionChains(selenium).move_to_element(first_pizza).perform()

        with allure.step("Добавить первую пиццу в корзину"):
            first_button = wait_visible(selenium, ADD_TO_CART_BUTTON)
            first_button.click()

        with allure.step("Дождаться загрузки второй пиццы в слайдере"):
            second_pizza = wait_visible(selenium, PIZZA_IMAGE_2)

        with allure.step("Навести курсор на вторую пиццу"):
            ActionChains(selenium).move_to_element(second_pizza).perform()

        with allure.step("Добавить вторую пиццу в корзину"):
            second_button = wait_visible(selenium, ADD_TO_CART_BUTTON_2)
            second_button.click()

        with allure.step("Перейти в корзину"):
            cart_link = wait_visible(selenium, CART_LINK)
            cart_link.click()

        with allure.step("Проверить, что в корзине две позиции"):
            wait_all_visible(selenium, (By.CSS_SELECTOR, 'table.shop_table.cart'))
            cart_items = wait_all_visible(selenium, CART_ITEM)
            assert len(cart_items) == 2, \
                f"В корзине {len(cart_items)} позиций, ожидалось 2"

    @allure.story("Главная страница")
    @allure.title("TC-04: Переключение слайдера вправо и влево")
    def test_slider_switch(self, selenium, go_to_url):
        selenium.maximize_window()
        
        def active_indexes():
            slides = selenium.find_elements(*ACTIVE_SLIDES)
            return tuple(
                slide.get_attribute("data-slick-index") for slide in slides
            )

        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url(MAIN_URL)

        with allure.step("Дождаться загрузки слайдера с пиццами"):
            active = wait_visible(selenium, PIZZA_IMAGE)
            wait_all_visible(selenium, ACTIVE_SLIDES)

        with allure.step("Навести мышь на первый активный слайд"):
            ActionChains(selenium).move_to_element(active).perform()

        with allure.step("Запомнить набор активных слайдов до переключения"):
            indexes_before = active_indexes()
        
        with allure.step("Нажать кнопку переключения слайдера вправо"):
            next_button = wait_clickable(selenium, SLIDER_NEXT)
            next_button.click()

        with allure.step("Дождаться смены набора активных слайдов"):
            WebDriverWait(selenium, 10).until(
                lambda d: active_indexes() != indexes_before,
                message="Слайдер не переключился вправо",
            )
            indexes_after_next = active_indexes()

        with allure.step("Навести мышь на первый активный слайд"):
            active = wait_visible(selenium, PIZZA_IMAGE_2)
            ActionChains(selenium).move_to_element(active).perform()

        with allure.step("Нажать кнопку переключения слайдера влево"):
            prev_button = wait_clickable(selenium, SLIDER_PREV)
            prev_button.click()

        with allure.step("Дождаться смены набора активных слайдов"):
            WebDriverWait(selenium, 10).until(
                lambda d: active_indexes() != indexes_after_next,
                message="Слайдер не переключился влево",
            )
            indexes_after_prev = active_indexes()

        with allure.step("Проверить, что вернулись к исходному набору"):
            assert indexes_after_prev == indexes_before, \
                f"После next+prev активные {indexes_after_prev}, " \
                f"ожидались исходные {indexes_before}"

    @allure.story("Главная страница")
    @allure.title("TC-05: Добавление пиццы в корзину после переключения слайдера")
    def test_add_pizza_to_cart_after_slider_switch(self, selenium, go_to_url):
        selenium.maximize_window()

        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url(MAIN_URL)

        with allure.step("Дождаться загрузки слайдера с пиццами"):
            first_pizza = wait_visible(selenium, PIZZA_IMAGE)

        with allure.step("Навести мышь на первую пиццу"):
            ActionChains(selenium).move_to_element(first_pizza).perform()

        with allure.step("Нажать кнопку переключения слайдера вправо"):
            next_button = wait_clickable(selenium, SLIDER_NEXT)
            next_button.click()

        with allure.step("Дождаться появления второй пиццы в слайдере"):
            second_pizza = wait_visible(selenium, PIZZA_IMAGE_2)
            wait_all_visible(selenium, ACTIVE_SLIDES)

        with allure.step("Навести мышь на вторую пиццу"):
            ActionChains(selenium).move_to_element(second_pizza).perform()

        with allure.step("Добавить вторую пиццу в корзину"):
            add_button = wait_visible(selenium, ADD_TO_CART_BUTTON_2)
            add_button.click()
            wait_visible(selenium, ADDED_TO_CART_2)

        with allure.step("Перейти в корзину"):
            cart_link = wait_visible(selenium, CART_LINK)
            cart_link.click()

        with allure.step("Проверить, что в корзине одна позиция"):
            cart_items = wait_all_visible(selenium, CART_ITEM)
            assert len(cart_items) == 1, \
                f"В корзине {len(cart_items)} позиций, ожидалась 1"

    @allure.story("Главная страница")
    @allure.title("TC-06: Переход на страницу подробностей пиццы по клику на изображение")
    def test_open_pizza_details_by_click_on_image(self, selenium, go_to_url):
        selenium.maximize_window()

        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url(MAIN_URL)
            
        with allure.step("Дождаться загрузки первой пиццы в слайдере"):
            pizza_image = wait_visible(selenium, PIZZA_IMAGE)
            wait_all_visible(selenium, ACTIVE_SLIDES)

        with allure.step("Запомнить название пиццы в карточке"):
            pizza_name = wait_visible(
                selenium, PIZZA_NAME_IN_CARD
            ).get_attribute("title").strip()

        with allure.step("Кликнуть по изображению пиццы"):
            pizza_image.click()

        with allure.step("Дождаться загрузки страницы подробностей"):
            product_title = wait_visible(selenium, (By.CSS_SELECTOR, 'h1.product_title'))

        with allure.step("Проверить, что открылась страница нужной пиццы"):
            title_text = product_title.text.strip()
            assert title_text == pizza_name, \
                f"Открылась пицца «{title_text}», " \
                f"ожидалась «{pizza_name}»"