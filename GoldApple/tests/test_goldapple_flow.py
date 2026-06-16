import time
from pytest import mark

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://goldapple.by"


# ---------- DRIVER ----------
def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-geolocation")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# ---------- POPUPS ----------
from selenium.common.exceptions import TimeoutException

def close_cookies(driver, wait):
    try:
        cookie_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='принять']/ancestor::button")
            )
        )

        driver.execute_script("arguments[0].click();", cookie_btn)
        print("Cookies accepted")

    except TimeoutException:
        print("Cookie banner not found")

# ---------- SEARCH ----------
def search_product(driver, wait, query):

    #  нажать лупу
    search_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//div[text()='Поиск']]")
        )
    )
    search_button.click()

    #  ждать именно ВИДИМОЕ и АКТИВНОЕ поле
    search_input = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[placeholder='хочу купить']")
        )
    )

    #  кликнуть в него (важно!)
    search_input.click()

    #  очистить и ввести текст
    search_input.clear()
    search_input.send_keys(query)

    #  нажать Enter
    search_input.send_keys(Keys.ENTER)


    print("Поиск выполнен:", query)

def add_products(driver, wait, count=5):

    for i in range(count):

        # обновляем список карточек после возврата назад
        products = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "[class*='product-card-vertical__name']"
                )
            )
        )

        product = products[i]

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            product
        )

        time.sleep(1)

        driver.execute_script(
            "arguments[0].click();",
            product
        )

        # ждём кнопку корзины
        add_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(., 'добавить в корзину')]"
                )
            )
        )

        driver.execute_script(
            "arguments[0].click();",
            add_button
        )

        print(f"Товар {i+1} добавлен")

        time.sleep(2)

        # возвращаемся к поиску
        driver.back()

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "[class*='product-card-vertical__name']"
                )
            )
        )

        time.sleep(2)

        # ---------- OPEN CART ----------
def open_cart(driver, wait):
    cart_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "button.ga-header__tab_type_cart"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        cart_button
    )

    driver.execute_script(
        "arguments[0].click();",
        cart_button
    )

    print("Корзина открыта")

# ---------- TEST ----------


@mark.ui
def test_goldapple_flow():
    driver = create_driver()
    wait = WebDriverWait(driver, 30)

    try:
        #  открыть сайт
        driver.get(BASE_URL)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        close_cookies(driver, wait)

        #  поиск товара
        search_product(driver, wait, "крем")

        #  добавить товар
        add_products(driver, wait, 5)

        open_cart(driver, wait)



        print("TEST PASSED")

    finally:
        time.sleep(3)
        driver.quit()