import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.actions.base import BasePage

MAIN_URL = 'https://pizzeria.skillbox.cc/'

PIZZA_SECTION = (By.XPATH, '//*[@id="product1"]')
PIZZA_IMAGE = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] img.wp-post-image')
PIZZA_IMAGE_2 = (By.CSS_SELECTOR, '#product1 li[data-slick-index="1"] img.wp-post-image')
ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] a.add_to_cart_button')
ADD_TO_CART_BUTTON_2 = (By.CSS_SELECTOR, '#product1 li[data-slick-index="1"] a.add_to_cart_button')
ADDED_TO_CART_2 = (By.CSS_SELECTOR, '#product1 li[data-slick-index="1"] a.added_to_cart')
PIZZA_NAME_IN_CARD = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] a[title]')
ACTIVE_SLIDES = (By.CSS_SELECTOR, '#product1 li.slick-active')
SLIDER_NEXT = (By.CSS_SELECTOR, '#product1 .slick-next')
SLIDER_PREV = (By.CSS_SELECTOR, '#product1 .slick-prev')


class MainPage(BasePage):

    @allure.step("Открыть главную страницу сайта Pizzeria")
    def open_page(self):
        self.open(MAIN_URL)
        return self

    @allure.step("Дождаться загрузки слайдера с пиццами")
    def wait_slider(self):
        self.find(PIZZA_SECTION)
        return self

    @allure.step("Дождаться загрузки слайдера с пиццами")
    def wait_all_slider(self):
        self.find_all(ACTIVE_SLIDES)
        return self

    def wait_slick_prev(self):
        self.find(SLIDER_PREV)
        return self

    @allure.step("Дождаться загрузки изображения пиццы в слайде")
    def wait_pizza_image(self):
        image = self.find(PIZZA_IMAGE)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script(
                "return arguments[0].complete"
                " && arguments[0].naturalWidth > 0",
                image,
            ),
            message="Изображение пиццы не загрузилось",
        )
        return image

    @allure.step("Получить название пиццы в карточке")
    def get_pizza_name_in_card(self):
        return self.find(PIZZA_NAME_IN_CARD).get_attribute("title").strip()

    def hover_first_pizza(self):
        ActionChains(self.driver).move_to_element(
            self.find(PIZZA_IMAGE)
        ).perform()
        return self

    @allure.step("Проверить, что кнопка «В корзину» отображается")
    def is_add_to_cart_visible(self):
        return self.find(ADD_TO_CART_BUTTON).is_displayed()

    @allure.step("Добавить первую пиццу в корзину")
    def add_first_pizza_to_cart(self):
        self.hover_first_pizza()
        self.click(ADD_TO_CART_BUTTON)
        return self

    def hover_second_pizza(self):
        ActionChains(self.driver).move_to_element(
            self.find(PIZZA_IMAGE_2)
        ).perform()
        return self

    @allure.step("Добавить вторую пиццу в корзину")
    def add_second_pizza_to_cart(self):
        self.hover_second_pizza()
        self.click(ADD_TO_CART_BUTTON_2)
        self.find(ADDED_TO_CART_2)
        return self

    @allure.step("Кликнуть по изображению первой пиццы")
    def click_first_pizza_image(self):
        self.find(PIZZA_IMAGE).click()
        return self

    @allure.step("Получить набор активных слайдов")
    def get_active_indexes(self):
        return tuple(
            slide.get_attribute("data-slick-index")
            for slide in self.driver.find_elements(*ACTIVE_SLIDES)
        )

    def hover_first_active(self):
        active = self.driver.find_elements(*ACTIVE_SLIDES)
        ActionChains(self.driver).move_to_element(active[0]).perform()
        return self

    def hover_last_active(self):
        active = self.driver.find_elements(*ACTIVE_SLIDES)
        ActionChains(self.driver).move_to_element(active[-1]).perform()
        return self

    @allure.step("Нажать «вправо» в слайдере")
    def click_next(self):
        self.click(SLIDER_NEXT)
        return self

    @allure.step("Нажать «влево» в слайдере")
    def click_prev(self):
        self.click(SLIDER_PREV)
        return self

    @allure.step("Дождаться смены набора активных слайдов")
    def wait_active_changed(self, previous, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_active_indexes() != previous,
            message="Набор активных слайдов не изменился",
        )
        return self.get_active_indexes()