import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from src.utils.waits import wait_clickable, wait_visible

MENU_LINK = (
    By.XPATH,
    '//nav//a[contains(normalize-space(.), "Меню")]',
)
SUB_MENU = (By.CSS_SELECTOR, 'ul.sub-menu')
DESSERTS_SUBMENU_LINK = (By.XPATH,
    ('//ul[contains(@class, "sub-menu")]//a[contains(normalize-space(.), '
    '"Десерты")]'))
DESSERTS_TITLE = (By.CSS_SELECTOR, 'h1.entry-title')

@allure.epic("Pizzeria")
@allure.feature("Основной флоу клиента")
class TestMenu:

    @allure.story("Меню")
    @allure.title("TC-12: Переход во вкладку «Меню» и выбор раздела «Десерты»")
    def test_open_desserts_from_menu(self, selenium, go_to_url):
        selenium.maximize_window()

        with allure.step("Открыть корзину"):
            go_to_url('https://pizzeria.skillbox.cc/cart/')

        with allure.step("Навести мышь на пункт меню «Menu»"):
            wait_visible(selenium, (By.CSS_SELECTOR, 'section.home_navigation'))
            menu_link = wait_visible(selenium, MENU_LINK)
            ActionChains(selenium).move_to_element(menu_link).perform()

        with allure.step("Дождаться открытия выпадающего подменю"):
            wait_visible(selenium, SUB_MENU)

        with allure.step("Навести мышь на пункт «Десерты»"):
            desserts_link = wait_visible(selenium, DESSERTS_SUBMENU_LINK)
            ActionChains(selenium).move_to_element(desserts_link).perform()

        with allure.step("Кликнуть по пункту «Десерты»"):
            wait_clickable(selenium, desserts_link).click()

        with allure.step("Дождаться загрузки страницы «Десерты»"):
            title = wait_visible(selenium, DESSERTS_TITLE)

        with allure.step("Проверить заголовок страницы"):
            title_text = title.text.strip()
            assert title_text == "Десерты", \
                f"Заголовок страницы «{title_text}», ожидался «Десерты»"