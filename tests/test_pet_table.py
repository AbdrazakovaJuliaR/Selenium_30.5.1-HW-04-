# Проверка таблицы питомцев (явные ожидания)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.credentials import EMAIL, PASSWORD

def test_my_pets_table(driver):
    driver.find_element(By.ID, 'email').send_keys(EMAIL)
    driver.find_element(By.ID, 'pass').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    driver.get('https://petfriends.skillfactory.ru/my_pets')  # переход к таблице

    # ⏳ Явное ожидание загрузки таблицы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table'))
    )

    # Проверка, что таблица содержит хотя бы одну строку питомца
    rows = driver.find_elements(By.CSS_SELECTOR, 'table.table tbody tr')
    assert len(rows) > 0
