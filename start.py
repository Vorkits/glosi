import client.handlers as client
import worker.handlers as worker
import threading
from telebot import types
import telebot
import config as cf
print('stsart')
to_base=lambda s:"'"+str(s)+"'"
bot = telebot.TeleBot('1123182125:AAGSp0qrIbpwo9Je4Lj-zAGA0OwsBq8S7jI')

sql=cf.sql_query
def start():
    print('s1')
    worker.start_bot(cf)
def start2():
    print('s2')

    client.start_bot(cf)
def feedbacks():
    s=sql('SELECT * FROM orders WHERE used=0')
    for i in s:
        workers=set(i[2])
        names=[]
        for j in workers:
            name=sql("""SELECT name from workers where tid={}""".format(to_base(j)))
            if name:
                names.append(name[0][0]+'-'+j)
        print(i[1])
        markup=types.InlineKeyboardMarkup()
        for j in names:
            data=j.split('-')
            markup.add(types.InlineKeyboardButton(text=data[0],callback_data='feed-{}'.format(data[1])))
        markup.add(types.InlineKeyboardButton(text='Ни с кем из них',callback_data='feed-not'))
        bot.send_message(i[1],'Выберите исполнителя с которым вы начали работу,если хотите поставить отзыв ему.',reply_markup=markup)
    sql('UPDATE orders SET used=1 WHERE used=0')
t =  threading.Thread(target=start)
t.start()
b =  threading.Thread(target=start2)
b.start()
# c =  threading.Thread(target=feedbacks)
# c.start()

