# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture(scope='function')
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  # ⏱ Неявное ожидание
    driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()
