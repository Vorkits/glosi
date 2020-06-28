import telebot
from telebot import types
import psycopg2
import sqlite3
conn = sqlite3.connect("mydatabase.db")
bot = telebot.TeleBot('1123182125:AAGSp0qrIbpwo9Je4Lj-zAGA0OwsBq8S7jI')
w_bot = telebot.TeleBot('914404855:AAEoc0ye_05EMpMaD5m43kytpkPhOL54pHQ')
print('CCCCCLIIIIEEEENNNNTTTTccz')
import string
import random
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
users={}
zakazi={}
to_base=lambda s:"'"+str(s)+"'"
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

def reply_city():
    markup=types.ReplyKeyboardMarkup(one_time_keyboard = True)
    cities=['Алматы','Астана(Нур-Султан)','Караганда','Актау','Шымкент','Лругой']
    for i in cities:
        markup.add(i)
    return markup

def start_bot(config):
    def showcategory(message):
        bot.send_message(message.from_user.id,' ',reply_markup=config.get_categoryes())
    @bot.message_handler(commands=['start'])
    def start_message(message):
        mes=config.main_message
        reply=types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply.add('Оставить заявку-')
        bot.send_message(message.from_user.id, mes,reply_markup=reply)
    @bot.message_handler(content_types=['text'])
    def text(message):
        def city_finish(message):
            users[message.from_user.username]['city']=message.text
            sql_query('INSERT INTO users (name,phone,city,username,tid) VALUES ({},{},{},{},{})'.format(to_base(users[message.from_user.username]['name']),to_base(users[message.from_user.username]['phone']),to_base(users[message.from_user.username]['city']),to_base(message.from_user.username),to_base(message.from_user.id)))
            mes='Теперь вы можете выбрать категорию в которой вам нужно получить услугу🛠'
            users.pop(message.from_user.username,1)
            m=bot.send_message(message.from_user.id, mes,reply_markup=config.get_categoryes())
        def phone_city(message):
            users[message.from_user.username]['phone']=message.text
            mes='Спасибо, теперь выбери свой город из предложенных ниже🔽'
            # инструкция
            m=bot.send_message(message.from_user.id, mes,reply_markup=reply_city())
            bot.register_next_step_handler(m,city_finish)
        def name_phone(message):
            users[message.from_user.username]={
                'name':message.text,
                'phone':'',
                'city':''
                
            }
            mes='Приятно познакомиться, {}. Отправь мне свой номер телефона.\n(если вы не хотите, чтобы исполнители связывались с вами по номеру телефона, оставьте поле пустым)'.format(message.text)
            m=bot.send_message(message.from_user.id, mes,reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(m,phone_city)
        if message.text=='Оставить заявку-':
            mes='Введите свое имя'
            print(message)
            m=bot.send_message(message.from_user.id, mes,reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(m,name_phone)
        
    @bot.callback_query_handler(func = lambda call: True) 
    def add(message):
        def price_finish(message):
            zakazi[message.from_user.username]['price']=message.text
            mes="""Ваша заявка-{}
Цена-{}
Категория-{}""".format(zakazi[message.from_user.username]['description'],zakazi[message.from_user.username]['price'],zakazi[message.from_user.username]['category'])
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Разместить заявку',callback_data='plae'))

            markup.add(types.InlineKeyboardButton(text='Отмена❌',callback_data='otmena'))
            f=bot.send_message(message.from_user.id,mes,reply_markup=markup)

        def desc_price(message):
            zakazi[message.from_user.username]['description']=message.text
            f=bot.send_message(message.from_user.id,'Напишите,сколько вы готовы за это заплатить.💰(если вы не знаете, отправьте "-")')
            bot.register_next_step_handler(f,price_finish)
        if 'change personal' in message.data:
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Изменить номер телефона',callback_data='changes,phone'))
            markup.add(types.InlineKeyboardButton(text='Изменить имя',callback_data='changes,name')) 
            markup.add(types.InlineKeyboardButton(text='Изменить город',callback_data='changes,city'))
            f=bot.send_message(message.from_user.id,'Что вы хотите изменить? Нажмите на соответствуюущую кнопку🔽',reply_markup=markup)
        if 'changes' in message.data:
            def change_data(message,do):
                try:
                    sql_query('UPDATE users SET {}={} WHERE tid={} '.format(do,to_base(message.text),to_base(message.from_user.id)))
                    markup=types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton(text='Разместить заявку еще раз',callback_data='place order'))
                    markup.add(types.InlineKeyboardButton(text='Изменить личные данные',callback_data='change personal')) 
                    bot.send_message(message.from_user.id,'Успешно',reply_markup=markup)
                except Exception as e:
                    print(e)
            f=False
            do=message.data.split(',')[1]
            if do=='city':
                f=bot.send_message(message.from_user.id,'Выбери свой город ниже🔽',reply_markup=reply_city())
            else:
                
                rep={
                    'name':'Свое имя',
                    'phone':'Свой номер'
                }
                f=bot.send_message(message.from_user.id,'Напиши мне {} '.format(rep[do]),reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(f,lambda message:change_data(message,do))

        if 'category' in message.data:
            cat=message.data.replace('category','')
            zakazi[message.from_user.username]={'category':cat,'price':'','description':''}
            f=bot.send_message(message.from_user.id,'Опишите, какая вам нужна услуга🛠',reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(f,desc_price)
        if 'place order' in message.data:
            mes='Выберите категорию в которой вам нужно получить услугу🔽'
            # инструкция
            m=bot.send_message(message.from_user.id, mes,reply_markup=config.get_categoryes())
        if 'otmena' in message.data:
            mes='Заявка отменена, чтобы разместить ее снова, нажмите кнопку ниже🔽'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Разместить заявку еще раз',callback_data='place order'))
            markup.add(types.InlineKeyboardButton(text='Изменить личные данные',callback_data='change personal')) 
            f=bot.send_message(message.from_user.id,mes,reply_markup=markup)
        if 'plae' in message.data and message.from_user.username in zakazi:
            mes='Заявка отправленна исполнителям, они в кратчайшее время свяжутся с вами.\nСпасибо что выбрали нас!'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Разместить заявку еще раз',callback_data='place order'))
            markup.add(types.InlineKeyboardButton(text='Изменить личные данные',callback_data='change personal')) 

            f=bot.send_message(message.from_user.id,mes,reply_markup=markup)
            sq=sql_query('SELECT city,name,phone from users WHERE tid={}'.format(to_base(message.from_user.id)))
            city=sq[0][0]
            name=sq[0][1]
            phone=sq[0][2]
            sq=sql_query('SELECT tid from workers WHERE category={}'.format(to_base(zakazi[message.from_user.username]['category'])))
            rstr=id_generator()
            markup=types.InlineKeyboardMarkup(types.InlineKeyboardButton(text='Просмотреть контакты',callback_data='show,{}'.format(rstr)))
            print(sq)
            data='{},{},{},{}'.format(city,name,phone,message.from_user.id)
            sql_query("""INSERT INTO orders VALUES({},{},{},{})""".format(to_base(rstr),to_base(message.from_user.id),to_base('{}'),to_base(data)))
            markup.add(types.InlineKeyboardButton(text='Просмотреть контакты',callback_data=''))
            print('show{},{},{},{}'.format(city,name,phone,message.from_user.id))
            mes="""
            Новая заявка
            
Описание-{}
Предложенная стоимость-{}
Город-{}""".format(to_base(zakazi[message.from_user.username]['description']),to_base(zakazi[message.from_user.username]['price']),to_base(city))
            used=[]
            for i in sq:
                
                id=i[0]
                if id not in used:
                    w_bot.send_message(id,mes,reply_markup=markup)
                used.append(id)
            zakazi.pop(message.from_user.username)
                
            


    bot.polling(none_stop=True)

  