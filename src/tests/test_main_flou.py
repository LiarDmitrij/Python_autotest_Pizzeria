import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PIZZA_SECTION = (By.XPATH, '//*[@id="product1"]')
PIZZA_IMAGE   = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] img.wp-post-image')
ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] a.add_to_cart_button')


@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestMainPage:

    @allure.story("Главная страница")
    @allure.title("TC-01: Отображение слайдера с пиццами на главной странице")
    def test_slider_pizza_displayed_on_main_page(self, selenium, go_to_url):
        with allure.step("Открыть главную страницу сайта Pizzeria"):
            go_to_url("https://pizzeria.skillbox.cc/")

        with allure.step("Дождаться загрузки слайдера с пиццами"):
            slide_section = WebDriverWait(selenium, 10).until(
                EC.visibility_of_element_located(PIZZA_SECTION)
            )
            assert slide_section.is_displayed(), \
                "Секция слайдера с пиццами не отображается"

        with allure.step("Дождаться загрузки изображения пиццы в слайде"):
            pizza_image = WebDriverWait(selenium, 10).until(
                EC.visibility_of_element_located(PIZZA_IMAGE)
            )
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

        with allure.step("Дождаться загрузки слайда с пиццей"):
            slide_item = WebDriverWait(selenium, 10).until(
                EC.visibility_of_element_located(PIZZA_IMAGE)
            )

        with allure.step("Навести курсор мыши на карточку пиццы"):
            ActionChains(selenium).move_to_element(slide_item).perform()

        with allure.step("Дождаться появления кнопки «В корзину»"):
            add_button = WebDriverWait(selenium, 10).until(
                EC.visibility_of_element_located(ADD_TO_CART_BUTTON)
            )

        with allure.step("Проверить, что кнопка «В корзину» отображается"):
            assert add_button.is_displayed(), \
                "Кнопка «В корзину» не отображается при наведении на пиццу"