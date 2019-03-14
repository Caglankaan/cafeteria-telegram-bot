from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bs4 import BeautifulSoup as BS
import urllib.request
import logging
from telegram.ext import Updater, CommandHandler
from time import gmtime, strftime

#check for new messages --> polling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#define a command callback function
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello, Welcome")

api_key = "777810566:AAH2lKomTZKIEAigvtUlYSoohxNiCy-HMPY"

updater = Updater(api_key, use_context=True)

#allows to register handler -> command, text, video, audio etc.
dispatcher = updater.dispatcher

#create a command handler
start_handler = CommandHandler("start",start)

#add command handler to dispatcher
dispatcher.add_handler(start_handler)

def yemekhane(update, context):
    date = strftime("%Y-%m-%d", gmtime())
    day = date.split('-')[1]
    month = date.split('-')[2]   
    year = date.split('-')[0]
    tarih = day+"."+month+"."+year
    page = "https://yks.iyte.edu.tr/yemekliste.aspx?tarih="+tarih+"&ogun=V"
    html = urllib.request.urlopen(page).read()
    soup = BS(html, features="lxml")
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id'))
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    string = f'1 - {data[0][0]}, kalori : {data[0][1]}\n2 - {data[1][0]}, kalori : {data[1][1]}\n3 - {data[2][0]}, kalori : {data[2][1]}\n4 - {data[3][0]}, kalori : {data[3][1]}\n'
    context.bot.send_message(chat_id = update.message.chat_id, text = string)
    

yemekhane_handler = CommandHandler("yemekhane",yemekhane)

dispatcher.add_handler(yemekhane_handler)

#start polling
updater.start_polling()

updater.idle()