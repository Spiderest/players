from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import scrapy, sys, time, os

class TokenAuthSpider(scrapy.Spider):
    name = 'token_auth_spider'

    def __init__(self, *args, **kwargs):
        super(TokenAuthSpider, self).__init__(*args, **kwargs)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(), options=options)

    def start_requests(self):
        self.driver.get("https://pleazgg.com/login")
        username_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        user = os.getenv('USER')
        password = os.getenv('PASSWORD')
        username_input.send_keys(user)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(5)

        self.driver.get("https://pleazgg.com/lobby")
        chat_container = self.driver.find_element(By.CLASS_NAME, "fixed-bottom")
        chat_container.click()
        time.sleep(5)

        self.parse_chat("")
        return []

    def parse_chat(self, response):
        try:
            path = os.path.join(os.getcwd(), 'source.html')
            page_html = self.driver.page_source
            with open(path, 'w', encoding='utf-8') as f:
                f.write(page_html)
        except Exception as e:
            self.driver.quit()
            self.close("ERROR")
            sys.exit(0)   
        finally:
            self.driver.quit()
            self.close("SHUTDOWN")

    def close(self, reason):
        print(reason)
