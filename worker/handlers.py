import telebot
from telebot import types
import psycopg2
bot = telebot.TeleBot('914404855:AAEoc0ye_05EMpMaD5m43kytpkPhOL54pHQ')
users={}
zakazi={}
to_base=lambda s:"'"+str(s)+"'"
def reply_city():
    markup=types.ReplyKeyboardMarkup(one_time_keyboard = True)
    cities=['Алматы','Астана(Нур-Султан)','Караганда','Актау','Шымкент','Другой']
    for i in cities:
        markup.add(i)
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
        mes=config.work_message
        reply=types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply.add('Зарегистрироваться')
        bot.send_message(message.from_user.id, mes,reply_markup=reply)
    @bot.message_handler(content_types=['text'])
    def text(message):
        def city_finish(message):
            users[message.from_user.id]['city']=message.text
            # sql_query('INSERT INTO users (name,phone,city) VALUES ({},{},{})'.format(to_base(users[message.from_user.username]['name']),to_base(users[message.from_user.username]['phone']),to_base(users[message.from_user.username]['city'])))
            mes='Теперь вы можете выбрать категорию, по которой хотите получать заказы.'
            # users.pop(message.from_user.username,1)
            m=bot.send_message(message.from_user.id, mes,reply_markup=config.get_categoryes())
        def phone_city(message):
            users[message.from_user.id]['phone']=message.text
            mes='Спасибо, теперь выбери свой город из предложенных ниже🔽'
            # инструкция
            m=bot.send_message(message.from_user.id, mes,reply_markup=reply_city())
            bot.register_next_step_handler(m,city_finish)
        def name_phone(message):
            users[message.from_user.id]={
                'name':message.text,
                'phone':'',
                'city':'',
                'category':''
                
            }
            mes='Приятно познакомиться, {}. Отправь мне свой номер телефона.'.format(message.text)
            m=bot.send_message(message.from_user.id, mes,reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(m,phone_city)
        if message.text=='Зарегистрироваться':
            mes='Введите свое ФИО'
            print(message)
            m=bot.send_message(message.from_user.id, mes,reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(m,name_phone)
        
    @bot.callback_query_handler(func = lambda call: True) 
    def add(message):
#         def price_finish(message):
#             zakazi[message.from_user.username]['price']=message.text
#             mes="""Ваша заявка-{}
# Цена-{}
# Категория-{}""".format(zakazi[message.from_user.username]['description'],zakazi[message.from_user.username]['price'],zakazi[message.from_user.username]['category'])
#             markup=types.InlineKeyboardMarkup()
#             markup.add(types.InlineKeyboardButton(text='Разместить заявку',callback_data='{},{},{}'.format(zakazi[message.from_user.username]['description'],zakazi[message.from_user.username]['price'],zakazi[message.from_user.username]['category'])))

#             markup.add(types.InlineKeyboardButton(text='Отмена❌',callback_data='otmena'))
#             f=bot.send_message(message.from_user.id,mes,reply_markup=markup)

#         def desc_price(message):
#             zakazi[message.from_user.username]['description']=message.text
#             f=bot.send_message(message.from_user.id,'Напишите,сколько вы готовы за это заплатить.(если вы не знаете, отправьте "-")')
#             bot.register_next_step_handler(f,price_finish)

        if 'category' in message.data and message.from_user.id in users:
            cat=message.data.replace('category','')
            users[message.from_user.id]['category']=cat
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Согласен',callback_data='personal'))
            f=bot.send_message(message.from_user.id,'Согласны ли вы на обработку ваших персональных данных?',reply_markup=markup)
            
        if 'personal' in message.data and message.from_user.id in users :
            markup=types.InlineKeyboardMarkup()
            
            sql_query('INSERT INTO workers (name,phone,city,category,username,tid) VALUES ({},{},{},{},{},{})'.format(to_base(users[message.from_user.id]['name']),to_base(users[message.from_user.id]['phone']),to_base(users[message.from_user.id]['city']),to_base(users[message.from_user.id]['category']),to_base(message.from_user.id),to_base(message.from_user.id)))
            markup.add(types.InlineKeyboardButton(text='Изменить личные данные',callback_data='change data'))
            markup.add(types.InlineKeyboardButton(text='Наши соц-сети',callback_data='socset'))
            markup.add(types.InlineKeyboardButton(text='Оставить заявку',callback_data='ispo'))

            f=bot.send_message(message.from_user.id,'Подписка на наш сервис оформленна, в этот чат вам будут приходить заявки от клиентов. Изменить свои данные вы можете по кнопке ниже🔽',reply_markup=markup)
            users.pop(message.from_user.id,1)
            
        if 'socset' in message.data:
            mes='Текст с соц-сетями'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Изменить личные данные',callback_data='change data'))
            markup.add(types.InlineKeyboardButton(text='Наши соц-сети',callback_data='socset'))
            markup.add(types.InlineKeyboardButton(text='Оставить заявку',callback_data='ispo'))
            f=bot.send_message(message.from_user.id,mes,reply_markup=markup)
        if 'ispo' in message.data:
            mes='Чтобы стать исполнителем, напишите этуму боту- @Glosi_bot'
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Изменить личные данные',callback_data='change data'))
            markup.add(types.InlineKeyboardButton(text='Наши соц-сети',callback_data='socset'))
            markup.add(types.InlineKeyboardButton(text='Оставить заявку',callback_data='ispo'))
            f=bot.send_message(message.from_user.id,mes,reply_markup=markup)
            
        if 'show' in message.data :
            dat=message.data.replace('show','').split(',')[1]
            sq=sql_query('SELECT * FROM orders WHERE id={}'.format(to_base(dat)))
            sq=sq[0]
            data=sq[3].split(',')
            
            mes="""Имя-{}
Город-{}
Номер-{}
Ссылка на переписку-[Ссылка](tg://user?id={})
""".format(data[1],data[0],data[2],data[3])
            bot.send_message(message.from_user.id,mes,parse_mode="Markdown")
            sq=sql_query("""UPDATE orders SET workers = array_append(workers,{}) WHERE id={}""".format(to_base(message.from_user.id),to_base(dat)))

        # if 'place order' in message.data:
        #     mes='Выберите категорию в которой вам нужно получить услугу(смайлик)'
        #     # инструкция
        #     m=bot.send_message(message.from_user.id, mes,reply_markup=config.get_categoryes())
        # if 'otmena' in message.data:
        #     mes='Заявка отменена, чтобы разместить ее снова, нажмите кнопку ниже(смайлик)'
        #     markup=types.InlineKeyboardMarkup()
        #     markup.add(types.InlineKeyboardButton(text='Разместить заявку еще раз',callback_data='place order'))
        #     markup.add(types.InlineKeyboardButton(text='Изменить личные данные',callback_data='change personal')) 
        #     f=bot.send_message(message.from_user.id,mes,reply_markup=markup) 
            
        if 'change data' in message.data:
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Изменить номер телефона',callback_data='changes,phone'))
            markup.add(types.InlineKeyboardButton(text='Изменить имя',callback_data='changes,name')) 
            markup.add(types.InlineKeyboardButton(text='Изменить город',callback_data='changes,city'))
            markup.add(types.InlineKeyboardButton(text='Изменить категорию услуг',callback_data='changes,category'))

            f=bot.send_message(message.from_user.id,'Что вы хотите изменить? Нажмите на соответствуюущую кнопку🔽',reply_markup=markup)
        if 'changes' in message.data:
            def change_data(message,do):
                try:
                    sql_query('UPDATE workers SET {}={} WHERE tid={} '.format(do,to_base(message.text),to_base(message.from_user.id)))
                    bot.send_message(message.from_user.id,'Успешно',reply_markup=types.ReplyKeyboardRemove())
                except Exception as e:
                    print(e)
            f=False
            do=message.data.split(',')[1]
            if do=='city':
                f=bot.send_message(message.from_user.id,'Выбери свой город ниже🔽',reply_markup=reply_city())
            elif do=='category':
                f=bot.send_message(message.from_user.id,'Выбери категорию город ниже🔽',reply_markup=config.get_cat())

            else:
                
                rep={
                    'name':'Свое имя',
                    'phone':'Свой номер'
                }
                f=bot.send_message(message.from_user.id,'Напиши мне {} '.format(rep[do]),reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(f,lambda message:change_data(message,do))


    bot.polling(none_stop=True)

  