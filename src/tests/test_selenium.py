class TestSeleniumDefault:
    def test_open_site(self, go_to_url, selenium):
        go_to_url("https://pizzeria.skillbox.cc/")
        assert "Pizzeria — Пиццерия" in selenium.title