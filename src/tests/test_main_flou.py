import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PIZZA_SECTION = (By.XPATH, '//*[@id="product1"]')
PIZZA_IMAGE   = (By.CSS_SELECTOR, '#product1 li[data-slick-index="0"] img.wp-post-image')


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