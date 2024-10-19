import asyncio, sys, os
from bs4 import BeautifulSoup
from telegram import Bot
from scrapy.crawler import CrawlerProcess
from pleazgg.spiders.spider import TokenAuthSpider

#------------------------------------------------------------------------------------
STARTLIST = '<div class="w-100 m-0 mt-2" data-chat-target="playersList">'
ENDLIST = '<div style="display: none;" data-chat-target="playersBlocksListArea">'
SPIDER = "scrapy crawl token_auth_spider"

def startSpider():
    process = CrawlerProcess()
    process.crawl(TokenAuthSpider)
    process.start()

def readHtml():
    path = os.path.join(os.getcwd(), 'source.html')
    with open(path, 'r', encoding='utf-8') as html:
        page = html.read()
        page = page.split(STARTLIST)[1]
        page = page.split(ENDLIST)[0]

    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find_all('div', attrs={'data-player-nickname': True})
    return [attribute['data-player-nickname'].lower() for attribute in div]

def searchPlayers(onlinePlayers):
    target = ['paolino885', 'jefsimons', 'ben201', 'dbn3', 'hehehe16', 'uberpapst', 
                'asther01', 'psico', 'quartlast', 'zenomullen', 'maark_02']

    subPlayers = []
    for nickname in onlinePlayers:
        if nickname in target:
            subPlayers.append(nickname)
    
    if subPlayers:
        message = "Online Players:\n"
        for i, nickname in enumerate(subPlayers):
            message += f"{i+1}. {nickname}\n"
    else:
        message = "No online Players"
        
    print(f"\n\nOUTPUT:\n{message}\n\n")
        
    return message

#------------------------------------------------------------------------------------
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHATID = os.getenv('CHAT_ID')

def sendMessage(message):
    async def send_message(message):
        bot = Bot(TOKEN)
        await bot.send_message(CHATID, message)
    asyncio.run(send_message(message))

if __name__ == '__main__':
#    try:
    startSpider()
    onlinePlayers = readHtml()
    message = searchPlayers(onlinePlayers)
    if message:
        sendMessage(message)
    else:
        print("No message")
    # except Exception as e:
    #     sendMessage(f"Failed by: {e}")
    # finally:
    #     sys.exit(0)