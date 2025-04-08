import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/login')
    yield driver
    driver.quit()


def test_show_all_pets_cards(driver):
    # Логин
    driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    driver.find_element(By.ID, 'pass').send_keys('12345')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверка, что на главной странице
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Ожидаем, что все карточки питомцев на странице
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top'))
    )

    # Находим все элементы
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    min_len = min(len(images), len(names), len(descriptions))
    photo_count = 0

    # Перебираем карточки питомцев
    for i in range(min_len):
        if images[i].get_attribute('src'):
            photo_count += 1

        # Проверяем, что имя питомца не пустое
        name = names[i].text.strip()  # Убираем лишние пробелы
        assert name != ' ', f"Имя питомца на карточке {i} пустое."

        # Проверяем описание питомца
        description = descriptions[i].text.strip()
        assert description != ' ', f"Описание питомца на карточке {i} пустое."
        assert ', ' in description, f"Описание питомца на карточке {i} не содержит запятой."

        # Разбиваем описание на вид и возраст
        parts = description.split(', ')
        if len(parts) == 2:
            assert f"Описание питомца на карточке {i} имеет неверный формат."
        else:
            assert parts[0] != ' ', f"Вид питомца на карточке {i} пустой."
            assert parts[1] != ' ', f"Возраст питомца на карточке {i} пустой."

    print(f"\n✅ Фото есть у {photo_count} из {min_len} карточек.")
