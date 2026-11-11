import pytest

from src.actions.account_page import AccountPage
from src.actions.cart_page import CartPage
from src.actions.categories_page import CategoriesPage
from src.actions.checkout_page import CheckoutPage
from src.actions.main_page import MainPage
from src.actions.menu_page import MenuPage
from src.actions.product_page import ProductPage

DESSERTS_URL = (
    'https://pizzeria.skillbox.cc/product-category/menu/deserts/'
)
PIZZA_CATEGORY_URL = (
    'https://pizzeria.skillbox.cc/product-category/menu/pizza/'
)


@pytest.fixture
def main_page(selenium):
    selenium.maximize_window()
    return MainPage(selenium)


@pytest.fixture
def categories_page(selenium):
    selenium.maximize_window()
    return CategoriesPage(selenium)


@pytest.fixture
def product_page(selenium):
    selenium.maximize_window()
    return ProductPage(selenium)


@pytest.fixture
def cart_page(selenium):
    return CartPage(selenium)


@pytest.fixture
def checkout_page(selenium):
    return CheckoutPage(selenium)


@pytest.fixture
def products_filtered(categories_page):
    categories_page.open_page(DESSERTS_URL).filter_by_max_price(135)
    return categories_page


@pytest.fixture
def menu_page(selenium):
    selenium.maximize_window()
    return MenuPage(selenium)


@pytest.fixture
def account_page(selenium):
    selenium.maximize_window()
    return AccountPage(selenium)
