from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_visible(driver, locator, timeout=10):
    """Ждёт, пока элемент по локатору станет видимым, и возвращает его."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_clickable(driver, locator, timeout=10):
    """Ждёт, пока элемент по локатору станет видимым, и возвращает его."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_all_visible(driver, locator, timeout=10):
    WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(locator)
        )


def wait_staleness_of(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.staleness_of(locator)
    )


def wait_invisible(driver, locator, timeout=10):
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(locator)
    )


def wait_present(driver, locator, timeout=10):
    """Ждёт наличия элемента в DOM (без требования видимости)."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
