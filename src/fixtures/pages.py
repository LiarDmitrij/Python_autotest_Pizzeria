import pytest

from src.actions.products_page import ProductsPage

DESSERTS_URL = (
    'https://pizzeria.skillbox.cc/product-category/menu/deserts/'
)
PIZZA_CATEGORY_URL = (
    'https://pizzeria.skillbox.cc/product-category/menu/pizza/'
)


@pytest.fixture
def products_page(selenium):
    selenium.maximize_window()
    return ProductsPage(selenium)


@pytest.fixture
def products_filtered(products_page):
    products_page.open_page(DESSERTS_URL).filter_by_max_price(135)
    return products_page


@pytest.fixture
def product_page(products_page):
    products_page.open_page(PIZZA_CATEGORY_URL)
    return products_page