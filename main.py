import asyncio, sys, os
from bs4 import BeautifulSoup
from telegram import Bot
from scrapy.crawler import CrawlerProcess
from pleazgg.spiders.spider import TokenAuthSpider

#-----------------------------------------------------------------------------------
SPIDER = "scrapy crawl token_auth_spider"
STARTLIST = '<!-- FRIENDS -->'
ENDLIST = '<!-- ONLINE LIST -->'

def startSpider():
    process = CrawlerProcess()
    process.crawl(TokenAuthSpider)
    process.start()

def playerParser(hList, tList):
    path = os.path.join(os.getcwd(), 'source.html')
    with open(path, 'r', encoding='utf-8') as html:
        page = html.read()
        page = page.split(hList)[1]
        page = page.split(tList)[0]

    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find_all('button', attrs={'data-chat-nickname-param': True})
    return [attribute['data-chat-nickname-param'].lower() for attribute in div]

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
