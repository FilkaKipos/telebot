import telebot
from telebot import types
import sqlite3
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

token = '6709073385:AAF-IVeh7I5sD4XCZpNBioZ5VLtpgN2FAwY'
bot = telebot.TeleBot(token)

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()

def check_user_in_db(user_id):
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()
    return existing_user is not None

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    if check_user_in_db(user_id):
        print(f"Пользователь с ID {user_id} уже присутствует в базе данных.")
    else:
        cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
        conn.commit()
        print(f"Пользователь с ID {user_id} успешно добавлен.")

def send_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = ['Об отеле:', 'Забронировать номер:', 'Категории номеров:', 'Связь с нами:', 'Где мы находимся:', 'FAQ(Часто задаваемые вопросы)']
    keyboard.add(*[types.KeyboardButton(button) for button in buttons])
    
    bot.send_message(message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в отель «EVA»')
    bot.send_message(message.chat.id, 'Я — чат-бот отеля «EVA» в Перми. Я могу предоставить всю необходимую информацию об отеле — воспользуйтесь кнопками ниже:')
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username

    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Об отеле:':
        bot.send_message(message.chat.id, '\nОтель «EVA» - один из лучших мини-отелей города Пермь, который уделяет особое внимание комфорту гостей.\n\nВ отеле 10 просторных номера площадь от 18 до 22 кв.м., от одноместных и двухместных номеров «Комфорт» и «Бизнес» до семейных.\nКаждый номер можно дополнить детской кроваткой.\n\nМы рады вам каждый день 💞')
        photos = [
        'https://eva-hotel.ru/wp-content/uploads/302537831-1.jpg',
        'https://eva-hotel.ru/wp-content/uploads/DSC00871-2-683x1024.jpg',
        'https://eva-hotel.ru/wp-content/uploads/151319674-1.jpg',
        'https://eva-hotel.ru/wp-content/uploads/279475052-2.jpg'
        ]
        media = [telebot.types.InputMediaPhoto(photos[i]) for i in range(4)]
        bot.send_media_group(message.chat.id, media)

    
    elif message.text == 'Забронировать номер:':
      bron_link = 'https://eva-hotel.ru/?page_id=262'
      bron_button = types.InlineKeyboardButton('Забронировать', url=bron_link)
      reply_markup = types.InlineKeyboardMarkup([[bron_button]])
      bot.send_message(message.chat.id, 'Для бронирования номера перейдите по ссылке:', reply_markup=reply_markup)
    
    
    elif message.text == 'Категории номеров:':
      keyboard = types.InlineKeyboardMarkup()
      comfort_button = types.InlineKeyboardButton(text='Комфорт', callback_data='comfort')
      business_button = types.InlineKeyboardButton(text='Бизнес', callback_data='business')
      keyboard.add(comfort_button, business_button)
      bot.send_message(message.chat.id, 'Выберите категорию номера:', reply_markup=keyboard)
    
    
    elif message.text == 'Связь с нами:':
        bot.send_message(message.chat.id, '\nВы можете  связаться с нами любым удобным способом:\n\n🔔на нашем сайте: https://eva-hotel.ru/, \n📞 по телефону: +7 (342) 212-58-58    (служба бронирования) \n📱+7 (992) 212-58-58 (Viber, WhatsApp)\n🔔Telegram-@EVA_Hotel_Perm \n📩 по почте: reception@eva-hotel.ru')
    
    
    elif message.text == 'Где мы находимся:':
        bot.send_message(message.chat.id, ' Обращаем Ваше внимание, что основной Въезд на парковку находится со стороны ул. Ленина (между домами 54 и 52)')
        bot.send_photo(message.chat.id, 'https://eva-hotel.ru/wp-content/uploads/4763-1024x683.jpg')
        bot.send_location(message.chat.id, 58.011385, 56.240717)

    elif message.text == 'FAQ(Часто задаваемые вопросы)':
      keyboard = types.InlineKeyboardMarkup()
      rules_button = types.InlineKeyboardButton(text='Правила заезда и выезда', callback_data='rules')
      parking_button = types.InlineKeyboardButton(text='Информация о парковке', callback_data='parking')
      stirka_button = types.InlineKeyboardButton(text='Стирка/глажка', callback_data='stirka')
      transfer_button = types.InlineKeyboardButton(text='Трансфер', callback_data='transfer')
      keyboard.add(rules_button, parking_button, stirka_button, transfer_button)
      bot.send_message(message.chat.id, 'Часто задаваемые вопросы:', reply_markup=keyboard)
        

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'comfort':
        bot.send_message(call.message.chat.id, '\nВсего в отеле 5 номеров категории «Комфорт», которые включают:\n Завтрак\n Двухместную кровать (Twin)\n Кондиционер\n Обогреватель (при необходимости)\n Банные принадлежности (халат, тапочки, полотенца)\n Ванная комната с душевой кабиной\n Туалетно-косметические принадлежности\n Фен\n Телевизор\n Телефон\n Мини- холодильник\n Сейфовые ячейки для хранения личных вещей\n Охраняемая парковка автомобиля \n Ежедневная уборка номера\n Круглосуточная работа стойки регистрации\n Возможность размещения детей в возрасте до 7 лет на имеющейся кровати')
    elif call.data == 'business':
        bot.send_message(call.message.chat.id, '\nВсего в отеле 5 номеров категории «Бизнес», которые включают:\n Завтрак\n Покрытие Wi-Fi на территории отеля\n Двухместная кровать\n Рабочее пространство\n Кондиционер\n Обогреватель (при необходимости)\n Банные принадлежности (халат, тапочки, полотенца)\n Ванная комната с душевой кабиной\n Туалетно-косметические принадлежности\n Фен\n Телевизор (SMART ТВ)\n Телефон\n Мини- холодильник\n Доставка свежей прессы\n Сейфовые ячейки для хранения личных вещей\n Охраняемая парковка автомобиля (по предварительной заявке)\n Ежедневная уборка номера\n Круглосуточная работа стойки регистрации\n Услуга «мобильный офис» (сканирование и распечатка документов по запросу)\n Кроватка для ребенка до 3-х лет (по предварительному запросу)')
    elif call.data == 'rules':
        bot.send_message(call.message.chat.id, '\nРегистрация заезда с 14:00.\n\nДоплата за ранний заезд с 09:01 до 13:59 (почасовая) составляет 200 руб/час.\n\nДоплата за поздний выезд с 12:01 до 16:59 (почасовая) составляет 200 руб/час.\n\nДоплата за ранний заезд ранее 09:00  составляет 50% стоимости проживания за сутки.\n\nДоплата за поздний выезд  после 17:00 составляет 50% стоимости проживания за сутки.\n\nДополнительное размещение 900 руб/сутки.\n\nРегистрация отъезда до 12:00.\n\nПри размещении всех детей  младше 7 лет на имеющихся кроватях проживание им предоставляется бесплатно.')
    elif call.data == 'parking':
        bot.send_message(call.message.chat.id, 'На территории гостиницы расположена охраняемая парковка. Вы сможете воспользоваться ее услугами в любой момент абсолютно бесплатно.')
        bot.send_photo(call.message.chat.id, 'https://eva-hotel.ru/wp-content/uploads/image-14-02-24-05-30-1-2-1-560x560.jpeg')
    elif call.data == 'stirka':
        bot.send_message(call.message.chat.id, 'Мы будем рады избавить Вас от хлопот и сэкономить Ваше время.\nВ отеле имеется гладильный уголок,  где вы сможете самостоятельно воспользоваться утюгом и гладильной доской (услуга предоставляется бесплатно).\nУслуги прачечной предоставляются за дополнительную плату.')
    elif call.data == 'transfer':
        bot.send_message(call.message.chat.id, 'Для Вашего максимального удобства, мы можем организовать  трансфер.\nК Вашим услугам – автомобиль и водитель, который встретит Вас в аэропорту или на ж/д вокзале и доставит в гостиницу.\nСтоимость трансфера:\n800 рублей с ЖД Вокзала.\n1200 рублей с аэропорта.')

# 1. Создание таблицы для отслеживания пользователей
def create_user_stats_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS user_stats (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, date TEXT)')
    conn.commit()

def create_user_stats_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS user_stats (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, date TEXT)')
    conn.commit()

def update_user_stats(user_id: int, date: str):
    cursor.execute('INSERT INTO user_stats (user_id, date) VALUES (?, ?)', (user_id, date))
    conn.commit()

def count_unique_users():
    cursor.execute('SELECT COUNT(DISTINCT user_id) FROM user_stats')
    count = cursor.fetchone()[0]
    return count

def send_daily_stats_to_user():
    chat_id = None
    for user in bot.get_chat_administrators('Ezhikpff'):
        if user.user.id:
            chat_id = user.user.id
            break

    if chat_id:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d')
        user_count = count_unique_users()
        stats_message = f"Статистика на {current_time}: Всего уникальных пользователей: {user_count}"
        bot.send_message(chat_id, stats_message)
    else:
        print("Пользователь @Ezhikpff не найден.")

scheduler = BackgroundScheduler(timezone='Europe/Moscow')
scheduler.add_job(send_daily_stats_to_user, 'cron', hour=19, minute=0, second=0)
scheduler.start()

create_user_stats_table()

bot.polling(none_stop=True)