import logging
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)


def handle_certain_exceptions(func):
    def wraps(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(e)
            return

    return wraps


class WebDriver():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        executable_path = BASE_DIR + "/../chromedriver_93"
        self.driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

    def find(self, search_name):
        image_url = self.get_search_page(search_name)
        return image_url

    @handle_certain_exceptions
    def get_search_page(self, search_name):
        self.driver.get(
            "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
        register_button = self.driver.find_element(by=By.CLASS_NAME, value="vector-search-box-input")
        if not register_button:
            return

        register_button.send_keys(search_name)
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "suggestions-results"))
        )
        register_button.send_keys(Keys.DOWN)
        register_button.send_keys(Keys.ENTER)

        try:
            return self.get_photo_from_page()
        except NoSuchElementException:
            pass
            return self.get_from_search_results()

    def get_photo_from_page(self):
        first_headline = self.driver.find_element(by=By.CLASS_NAME, value='mw-first-heading')
        main_photo_container = self.driver.find_element(by=By.CLASS_NAME, value='infobox-image')
        main_photo = main_photo_container.find_element(by=By.TAG_NAME, value='img')
        return main_photo.get_attribute('src')

    def get_from_search_results(self):
        search_results = self.driver.find_elements(by=By.CLASS_NAME, value='mw-search-result-heading')
        results_urls = []
        for search_result in search_results:
            search_result_link = search_result.find_element(by=By.TAG_NAME, value='a')
            search_result_url = search_result_link.get_attribute('href')
            if search_result_url:
                results_urls.append(search_result_url)

        for result_url in results_urls:
            self.driver.get(result_url)
            try:
                photo_url = self.get_photo_from_page()
                if photo_url:
                    return photo_url
            except NoSuchElementException:
                continue


if __name__ == "__main__":
    driver_service = WebDriver()
    # driver_service.find("Сталин")
    # driver_service.find("Ленин")
    # driver_service.find("Молотов")
    # driver_service.find("Александр Матросов ")
    # driver_service.find("Евгений Перминов")
    # driver_service.find("Привет мир")
    driver_service.find("Мир на изнанку")
