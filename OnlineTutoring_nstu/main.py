import telebot
from telebot import types
from text import main_text
import sqlite3

token = ''
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == 777759367:
        db = sqlite3.connect("TutorsNstu.db")
        cursor = db.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS tutors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tg INTEGER UNIQUE,
            status INTEGER DEFAULT 0
            )""")
            db.commit()
            cursor.execute(f"INSERT INTO tutors (id_tg) VALUES ({message.chat.id})")
            db.commit()
            cursor.close()
            db.close()
            bot.send_message(message.chat.id,
                             '<code>Привет</code>! Рады, что готов/-а помочь 😊 Напиши <b>!вход</b>, чтобы выйти на смену и получать новых учеников, которым нужна помощь 🤯',
                             parse_mode='html')
            bot.register_next_step_handler(message, entry)
        except sqlite3.IntegrityError:
            cursor.close()
            db.close()
            bot.send_message(message.chat.id,
                             '<code>Привет</code>! Рады, что готов/-а помочь 😊 Напиши <b>!вход</b>, чтобы выйти на смену и получать новых учеников, которым нужна помощь 🤯',
                             parse_mode='html')
            bot.register_next_step_handler(message, entry)
    else:
        db = sqlite3.connect("StudentsNstu.db")
        cursor = db.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tg INTEGER UNIQUE,
            name VARCHAR,
            surname VARCHAR,
            number_curs INTEGER
            )""")
            db.commit()
            cursor.execute(f"INSERT INTO students (id_tg) VALUES ({message.chat.id})")
            db.commit()
            markup = types.InlineKeyboardMarkup()
            bt_1 = types.InlineKeyboardButton('Готов(a)', callback_data='ready_now')
            markup.add(bt_1)
            bot.send_message(message.chat.id, f'{main_text}', reply_markup=markup, parse_mode='html')
            cursor.close()
            db.close()
        except sqlite3.IntegrityError:
            cursor.close()
            db.close()
            bot.send_message(message.chat.id, 'Введи своё <b>имя</b> 💬', parse_mode='html')
            bot.register_next_step_handler(message, register)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'ready_now':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Регистрация', callback_data='registration')
        markup.add(bt_1)
        bot.send_message(call.message.chat.id,
                         '<code>Отлично</code>! Рады, что ты заинтересован/-а в этом 😉 Сейчас мы тебя <b>зарегистрируем</b> 👨🏻‍💻',
                         reply_markup=markup, parse_mode='html')
    elif call.data == 'registration':
        bot.send_message(call.message.chat.id, 'Введи своё <b>имя</b> 💬', parse_mode='html')
        bot.register_next_step_handler(call.message, register)
    elif call.data == 'replace':
        bot.send_message(call.message.chat.id,
                         '<code>Сейчас заново тебя зарегистрируем</code> 📝\nВведи своё <b>имя</b> 💬',
                         parse_mode='html')
        bot.register_next_step_handler(call.message, register)
    elif call.data == 'good':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('1', callback_data='one')
        bt_2 = types.InlineKeyboardButton('2', callback_data='two')
        markup.add(bt_1, bt_2)
        bot.send_message(call.message, '<code>Данные сохранены</code> ✅\nВыбери <b>курс</b> 1️⃣ 2️⃣', parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'one':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Матанализ', callback_data='matanaliz_one')
        bt_2 = types.InlineKeyboardButton('Линал', callback_data='linal_one')
        markup.add(bt_1, bt_2)
        bot.send_message(call.message, 'Выбери <b>предмет</b> 👇', parse_mode='html', reply_markup=markup)
    elif call.data == 'two':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Матанализ', callback_data='matanaliz_two')
        bt_2 = types.InlineKeyboardButton('Линал', callback_data='linal_two')
        markup.add(bt_1, bt_2)
        bot.send_message(call.message, 'Выбери <b>предмет</b> 👇', parse_mode='html', reply_markup=markup)
    elif call.data == 'matanaliz_one':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Конспекты', callback_data='synopsis_mat_one')
        bt_2 = types.InlineKeyboardButton('Вебинары', callback_data='vebs_mat_one')
        bt_3 = types.InlineKeyboardButton('Онлайн-помощь', callback_data='online_help')
        bt_4 = types.InlineKeyboardButton('Задачи', callback_data='tasks_mat_one')
        markup.add(bt_1, bt_2)
        markup.add(bt_3, bt_4)
        bot.send_message(call.message.chat.id, 'Выбери желаемую <b>помощь</b> 🆘', parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'linal_one':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Конспекты', callback_data='synopsis_linal_one')
        bt_2 = types.InlineKeyboardButton('Вебинары', callback_data='vebs_linal_one')
        bt_3 = types.InlineKeyboardButton('Онлайн-помощь', callback_data='online_help')
        bt_4 = types.InlineKeyboardButton('Задачи', callback_data='tasks_linal_one')
        markup.add(bt_1, bt_2)
        markup.add(bt_3, bt_4)
        bot.send_message(call.message.chat.id, 'Выбери желаемую <b>помощь</b> 🆘', parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'matanaliz_two':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Конспекты', callback_data='synopsis_mat_two')
        bt_2 = types.InlineKeyboardButton('Вебинары', callback_data='vebs_mat_two')
        bt_3 = types.InlineKeyboardButton('Онлайн-помощь', callback_data='online_help')
        bt_4 = types.InlineKeyboardButton('Задачи', callback_data='tasks_mat_two')
        markup.add(bt_1, bt_2)
        markup.add(bt_3, bt_4)
        bot.send_message(call.message.chat.id, 'Выбери желаемую <b>помощь</b> 🆘', parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'linal_two':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Конспекты', callback_data='synopsis_linal_two')
        bt_2 = types.InlineKeyboardButton('Вебинары', callback_data='vebs_linal_two')
        bt_3 = types.InlineKeyboardButton('Онлайн-помощь', callback_data='online_help')
        bt_4 = types.InlineKeyboardButton('Задачи', callback_data='tasks_linal_two')
        markup.add(bt_1, bt_2)
        markup.add(bt_3, bt_4)
        bot.send_message(call.message.chat.id, 'Выбери желаемую <b>помощь</b> 🆘', parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'synopsis_mat_one':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Функции', callback_data='funcs')
        bt_2 = types.InlineKeyboardButton('Пределы', callback_data='predels')
        markup.add(bt_1, bt_2)
        bt_3 = types.InlineKeyboardButton('Производная', callback_data='proizvod')
        bt_4 = types.InlineKeyboardButton('Интегралы', callback_data='integrals')
        markup.add(bt_3, bt_4)
        bot.send_message(call.message, 'Выбери нужную <b>тему</b> 👇', parse_mode='html', reply_markup=markup)
    elif call.data == 'synopsis_linal_one':
        markup = types.InlineKeyboardMarkup()
        bt_1 = types.InlineKeyboardButton('Матрицы', callback_data='matrix')
        bt_2 = types.InlineKeyboardButton('ФСУ', callback_data='fsy')
        markup.add(bt_1, bt_2)
        bt_3 = types.InlineKeyboardButton('Векторная алгебра', callback_data='vectors')
        bt_4 = types.InlineKeyboardButton('Линейные пространства и операторы', callback_data='linal_operator')
        markup.add(bt_3, bt_4)
        bt_5 = types.InlineKeyboardButton('Кривые второго порядка', callback_data='two_row')
        bt_6 = types.InlineKeyboardButton('Евклидово пространство', callback_data='evklid_space')
        markup.add(bt_5, bt_6)
        bot.send_message(call.message, 'Выбери нужную <b>тему</b> 👇', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['text'])
def register(message):
    name = message.text
    db = sqlite3.connect("StudentsNstu.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE students SET name = '{name}' WHERE id_tg = {message.chat.id}")
    db.commit()
    cursor.execute(f"SELECT name FROM students WHERE id_tg = {message.chat.id}")
    name_proverka = cursor.fetchone()[0]
    bot.send_message(message.chat.id,
                     f'<code>Принято</code> ✅\n\n<b>Имя</b>: <code>{name_proverka}</code>\nВведи свою <b>фамилию</b> 💬',
                     parse_mode='html')
    cursor.close()
    db.close()
    bot.register_next_step_handler(message, register_surname)


def register_surname(message):
    surname = message.text
    db = sqlite3.connect("StudentsNstu.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE students SET surname = '{surname}' WHERE id_tg = {message.chat.id}")
    db.commit()
    cursor.execute(f"SELECT surname FROM students WHERE id_tg = {message.chat.id}")
    surname_proverka = cursor.fetchone()[0]
    bot.send_message(message.chat.id,
                     f'<code>Принято</code> ✅\n\n<b>Фамилия</b>: <code>{surname_proverka}</code>\nВведи свой <b>курс</b> (цифру!!!) 💬',
                     parse_mode='html')
    cursor.close()
    db.close()
    bot.register_next_step_handler(message, register_curs)


def register_curs(message):
    curs = message.text
    db = sqlite3.connect("StudentsNstu.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE students SET number_curs = '{curs}' WHERE id_tg = {message.chat.id}")
    db.commit()
    cursor.execute(f"SELECT number_curs FROM students WHERE id_tg = {message.chat.id}")
    curs_proverka = cursor.fetchone()[0]
    bot.send_message(message.chat.id, f'<code>Принято</code> ✅\n\n<b>Курс</b>: <code>{curs_proverka}</code>',
                     parse_mode='html')
    cursor.execute(f"SELECT name, surname, number_curs FROM students WHERE id_tg = {message.chat.id}")
    proverka = cursor.fetchone()
    markup = types.InlineKeyboardMarkup()
    bt_1 = types.InlineKeyboardButton('Принять', callback_data='good')
    bt_2 = types.InlineKeyboardButton('Изменить', callback_data='replace')
    markup.add(bt_1, bt_2)
    bot.send_message(message.chat.id,
                     f'<code>Регистрация завершена успешно</code> ✅\n\n<b>Имя</b>: <code>{proverka[0]}</code>\n<b>Фамилия</b>: <code>{proverka[1]}</code>\n<b>Курс</b>: <code>{proverka[2]}</code>',
                     parse_mode='html', reply_markup=markup)
    cursor.close()
    db.close()


def entry(message):
    if message.text == '!вход':
        db = sqlite3.connect("TutorsNstu.db")
        cursor = db.cursor()
        cursor.execute(f"UPDATE tutors SET status = 1 WHERE id_tg = {message.chat.id}")
        db.commit()
        cursor.close()
        db.close()
        bot.send_message(message.chat.id,
                         '<b>Ты вышел/-а на смену</b>! Удачи 🍀\nДля выхода со смены необходимо ввести команду <b>!выход</b>',
                         parse_mode='html')
        bot.register_next_step_handler(message, exit)
    else:
        bot.send_message(message.chat.id, 'Неверная команда ❌ Для входа необходимо ввести команду <b>!вход</b>',
                         parse_mode='html')
        bot.register_next_step_handler(message, entry)


def exit(message):
    if message.text == '!выход':
        db = sqlite3.connect("TutorsNstu.db")
        cursor = db.cursor()
        cursor.execute(f"UPDATE tutors SET status = 0 WHERE id_tg = {message.chat.id}")
        db.commit()
        cursor.close()
        db.close()
        bot.send_message(message.chat.id,
                         '<b>Ты вышел/-а со смены</b>! До встречи 👋\nДля входа необходимо ввести команду <b>!вход</b>',
                         parse_mode='html')
        bot.register_next_step_handler(message, entry)
    else:
        bot.send_message(message.chat.id, 'Неверная команда ❌ Для выхода необходимо ввести команду <b>!выход</b>',
                         parse_mode='html')
        bot.register_next_step_handler(message, exit)


bot.infinity_polling()
