import asyncio, sys, os
from bs4 import BeautifulSoup
from telegram import Bot
from scrapy.crawler import CrawlerProcess
from pleazgg.spiders.spider import TokenAuthSpider

#------------------------------------------------------------------------------------
STARTLIST = '<div class="w-100 m-0 mt-2" data-chat-target="playersList">'
ENDLIST = '<div style="display: none;" data-chat-target="playersBlocksListArea">'
STARTFRIEND = '<div class="w-100 m-0 mt-2" data-chat-target="playersFriendsList">'
ENDFRIEND = '<div class="w-100 m-0 mt-2" data-chat-target="playersList">'
SPIDER = "scrapy crawl token_auth_spider"

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
    div = soup.find_all('div', attrs={'data-player-nickname': True})
    return [attribute['data-player-nickname'].lower() for attribute in div]

def searchPlayers(onlinePlayers):
    target = ['paolino885', 'jefsimons', 'ben201', 'dbn3', 'hehehe16', 'uberpapst', 'aster02', 'txxxm15',
                'psico', 'quartlast', 'charlie74', 'sam987654', 'asher14', 'random146435']

    subPlayers = []
    for nickname in onlinePlayers:
        if nickname in target:
            subPlayers.append(nickname)

    message = ""
    if subPlayers:
        message = "Online Players:\n"
        for i, nickname in enumerate(subPlayers):
            message += f"{i+1}. {nickname}\n"
        
    return message

#------------------------------------------------------------------------------------

def sendMessage(message):
    async def send_message(message):
        bot = Bot(os.getenv('TG'))
        await bot.send_message(os.getenv('CHAT'), message)
    asyncio.run(send_message(message))

def process():
    startSpider()
    onlinePlayers = playerParser(STARTLIST, ENDLIST)
    message = searchPlayers(onlinePlayers)
    friends = playerParser(STARTFRIEND, ENDFRIEND)
    if friends:
        message += f"\nFriends:\n{friends}"
    
    if message:
        sendMessage(message)
    
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
