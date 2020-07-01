from telebot import types
import psycopg2

main_message="""
    Добро пожаловать в Glosi, сообщество специалистов, готовых мгновенно решить любое ваше задание. Сталкиваетесь с делами, в которых не разбираетесь или на которые у вас не хватает времени.

Реши свою проблему уже сейчас, оставив заявку, исполнители сами напишут вам.

    """
work_message="""
    Добро пожаловать в Glosi. Ты специалист, и тебе нужны клиенты? Наш бот поможет тебе.
Оставь лишь раз свои данные и ежедневно получай заявки. 
И, так как наш бот только выходит на рынок, для новых специалистов он полностью бесплатен.

Скорее регистрируйся и получай новые заявки.
    """
ab=['Юридические услуги','Бухгалтерские услуги💰','Брокерские услуги📈']

def get_categoryes():
    markup=types.InlineKeyboardMarkup()
    for i in ab:
        markup.add(types.InlineKeyboardButton(text=i,callback_data=i+'category'))
    return markup
def get_cat():
    markup=types.ReplyKeyboardMarkup()
    for i in ab:
        markup.add(types.InlineKeyboardButton(i))
    return markup
def sql_query(sql):
    f=''
    try:
        conn = psycopg2.connect(dbname='dbl897lkr3kqj0', user='gyvyzqvrydwlxe', 
                                password='44826dd7802986c134535b8c9724edbe06185e69c372d144a0f554ad59bdf040', host='ec2-79-125-26-232.eu-west-1.compute.amazonaws.com')
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(sql)
        f=cur.fetchall()
        conn.close()
    except Exception as e:
        print (e)
    try:
        conn.close()
    except:
        print()
    return f
