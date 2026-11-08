import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.waits import wait_visible

PIZZA_SECTION = (By.XPATH, '//*[@id="product1"]')
PIZZA_IMAGE   = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] img.wp-post-image')
ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] a.add_to_cart_button')

PIZZA_IMAGE_2 = (By.CSS_SELECTOR, '#product1 li[data-slick-index="1"] img.wp-post-image')
ADD_TO_CART_BUTTON_2 = (By.CSS_SELECTOR,'#product1 li[data-slick-index="1"] a.add_to_cart_button')
CART_LINK = (By.CSS_SELECTOR, 'a.cart-contents')
CART_ITEM = (By.CSS_SELECTOR, '.cart_item')


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestMainPage:

    @allure.story("Главная страница")
    @allure.title("TC-01: Отображение слайдера с пиццами на главной странице")
    def test_slider_pizza_displayed_on_main_page(self, selenium, go_to_url):
        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url("https://pizzeria.skillbox.cc/")

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
            go_to_url("https://pizzeria.skillbox.cc/")

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
            go_to_url("https://pizzeria.skillbox.cc/")

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
            cart_items = WebDriverWait(selenium, 10).until(
                EC.visibility_of_all_elements_located(CART_ITEM)
            )
            assert len(cart_items) == 2, \
                f"В корзине {len(cart_items)} позиций, ожидалось 2"