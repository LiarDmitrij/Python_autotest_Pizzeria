import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from src.actions.base import BasePage

MENU_LINK = (
    By.XPATH,
    '//nav//a[contains(normalize-space(.), "Меню")]',
)
SUB_MENU = (By.CSS_SELECTOR, 'ul.sub-menu')
DESSERTS_SUBMENU_LINK = (By.XPATH,
    ('//ul[contains(@class, "sub-menu")]//a[contains(normalize-space(.), '
    '"Десерты")]')
)
DESSERTS_TITLE = (By.CSS_SELECTOR, 'h1.entry-title')


class MenuPage(BasePage):

    @allure.step("Навести мышь на пункт меню «Меню»")
    def hover_menu(self):
        ActionChains(self.driver).move_to_element(
            self.find(MENU_LINK)
        ).perform()
        return self

    @allure.step("Дождаться открытия выпадающего подменю")
    def wait_submenu(self):
        self.find(SUB_MENU)
        return self

    @allure.step("Навести мышь на пункт «Десерты»")
    def hover_desserts(self):
        ActionChains(self.driver).move_to_element(
            self.find(DESSERTS_SUBMENU_LINK)
        ).perform()
        return self

    @allure.step("Кликнуть по пункту «Десерты»")
    def click_desserts(self):
        self.click(DESSERTS_SUBMENU_LINK)
        return self

    @allure.step("Дождаться загрузки страницы «Десерты»")
    def wait_desserts_page(self):
        self.find(DESSERTS_TITLE)
        return self

    @allure.step("Получить заголовок страницы")
    def get_title(self):
        return self.find(DESSERTS_TITLE).text.strip()

    @allure.step("Открыть раздел «Десерты» через меню")
    def open_desserts(self):
        self.hover_menu()
        self.wait_submenu()
        self.hover_desserts()
        self.click_desserts()
        self.wait_desserts_page()
        return self