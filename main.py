import asyncio, sys, os
from bs4 import BeautifulSoup
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os


def startSpider():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        driver.get("https://pleazgg.com/login")
        time.sleep(10)

        driver.find_element(By.ID, "username").send_keys(os.getenv('USER'))
        driver.find_element(By.ID, "password").send_keys(os.getenv('PASSWORD'))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(5)

        driver.get("https://pleazgg.com/lobby")
        driver.find_element(By.CLASS_NAME, "fixed-bottom").click()
        time.sleep(5)

        path = os.path.join(os.getcwd(), 'source.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("finished")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        driver.quit()

#-----------------------------------------------------------------------------------
SPIDER = "scrapy crawl token_auth_spider"
STARTLIST = '<!-- FRIENDS -->'
ENDLIST = '<!-- ONLINE LIST -->'

def playerParser(hList, tList):
    path = os.path.join(os.getcwd(), 'source.html')
    with open(path, 'r', encoding='utf-8') as html:
        page = html.read()
        page = page.split(hList)[1]
        page = page.split(tList)[0]

    soup = BeautifulSoup(page, 'html.parser')
    buttons = soup.find_all('button', attrs={'data-chat-nickname-param': True})
    nicknames = [btn['data-chat-nickname-param'].lower() for btn in buttons]
    return nicknames

#----------------------------------------------------------------------------------
def str(onlinePlayers):
    message = "Online Players:\n"
    for i, player in enumerate(onlinePlayers):
        message += f"{i + 1}. {player}\n"
    print(message)
    return message

def sendMessage(message):
    async def send_message(message):
        bot = Bot(os.getenv('TG'))
        await bot.send_message(os.getenv('CHAT'), message)
    asyncio.run(send_message(message))
    
#----------------------------------------------------------------------------------
def process():
    startSpider()
    friends = playerParser(STARTLIST, ENDLIST)
    if friends:
        sendMessage(str(friends))
    
if __name__ == '__main__':
    try:
        process()
    except FileNotFoundError:
        sendMessage("Restarting process")
        process()
    except Exception as e:
        sendMessage(f"Failed by: {e}")
    finally:
        sys.exit(0)
