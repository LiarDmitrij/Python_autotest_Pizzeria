
from playwright.sync_api import Page, expect

def test_open_site(page: Page):
    page.goto("https://pizzeria.skillbox.cc/")
    expect(page).to_have_title("Pizzeria — Пиццерия")
    pass