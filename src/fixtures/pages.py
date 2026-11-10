import pytest

from src.actions.cart_page import CartPage
from src.actions.checkout_page import CheckoutPage
from src.actions.main_page import MainPage
from src.actions.product_page import ProductPage
from src.actions.products_page import ProductsPage

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
def products_page(selenium):
    selenium.maximize_window()
    return ProductsPage(selenium)


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
def products_filtered(products_page):
    products_page.open_page(DESSERTS_URL).filter_by_max_price(135)
    return products_page