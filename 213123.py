import telebot
from telebot import types
import sqlite3


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
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = ['Об отеле:','📞 Написать нам:','Где мы находимся:', 'Категории номеров:','Завтраки', 'Контакты:',  'FAQ(Часто задаваемые вопросы)',  ]
    keyboard.add(*[types.KeyboardButton(button) for button in buttons])
    bot.send_message(message.chat.id, 'Для продолжения нажмите любую кнопку:', reply_markup=keyboard)
    

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в отель «EVA»')
    bot.send_message(message.chat.id, 'Я — чат-бот отеля «EVA» в Перми. Я могу предоставить всю необходимую информацию об отеле — воспользуйтесь кнопками ниже:')
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    send_keyboard(message)

    db_table_val(user_id=user_id, user_name=user_name, user_surname=user_surname, username=username)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    send_keyboard(message)
    if message.text == 'Об отеле:':
        bot.send_message(message.chat.id, '\nОтель «EVA» - один из лучших мини-отелей города Пермь, который уделяет особое внимание комфорту гостей.\n\nВ отеле 10 просторных номера площадь от 18 до 22 кв.м., от одноместных и двухместных номеров «Комфорт» и «Бизнес» до семейных.\nКаждый номер можно дополнить детской кроваткой.\n\nМы рады вам каждый день 💞')
        photos = [
        'https://i.imgur.com/ORwCXrS.jpeg',
        'https://eva-hotel.ru/wp-content/uploads/DSC00871-2-683x1024.jpg',
        'https://i.imgur.com/4cMEoXp.jpeg',
        'https://i.imgur.com/UDo3GxT.jpeg',
        'https://i.imgur.com/WZBPX7R.jpeg'
        ]
        media = [telebot.types.InputMediaPhoto(photos[i]) for i in range(5)]
        bot.send_media_group(message.chat.id, media)

    
    
    elif message.text == 'Категории номеров:':
      keyboard = types.InlineKeyboardMarkup()
      comfort_button = types.InlineKeyboardButton(text='Комфорт', callback_data='comfort')
      semeyniy_button = types.InlineKeyboardButton(text='Семейный', callback_data='semeyniy')
      business_button = types.InlineKeyboardButton(text='Бизнес', callback_data='business')
      keyboard.add(comfort_button, business_button, semeyniy_button)
      bot.send_message(message.chat.id, 'Выберите категорию номера:', reply_markup=keyboard)
    
    
    elif message.text == '📞 Написать нам:':
        bot.send_message(message.chat.id, 'Вы перешли в чат с @EVA_Hotel_Perm 😊')
        chat_id = '5216025312'  # Имя пользователя (username) для перехода в чат
        try:
            bot.send_message(chat_id, f'Пользователь {message.from_user.first_name} @{message.from_user.username} хочет связаться с вами. Пожалуйста, напишите ему первым.')
        except Exception as e:
            bot.send_message(message.chat.id, 'Не удалось отправить сообщение. Владелец чата не найден. Попробуйте позже.')
    
    elif message.text == 'Контакты:':
        bot.send_message(message.chat.id, '\nВы можете  связаться с нами любым удобным способом:\n\n🔔на нашем сайте: https://eva-hotel.ru/, \n📞 по телефону: +7 (342) 212-58-58    (служба бронирования) \n📱+7 (992) 212-58-58 (Viber, WhatsApp)\n🔔Telegram-@EVA_Hotel_Perm \n📩 по почте: reception@eva-hotel.ru')
    
    
    elif message.text == 'Где мы находимся:':
        keyboard = types.InlineKeyboardMarkup()
        adress_button = types.InlineKeyboardButton(text='Схема проезда:', callback_data='adress')
        keyboard.add(adress_button)
        bot.send_message(message.chat.id, '614000, г. Пермь, ул. Пермская 63/1', reply_markup=keyboard)
        
        

    elif message.text == 'FAQ(Часто задаваемые вопросы)':
      keyboard = types.InlineKeyboardMarkup()
      rules_button = types.InlineKeyboardButton(text='Правила заезда и выезда', callback_data='rules')
      stirka_button = types.InlineKeyboardButton(text='Стирка/глажка', callback_data='stirka')
      transfer_button = types.InlineKeyboardButton(text='Трансфер', callback_data='transfer')
      keyboard.add(rules_button, stirka_button, transfer_button)
      bot.send_message(message.chat.id, 'Часто задаваемые вопросы:', reply_markup=keyboard)

    elif message.text == 'Завтраки':
        bot.send_message(message.chat.id, 'Завтраки проходят в формате Room-service ежедневно с 07:00-12:00.\nГости выбирают завтрак по меню и удобное время подачи.\nТакже для гостей выезжающих ночью доступен вариант ночного завтрака/ланч бокс с собой. ' )
        bot.send_photo(message.chat.id,'https://s.101hotelscdn.ru/uploads/image/hotel_image/310/4939727.jpg')
        bot.send_photo(message.chat.id, 'https://eva-hotel.ru/wp-content/uploads/302537831-1.jpg')
        keyboard = types.InlineKeyboardMarkup()
        zavtrak_button= types.InlineKeyboardButton(text='клик', callback_data='zavtrak')
        keyboard.add(zavtrak_button)
        bot.send_message(message.chat.id, 'Меню:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'comfort':
        bot.send_message(call.message.chat.id, '\nВсего в отеле 5 номеров категории «Комфорт», которые включают:\n▪️ Завтрак\n▪️ Двухместную кровать (Twin)\n▪️ Кондиционер\n▪️ Обогреватель (при необходимости)\n▪️ Банные принадлежности (халат, тапочки, полотенца)\n▪️ Ванная комната с душевой кабиной\n▪️ Туалетно-косметические принадлежности\n▪️ Фен\n▪️ Телевизор\n▪️ Телефон\n▪️ Мини- холодильник\n▪️ Сейфовые ячейки для хранения личных вещей\n▪️ Охраняемая парковка автомобиля \n▪️ Ежедневная уборка номера\n▪️ Круглосуточная работа стойки регистрации\n▪️ Возможность размещения детей в возрасте до 7 лет на имеющейся кровати')
        photocomf = [
            'https://i.imgur.com/2F16qvM.jpeg',
            'https://reservationsteps.ru/files/a3/9d/a39dab9322fcc73823c588470ebee6dd_1050x600.jpg',
            'https://i.imgur.com/gPEOjH5.jpeg',
            'https://i.imgur.com/LhgmtQI.jpeg',
            'https://reservationsteps.ru/files/05/28/0528b3dc91ae125c52df00ee615c349c_1050x600.jpg',
        ]
        mediacomf = [telebot.types.InputMediaPhoto(photocomf[i]) for i in range(5)]
        bot.send_media_group(call.message.chat.id, mediacomf)
    elif call.data == 'business':
        bot.send_message(call.message.chat.id, '\nВсего в отеле 5 номеров категории «Бизнес», которые включают:\n▪️ Завтрак\n▪️ Покрытие Wi-Fi на территории отеля\n▪️ Двухместная кровать\n▪️ Рабочее пространство\n▪️ Кондиционер\n▪️ Обогреватель (при необходимости)\n▪️ Банные принадлежности (халат, тапочки, полотенца)\n▪️ Ванная комната с душевой кабиной\n▪️ Туалетно-косметические принадлежности\n▪️ Фен\n▪️ Телевизор (SMART ТВ)\n▪️ Телефон\n▪️ Мини- холодильник\n▪️ Доставка свежей прессы\n▪️ Сейфовые ячейки для хранения личных вещей\n▪️ Охраняемая парковка автомобиля (по предварительной заявке)\n▪️ Ежедневная уборка номера\n▪️ Круглосуточная работа стойки регистрации\n▪️ Услуга «мобильный офис» (сканирование и распечатка документов по запросу)\n▪️ Кроватка для ребенка до 3-х лет (по предварительному запросу)')
        photobiz = [
            'https://i.imgur.com/Bbf9PCK.jpeg',
            'https://i.imgur.com/rp5tjOB.jpeg',
            'https://i.imgur.com/fOLFVZ5.jpeg',
            'https://i.imgur.com/rtdQVP3.jpeg',
            'https://i.imgur.com/oXSIQjf.jpeg',
            'https://i.imgur.com/GKcU9N1.jpeg',
        ]
        mediabiz = [telebot.types.InputMediaPhoto(photobiz[i]) for i in range(6)]
        bot.send_media_group(call.message.chat.id, mediabiz)
    elif call.data == 'rules':
        bot.send_message(call.message.chat.id, '\nРегистрация заезда с 14:00.\n\nДоплата за ранний заезд с 09:01 до 13:59 (почасовая) составляет 300 руб/час.\n\nДоплата за поздний выезд с 12:01 до 16:59 (почасовая) составляет 300 руб/час.\n\nДоплата за ранний заезд ранее 09:00  составляет 50% стоимости проживания за сутки.\n\nДоплата за поздний выезд  после 17:00 составляет 50% стоимости проживания за сутки.\n\nДополнительное размещение 1000 руб/сутки.\n\nРегистрация отъезда до 12:00.\n\nПри размещении всех детей  младше 7 лет на имеющихся кроватях проживание им предоставляется бесплатно.')
    elif call.data == 'parking':
        bot.send_message(call.message.chat.id, 'На территории гостиницы расположена охраняемая парковка. Вы сможете воспользоваться ее услугами в любой момент абсолютно бесплатно.')
        bot.send_photo(call.message.chat.id, 'https://eva-hotel.ru/wp-content/uploads/image-14-02-24-05-30-1-2-1-560x560.jpeg')
    elif call.data == 'stirka':
        bot.send_message(call.message.chat.id, 'Мы будем рады избавить Вас от хлопот и сэкономить Ваше время.\nВ отеле имеется гладильный уголок,  где вы сможете самостоятельно воспользоваться утюгом и гладильной доской (услуга предоставляется бесплатно).\nУслуги прачечной предоставляются за дополнительную плату.')
    elif call.data == 'transfer':
        bot.send_message(call.message.chat.id, 'Для Вашего максимального удобства, мы можем организовать  трансфер.\nК Вашим услугам – автомобиль и водитель, который встретит Вас в аэропорту или на ж/д вокзале и доставит в гостиницу.\nСтоимость трансфера:\n800 рублей с ЖД Вокзала.\n1200 рублей с аэропорта.')
    elif call.data == 'adress':
        bot.send_message(call.message.chat.id, 'Обращаем Ваше внимание, что основной Въезд на парковку находится со стороны ул. Ленина (между домами 54 и 52)')
        bot.send_photo(call.message.chat.id, 'https://eva-hotel.ru/wp-content/uploads/4763-1024x683.jpg')
        bot.send_location(call.message.chat.id, 58.011385, 56.240717)

        keyboard = types.InlineKeyboardMarkup()
        parking_button = types.InlineKeyboardButton(text='Информация о парковке', callback_data='parking')
        keyboard.add(parking_button)

        bot.send_message(call.message.chat.id, 'Дополнительная информация о парковке:', reply_markup=keyboard)

    elif call.data == 'semeyniy':
        bot.send_message(call.message.chat.id, '\nСемейный номер представляет собой – два смежных номера, общей площадью – 40 м2. С двумя комнатами, в каждой из которых: собственная ванная с душевой кабиной и туалетно-косметическими принадлежностями, двуспальная кровать/2 односпальных кровати, телевизор, письменный стол, мини холодильник, Wi-Fi, кондиционер, сейф.\n\nВсего в отеле 1 номер данной категории.')
        bot.send_message(call.message.chat.id, '\nБесплатно:\n ▪️ Покрытие Wi-Fi на территории отеля\n ▪️ 1 двуспальная кровать, 2 односпальные кровати\n ▪️ Рабочее пространство\n ▪️ Электрический чайник и чайная пара (по запросу у администратора) \n ▪️ Кондиционер в каждой комнате\n ▪️ Обогреватель (при необходимости)\n ▪️ Банные принадлежности (халат, тапочки, полотенца)\n ▪️ Ванная комната с душевой кабиной\n ▪️ Туалетно-косметические принадлежности\n ▪️ Фен\n ▪️ Телевизор (SMART ТВ)\n ▪️ Телефон\n ▪️ 2 Мини- холодильника\n ▪️ Доставка свежей прессы\n ▪️ 2 сейфовые ячейки для хранения личных вещей\n ▪️ Охраняемая парковка автомобиля (по предварительной заявке)\n ▪️ Ежедневная уборка номера\n ▪️ Круглосуточная работа стойки регистрации\n ▪️ Услуга «мобильный офис» (сканирование и распечатка документов по запросу)\n ▪️ Детская кроватка для ребенка до 3-х лет (по предварительному запросу)')
        photosem = [
            'https://i.imgur.com/kZ8ctSq.jpeg',
            'https://i.imgur.com/rvQgUvv.jpeg',
            'https://i.imgur.com/UQ5rbvQ.jpeg',
            'https://i.imgur.com/Bwrooiz.jpeg',
            'https://reservationsteps.ru/files/32/c8/32c8a51f1ed3303c807a045946d8a28c_1050x600.jpg'
        ]
        mediasem = [telebot.types.InputMediaPhoto(photosem[i]) for i in range(5)]
        bot.send_media_group(call.message.chat.id, mediasem)
    elif call.data == 'zavtrak':
        bot.send_photo(call.message.chat.id, 'https://i.imgur.com/rFtPMhz.png')
bot.polling(none_stop=True)