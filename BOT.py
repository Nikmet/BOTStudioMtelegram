import telebot
from telebot import types, TeleBot

# Создаем бота и определяем токен
token = '5547330839:AAFtmoiFBZO3-ebLOQPpY6Vc2UCuwwFYFmA'
bot = telebot.TeleBot(token)


"""БЛОК ОПРЕДЕЛЕНИЯ КОМАНД"""
# Начальная команда (/start)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}, '
                                      f'приветствуем вас в нашем боте! Чтобы начать работу напишите /help')

# Команда основого меню помощи (/help)
@bot.message_handler(commands=['help'])
def help_quastion(message):
    markup_wcdb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=False)
    wcdb_button = types.KeyboardButton('Что умеет наш бот?')
    markup_wcdb.add(wcdb_button)
    bot.send_message(message.chat.id, 'Что я могу здесь узнать?', reply_markup=markup_wcdb)


"""БЛОК ОБРАБОТКИ ТЕКСТА"""
@bot.message_handler(content_types=['text'])
def text_hendler(message):
    if message.text.lower() == 'что умеет наш бот?':
        markup_help = types.InlineKeyboardMarkup()
        markup_help.row_width = 2
        markup_help.add(types.InlineKeyboardButton('Показать прайс-лист', callback_data='price'),
                        types.InlineKeyboardButton('Показать график работы', callback_data='schedule'))
        bot.send_message(message.chat.id, '<i><b>Вот что я умею:</b></i>', parse_mode='html', reply_markup=markup_help)

    #Меню для товаров
    elif message.text == 'Услуги':
        # Инлайн меню для услуг
        price_service_menu_markup = types.InlineKeyboardMarkup()
        price_service_menu_markup.row_width = 2
        price_take_photo = types.InlineKeyboardButton('Сфотографироваться (...)', callback_data='take_photo_price')
        price_service_menu_markup.add(price_take_photo)
        # Вызов меню
        bot.send_message(message.chat.id, '<i><b>На какие услуги вы хотели бы узнать цену?</b></i>',
                         parse_mode='html',
                         reply_markup=price_service_menu_markup)

    elif message.text == 'Товары':
        # Инлайн меню для товаров
        price_products_menu_markup = types.InlineKeyboardMarkup()
        price_products_menu_markup.row_width = 2
        price_printout = types.InlineKeyboardButton('Распечатать (...)', callback_data='printout_price')
        price_pictureframe = types.InlineKeyboardButton('Фото-Рамку', callback_data='pictureframe_price')
        price_products_menu_markup.add(price_printout, price_pictureframe)
        # Вызов меню
        bot.send_message(message.chat.id, '<i><b>На какие товары вы хотели бы узнать цену?</b></i>',
                         parse_mode='html',
                         reply_markup=price_products_menu_markup)


""""БЛОК ОБРАБОТКИ КНОПОК"""
@bot.callback_query_handler(func=lambda call: True)
def help_button_price(call):
    # Обработчик для кнопки "Показать прайс-лист"
    if call.data == 'price':

        #Создание менбшки выбора товаров или услуг
        price_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        service_button = types.KeyboardButton('Услуги')
        products_button = types.KeyboardButton('Товары')
        price_markup.add(service_button, products_button)
        bot.send_message(call.message.chat.id, '<i><b>На что вы бы хотели узнать цену?</b></i>',
                         parse_mode='html',
                         reply_markup=price_markup)

    # Обработчик для кнопки "Показать график работы"
    elif call.data == 'schedule':
        bot.send_message(call.message.chat.id, "График работы:\n"
                                               "ПН - С 8:30 ДО 17:00 \n"
                                               "ВТ - С 8:30 ДО 17:00 \n"
                                               "СР - С 8:30 ДО 17:00 \n"
                                               "ЧТ - С 8:30 ДО 17:00 \n"
                                               "ПТ - С 8:30 ДО 17:00 \n"
                                               "СБ - ВЫХОДНОЙ \n"
                                               "ВС - С 8:30 ДО 13:00 \n")

    # Обработчик для кнопки покупки фотографий
    elif call.data == 'printout_price':
        photo_markup = types.InlineKeyboardMarkup()
        photo_markup.row_width = 2
        photo_A2 = types.InlineKeyboardButton('A2 Фотография', callback_data='A2_photo')
        photo_A3 = types.InlineKeyboardButton('A3 Фотография', callback_data='A3_photo')
        photo_A4 = types.InlineKeyboardButton('A4 Фотография', callback_data='A4_photo')
        photo_A5 = types.InlineKeyboardButton('A5 Фотография', callback_data='A5_photo')
        photo_markup.add(photo_A2, photo_A3, photo_A4, photo_A5)
        bot.send_message(call.message.chat.id, 'Выберете какую фотографию вы хотите:', reply_markup=photo_markup)

    # Обработчик для кнопки покупки фоторамок
    elif call.data == 'pictureframe_price':
        pictureframe_markup = types.InlineKeyboardMarkup()
        pictureframe_markup.row_width = 2
        pictureframe_ready = types.InlineKeyboardButton('Готовая рамка', callback_data='ready_pictureframe')
        pictureframe_make = types.InlineKeyboardButton('Рамка на заказ', callback_data='make_pictureframe')
        pictureframe_markup.add(pictureframe_ready, pictureframe_make)
        bot.send_message(call.message.chat.id, 'Выберете какую фотографию вы хотите:', reply_markup=pictureframe_markup)


# Зацикливание бота
bot.polling(none_stop=True, interval=0)
