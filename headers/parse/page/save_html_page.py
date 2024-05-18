import os
import undetected_chromedriver as uc
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class Chrome:
    def __init__(self):
        self._is_closed = False

        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)")
        options.add_argument('--headless=new')

        self._browser = uc.Chrome(driver_executable_path='C:/Users/user/Desktop/manga/chromedriver/chromedriver.exe',
                                  browser_executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',
                                  disable_detection=True,
                                  options=options)
        self._wait = WebDriverWait(self._browser, 600)


    def save_manga_html(self, url, filename):
        try:
            self._browser.get(url)
            images = self._wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img#mangaPicture")))

            for img in images:
                self._wait.until(lambda browser: img.get_attribute('complete') == 'true')

            output_folder = 'html'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            file_path = os.path.join(output_folder, filename)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self._browser.page_source)

            print(f"HTML-страница успешно сохранена в '{file_path}'")

        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")


    def quit_browser(self):
        try:
            time.sleep(0.1)
            if not self._is_closed and self._browser:
                self._browser.quit()
                self._is_closed = True
        except:
            pass


    def __del__(self):
        self.quit_browser()