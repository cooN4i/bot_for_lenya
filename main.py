import mysql.connector
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telebot.types import LabeledPrice
import psycopg2
import time
import config
from prompt import *
import MySQLdb
bot = telebot.TeleBot(TOKEN_BOT)




NATIONS = {"Белые": "white", "Европейцы": "european", "Черные": "black", "Латины": "latin",
                   "Русские": "russian",
                   "Австрийцы": "austrian", "Американцы": "american", "Арабы": "arab", "Армяне": "armenian",
                   "Белорусы": "belarusian", "Бразильцы": "brazilian", "Британцы": "british", "Румыны": "romanians",
                   "Татары": "tatar", "Турки": "turk", "Вьетнамцы": "vietnamese", "Греки": "greek",
                   "Грузины": "georgian", "Египтяне":"egyptian", "Испанцы":"spaniard", "Итальянцы":"italian",
                   "Казахи":"kazakhs","Китайцы":"chinese","Корейцы":"korean","Японцы":"japanese","Немцы":"german",
                   "Персы":"persian","Поляки":"pole","Португальцы":"portuguese","Украинцы":"ukrainians","Французы":"french",
                   "Чехи":"czech","Шведы":"swede"}

RACES = {"Человек":"human","Ангел":"angel","Демон":"demon","Рептилия":"reptile","Робот":"robot","Суккуб":"succubus",
             "Фея":"fairy","Фурри":"furry","Эльф":"elf"}



BODY = {"Накаченное":"muscular", "Пухлое":"plump", "Пышное":"busty", "Спортивное":"sporty", "Толстое":"fat", "Худое":"skinny"}


BOOBS = {"Огромная":"huge_b","Большая":"big_b", "Средняя":"medium-sized_b","Маленькая":"small_b","Натуральная":"natural_b"}

ASS = {"Огромные":"huge_a","Большие":"big_a", "Средние":"medium-sized_a","Маленькие":"small_a","Круглые":"round_a"}

LEGS = {"Толстые":"fat_l", "Пышные":"busty_l", "Спортивные":"sporty_l", "Худые":"skinny_l"}

HAIRCUT = {"Длинные":"long", "Средние":"middle-length","Короткие":"short","Коса":"braid","Каре":"bob","Хвост":"ponytail","Ирокез":"mohawk"}

HAIRCOLOR = {"Блонд":"blonde_h", "Брюнет(ка)":"brunette_h", "Рыжий":"orange_h", "Белый":"white_h", "Красный": "red_h", "Розовый":"pink_h", "Синий": "blue_h",
             "Желтый":"yellow_h", "Зеленый": "green_h", "Фиолетовый": "purple_h"}

EYESCOLOR = {"Зеленые":"green_e", "Карие":"brown_e", "Серые": "grey_e", "Голубые": "blue_e"}

CLOTHES = {"Голая(ый)": "naked", "Платье": "dress", "Хиджаб": "hijab", "Школьная форма": "school uniform",
           "Халат":"bathrobe", "Мини-юбка":"mini skirt", "Чулки":"cotton thick black stockings", "Купальник":"swimsuit",
           "Латексный костюм":"thick black latex suit", "Хеллоуин костюм":"halloween costume", "Корсет":"corset",
           "Античная одежда":"antique clothes"}

POSES = {"На четв.":"on all fours", "На спине":"lying on back", "На животе":"lying on stomach", "На боку":"on side",
         "Ползет":"crawl","Танцует":"dance","Лежит":"laying","Модельная":"model","Раздвинутые ноги":"spreaded legs",
         "В присяде":"squatting","Стоит":"standing","Йога":"yoga"}

AGES = {'18-24':'21_a', '25-30':'27_a', '31-40': '36_a', '41-50':'46_a','51-60':'56_a', '60+':'65_a'}


EMOTIONS = {"Ахегао":"ahegao", "Оргазм":"orgasm", "Хорни":"horny", "Счастье":"happy", "Улыбка":"smile", "Милая":"cute", "Грустная":"sad", "Плачущая":"crying", "Злая":"angry", "Серьезная":"serious"}

PLACES = {"Замок":"castle", "Река":"river", "Бар":"bar", "Ванная":"bathroom", "Пляж":"beach", "Кровать":"bed", "Автобус":"bus",
          "Кафе":"cafe", "Казино":"casino", "Пещера":"cave", "Церковь":"church", "Пустыня":"desert", "Лес":"forest",
          "Госпиталь":"hospital", "Кухня":"kitchen", "Горы":"mountains", "Праздник":"party", "Бассейн":"pool",
          "Ресторан":"restautant", "Сауна":"sauna", "Улица":"street", "Яхта":"yacht"}



PRICE_ONCE = LabeledPrice(label="Разовый платеж", amount=10*100)
PRICE_1_MONTH = LabeledPrice(label="1 месяц", amount=50*100)
PRICE_3_MONTH = LabeledPrice(label="3 месяца", amount=100*100)
PRICE_12_MONTH = LabeledPrice(label="12 месяцев", amount=400*100)


try:
    # пытаемся подключиться к базе данных
    conn = MySQLdb.connect(host="176.124.213.136", user="gen_user", passwd="#x*NP&6h\\\AGsY", db="default_db", port=3306)
#     conn = mysql.connector.connect(user='coon4i', password='OVERPLANET',
#                                    host='coon4i.mysql.pythonanywhere-services.com',
#                                    database='coon4i$default', connect_timeout=28800)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS subscriptions(
            id_s INTEGER,
            sub_until varchar(30),
            PROMPT varchar(1000),
            STYLE varchar(50),
            MESSAGES varchar(1000)
            );"""
    )
    conn.commit()

except:
    # в случае сбоя подключения будет выведено сообщение в STDOUnaT
    print('Can`t establish connection to database')


def choice_menu(call_id, id):
    markup = InlineKeyboardMarkup()
    button_style = InlineKeyboardButton(text="Стиль", callback_data="стиль")
    button_number = InlineKeyboardButton(text="Кол-во перс.", callback_data="количество персонажей")
    button_pose = InlineKeyboardButton(text="Поза", callback_data="поза")
    button_gender = InlineKeyboardButton(text="Пол", callback_data="пол")
    button_nation = InlineKeyboardButton(text="Нация", callback_data="нация")
    button_age = InlineKeyboardButton(text="Возраст", callback_data="возраст")
    button_race = InlineKeyboardButton(text="Расы", callback_data="расы")
    button_body = InlineKeyboardButton(text="Фигура", callback_data="телосложение")
    button_boobs = InlineKeyboardButton(text="Грудь", callback_data="грудь")
    button_ass = InlineKeyboardButton(text="Ягодицы", callback_data="попа")
    button_legs = InlineKeyboardButton(text="Ляжки", callback_data="ляжки")
    button_tatoo = InlineKeyboardButton(text="Тату", callback_data="тату")
    button_hair = InlineKeyboardButton(text="Волосы", callback_data="волосы")
    button_haircolor = InlineKeyboardButton(text="Цвет волос", callback_data="цвет волос")
    button_eyescolor = InlineKeyboardButton(text="Цвет глаз", callback_data="цвет глаз")
    button_clothes = InlineKeyboardButton(text="Одежда", callback_data="одежда")
    #button_emotions = InlineKeyboardButton(text="Лицо", callback_data="лицо")
    button_places = InlineKeyboardButton(text="Локации", callback_data="локации")
    button_confirm = InlineKeyboardButton(text="Готово", callback_data="отправить картинку")
    button_again = InlineKeyboardButton(text="Начать заново", callback_data="restart")
    markup.add(button_style, button_gender, button_number, button_pose, button_nation, button_age, button_race, button_body, button_boobs, button_ass, button_legs, button_tatoo, button_hair, button_haircolor, button_eyescolor, button_clothes, button_places, button_confirm, button_again)
    id_of_message = bot.send_message(call_id, "✏️ Выбери, какой параметр персонажа хочешь задать самостоятельно 👇\n\n❗️ Учти, что все оставшиеся параметры будут выбраны случайным образом\n\n⏪ Чтобы вернуться в главное меню, используй:  /menu\n\n⚠️ Обрати внимание, что при возвращении в главное меню все выбранные параметры будут сброшены", reply_markup=markup).message_id
    TO_ADD = f'"choice_menu":{id_of_message}, '
    ADD_MESSAGES_IDS(id, TO_ADD)


def GREETING_START_MENU(call_id):
    markup = InlineKeyboardMarkup()
    button_start = InlineKeyboardButton(text="Сгенерировать", callback_data="Сгенерировать картинку")
    button_sub = InlineKeyboardButton(text="Подписка", callback_data="подписка")
    button_support = InlineKeyboardButton(text="Поддержка", callback_data="поддержка")
    markup.add(button_start, button_sub, button_support)
    bot.send_message(call_id, "✌️ Добро пожаловать в главное меню!\n\n🔍 Отсюда ты сможешь начать генерацию, узнать дату окончания подписки, подробную информацию о существующих подписках и связаться с поддержкой 👇\n\n", reply_markup=markup)


def DEFAULT_START_MENU(call_id):
    markup = InlineKeyboardMarkup()
    button_start = InlineKeyboardButton(text="Сгенерировать", callback_data="Сгенерировать картинку")
    button_sub = InlineKeyboardButton(text="Подписка", callback_data="подписка")
    button_support = InlineKeyboardButton(text="Поддержка", callback_data="поддержка")
    markup.add(button_start, button_sub, button_support)
    bot.send_message(call_id,"📌 Ты находишься в главном меню\n\n🔍 Отсюда ты можешь начать генерацию, узнать дату окончания подписки, подробную информацию о существующих подписках и связаться с поддержкой 👇\n\n", reply_markup=markup)


def FACE_MENU(call_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Эмоция", callback_data="эмоция"),
               InlineKeyboardButton(text="Брови", callback_data="брови"),
               InlineKeyboardButton(text="Губы", callback_data="губы"),
               InlineKeyboardButton(text="Нос", callback_data="нос"),
               InlineKeyboardButton(text="Макияж", callback_data="макияж"),
               InlineKeyboardButton(text="Отмена", callback_data="отмена"))
    bot.send_message(chat_id=call_id, text="✏️ Выбери, какой параметр лица персонажа хочешь задать самостоятельно 👇\n\n❗️ Учти, что все оставшиеся параметры будут выбраны случайным образом", reply_markup=markup)


def days_to_sec(days):
    return days * 24 * 60 * 60


def time_remain(id):
    with conn.cursor() as cursor:
        cursor.execute(
            ""f"SELECT sub_until FROM subscriptions WHERE id_s = {id}"""
        )
        remained = int(cursor.fetchone()[0])
        if remained != 0:
            remain = remained - int(time.time())
            if remain:
                return True
            else:
                return False
        else:
            return False


def UPDATE(id, value):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""UPDATE subscriptions   
            SET PROMPT = '{value}'
	        WHERE id_s = {id};"""
        )
        conn.commit()

def GET_PROMPT(id):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT PROMPT FROM subscriptions WHERE id_s = {id};"""
        )
        return cursor.fetchone()

def GET_STYLE(id):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT STYLE FROM subscriptions WHERE id_s = {id};"""
        )
        return cursor.fetchone()

def ADD_STYLE(id, style):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""UPDATE subscriptions   
                SET STYLE = '{style}'
    	        WHERE id_s = {id};"""
        )
        conn.commit()

def GET_MESSAGES_IDS(id):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT MESSAGES FROM subscriptions WHERE id_s = {id};"""
        )
        return cursor.fetchone()

def ADD_MESSAGES_IDS(id, value):
    prev_value = ", ".join(GET_MESSAGES_IDS(id))
    value = prev_value + value
    with conn.cursor() as cursor:
        cursor.execute(
            f"""UPDATE subscriptions   
                SET MESSAGES = '{value}'
    	        WHERE id_s = {id};"""
        )
        conn.commit()

@bot.message_handler(commands=['start'])
def start(message):

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Я согласен", callback_data="я согласен"))
    bot.send_message(message.chat.id, f"👋🏼 Привет, {message.from_user.first_name}!\n\n📝 Чтобы начать работу со мной, необходимо ознакомиться с <a href='https://telegra.ph/Polzovatelskoe-Soglashenie-bot-08-23'>пользовательским соглашением</a> 👇\n\n⚠️ Внимание! Нажимая кнопку «Я согласен», Вы подтверждаете, что Вам исполнилось 18 лет и Вы принимаете пользовательское соглашение", reply_markup=markup, parse_mode="HTML")


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.delete_message(message.chat.id, message.message_id)
    cursor = conn.cursor()
    MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(message.from_user.id)) + '}')
    MESSAGES_IDS = list(MESSAGES_IDS.values())
    for key in MESSAGES_IDS:
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=key)
        except:
            pass
    UPDATE(message.from_user.id, '{"ccc":"naked", ')
    with conn.cursor() as cursor:
        cursor.execute(
            f"""UPDATE subscriptions   
                        SET MESSAGES = '{chr(123)}"shablon":"777", '
            	        WHERE id_s = {message.from_user.id};"""
        )
        conn.commit()
    with conn.cursor() as cursor:
        cursor.execute(
            f"""UPDATE subscriptions   
                        SET PROMPT = '{chr(123)}"clothes":"naked", '
            	        WHERE id_s = {message.from_user.id};"""
        )
        conn.commit()
    DEFAULT_START_MENU(message.chat.id)

@bot.message_handler(content_types=['text'])
def messages(message):
    global DURATION
    call_id = message.chat.id


    if message.text == "Разовый платеж":
        DURATION = ""
        bot.send_invoice(
            message.chat.id,  # chat_id
            'Subscription for once',  # title
            'This is test subscription with once during',
            # description
            provider_token=PAYMASTER_TOKEN,  # provider_token
            currency='rub',  # currency
            prices=[PRICE_ONCE],
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='sub_once',
            invoice_payload="test-invoice-payload")

    if message.text == "Оформить подписку":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = "1 месяц"
        button2 = "3 месяца"
        button3 = "12 месяцев"
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, "Выберите период оформления подписки:", reply_markup=markup)
    if message.text == "1 месяц" or message.text == "3 месяца" or message.text == "12 месяцев":
        if message.text == "1 месяц":
            DURATION = message.text
            bot.send_invoice(
                message.chat.id,  # chat_id
                'Subscription for 1 month',  # title
                'This is test subscription with during 1 month',
                # description
                provider_token=PAYMASTER_TOKEN,  # provider_token
                currency='rub',  # currency
                prices=[PRICE_1_MONTH],
                is_flexible=False,  # True If you need to set up Shipping Fee
                start_parameter='sub_1_month',
                invoice_payload="test-invoice-payload")
            TIME = str(int(time.time()) + days_to_sec(30))
            cursor.execute(
                f"""UPDATE subscriptions
                 SET sub_until = {TIME}
                 WHERE id_s = {message.from_user.id};
               """
            )
            conn.commit()
        if message.text == "3 месяца":
            DURATION = message.text
            bot.send_invoice(
                message.chat.id,  # chat_id
                'Subscription for 3 month',  # title
                'This is test subscription with during 3 month',
                # description
                provider_token=PAYMASTER_TOKEN,  # provider_token
                currency='rub',  # currency
                prices=[PRICE_3_MONTH],
                is_flexible=False,  # True If you need to set up Shipping Fee
                start_parameter='sub_3_month',
                invoice_payload="test-invoice-payload")
            TIME = str(int(time.time()) + days_to_sec(90))
            cursor.execute(
                f"""UPDATE subscriptions
                 SET sub_until = {TIME}
                 WHERE id_s = {message.from_user.id};
               """
            )
            conn.commit()
        if message.text == "12 месяцев":
            DURATION = message.text
            bot.send_invoice(
                message.chat.id,  # chat_id
                'Subscription for 12 month',  # title
                'This is test subscription with during 12 month',
                # description
                provider_token=PAYMASTER_TOKEN,  # provider_token
                currency='rub',  # currency
                prices=[PRICE_12_MONTH],
                is_flexible=False,  # True If you need to set up Shipping Fee
                start_parameter='sub_12_month',
                invoice_payload="test-invoice-payload")
            TIME = str(int(time.time()) + days_to_sec(365))
            cursor.execute(
                f"""UPDATE subscriptions
                 SET sub_until = {TIME}
                 WHERE id_s = {message.from_user.id};
               """
            )
            conn.commit()




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    call_id = call.message.chat.id
    cursor = conn.cursor()
    global NATIONS
    global DURATION
    global POSES
    global AGES
    global EMOTIONS


    if call.data == "локации":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Замок", callback_data="castle"),
                   InlineKeyboardButton(text="Река", callback_data="river"),
                   InlineKeyboardButton(text="Бар", callback_data="bar"),
                   InlineKeyboardButton(text="Ванная", callback_data="bathroom"),
                   InlineKeyboardButton(text="Пляж", callback_data="beach"),
                   InlineKeyboardButton(text="Кровать", callback_data="bed"),
                   InlineKeyboardButton(text="Автобус", callback_data="bus"),
                   InlineKeyboardButton(text="Кафе", callback_data="cafe"),
                   InlineKeyboardButton(text="Казино", callback_data="casino"),
                   InlineKeyboardButton(text="Пещера", callback_data="cave"),
                   InlineKeyboardButton(text="Церковь", callback_data="church"),
                   InlineKeyboardButton(text="Пустыня", callback_data="desert"),
                   InlineKeyboardButton(text="Лес", callback_data="forest"),
                   InlineKeyboardButton(text="Госпиталь", callback_data="hospital"),
                   InlineKeyboardButton(text="Кухня", callback_data="kitchen"),
                   InlineKeyboardButton(text="Горы", callback_data="mountains"),
                   InlineKeyboardButton(text="Праздник", callback_data="party"),
                   InlineKeyboardButton(text="Бассейн", callback_data="pool"),
                   InlineKeyboardButton(text="Ресторан", callback_data="restaurant"),
                   InlineKeyboardButton(text="Сауна", callback_data="sauna"),
                   InlineKeyboardButton(text="Улица", callback_data="street"),
                   InlineKeyboardButton(text="Яхта", callback_data="yacht"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call_id, message_id=call.message.message_id, text="Выбери, в какой локации хочешь видеть персонажа 👇", reply_markup=markup)


    if call.data ==  "лицо":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Эмоция", callback_data="эмоция"),
                   InlineKeyboardButton(text="Брови", callback_data="брови"),
                   InlineKeyboardButton(text="Губы", callback_data="губы"),
                   InlineKeyboardButton(text="Нос", callback_data="нос"),
                   InlineKeyboardButton(text="Макияж", callback_data="макияж"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call_id, message_id=call.message.message_id, text="✏️ Выбери, какой параметр лица персонажа хочешь задать самостоятельно 👇\n\n❗️ Учти, что все оставшиеся параметры будут выбраны случайным образом", reply_markup=markup)



    if call.data == "эмоция":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Ахегао", callback_data="ahegao"),
                   InlineKeyboardButton(text="Оргазм", callback_data="orgasm"),
                   InlineKeyboardButton(text="Хорни", callback_data="horny"),
                   InlineKeyboardButton(text="Счастье", callback_data="happy"),
                   InlineKeyboardButton(text="Улыбка", callback_data="smile"),
                   InlineKeyboardButton(text="Милая", callback_data="cute"),
                   InlineKeyboardButton(text="Грустная", callback_data="sad"),
                   InlineKeyboardButton(text="Плачущая", callback_data="crying"),
                   InlineKeyboardButton(text="Злая", callback_data="angry"),
                   InlineKeyboardButton(text="Серьезная", callback_data="serious"),
                   InlineKeyboardButton(text="Отмена", callback_data="return_to_face"))
        bot.edit_message_text(chat_id=call_id, message_id=call.message.message_id, text="Выбери, какую эмоцию хочешь видеть на персонаже 👇", reply_markup=markup)


    if call.data == "return_to_face":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Эмоция", callback_data="эмоция"),
                   InlineKeyboardButton(text="Брови", callback_data="брови"),
                   InlineKeyboardButton(text="Губы", callback_data="губы"),
                   InlineKeyboardButton(text="Нос", callback_data="нос"),
                   InlineKeyboardButton(text="Макияж", callback_data="макияж"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call_id, message_id=call.message.message_id, text="✏️ Выбери, какой параметр лица персонажа хочешь задать самостоятельно 👇\n\n❗️ Учти, что все оставшиеся параметры будут выбраны случайным образом", reply_markup=markup)

    if call.data == "подписка":
            bot.send_message(call.message.chat.id, "тут будет инфа про подписку")
    if call.data == "поддержка":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Вернуться в главное меню", callback_data="вернуться в главное меню"))
        text = f"📬 Для того, чтобы связаться с нами, отправь письмо с интересующим тебя вопросом или жалобой на эту электронную почту 👇\n\n📧 blabla@mail.ru\n\n🆔 Обязательно укажи в письме ID своего профиля: {call.from_user.id}"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup)


    if call.data == "вернуться в главное меню":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        DEFAULT_START_MENU(call_id)


    if call.data == "отмена":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choice_menu(call_id, call.from_user.id)
    if call.data == "возраст":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='18-24', callback_data='21_a'),
                   InlineKeyboardButton(text='25-30', callback_data='27_a'),
                   InlineKeyboardButton(text='31-40', callback_data='36_a'),
                   InlineKeyboardButton(text='41-50', callback_data='46_a'),
                   InlineKeyboardButton(text='51-60', callback_data='56_a'),
                   InlineKeyboardButton(text='60+', callback_data='65_a'),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите возраст персонажа 👇', reply_markup=markup)

    if call.data in AGES.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(AGES.values()).index(call.data)
        key = list(AGES.keys())[value]
        if 'age' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['age'],
                                      text=f"✅ Выбран возраст: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбран возраст: {key.lower()}").message_id
            TO_ADD = f'"age":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"age":"{call.data[:-2]} aged", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)



    if call.data == "количество персонажей":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='1', callback_data='1'),
                   InlineKeyboardButton(text='2', callback_data='2'),
                   InlineKeyboardButton(text='3', callback_data='3'),
                   InlineKeyboardButton(text='4', callback_data='4'),
                   InlineKeyboardButton(text='5', callback_data='5'),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите, сколько персонажей хотите видеть на фото 👇', reply_markup=markup)

    if call.data.isdigit() and 1 <= int(call.data) <= 5:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        if 'number' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['number'],
                                      text=f"✅ Выбрано количество персонажей: {call.data}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрано количество персонажей: {call.data}").message_id
            TO_ADD = f'"number":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"number":"{call.data} people", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data == "поза":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="На четв.", callback_data="on all fours"),
                   InlineKeyboardButton(text="На спине", callback_data="lying on back"),
                   InlineKeyboardButton(text="На животе", callback_data="lying on stomach"),
                   InlineKeyboardButton(text="На боку", callback_data="on side"),
                   InlineKeyboardButton(text="Ползет", callback_data="crawl"),
                   InlineKeyboardButton(text="Танцует", callback_data="dance"),
                   InlineKeyboardButton(text="Лежит", callback_data="laying"),
                   InlineKeyboardButton(text="Модельная", callback_data="model"),
                   InlineKeyboardButton(text="Раздвинутые ноги", callback_data="spreaded legs"),
                   InlineKeyboardButton(text="В присяде", callback_data="squatting"),
                   InlineKeyboardButton(text="Стоит", callback_data="standing"),
                   InlineKeyboardButton(text="Йога", callback_data="yoga"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите, в какой позе будет находится ваш персонаж 👇', reply_markup=markup)


    if call.data == "restart":
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        MESSAGES_IDS = list(MESSAGES_IDS.values())
        for key in MESSAGES_IDS:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=key)
            except:
                pass
        UPDATE(call.from_user.id, '{"ccc":"naked", ')
        with conn.cursor() as cursor:
            cursor.execute(
                f"""UPDATE subscriptions   
                    SET MESSAGES = '{chr(123)}"shablon":"777", '
        	        WHERE id_s = {call.from_user.id};"""
            )
            conn.commit()
        with conn.cursor() as cursor:
            cursor.execute(
                f"""UPDATE subscriptions   
                    SET PROMPT = '{chr(123)}"clothes":"naked", '
        	        WHERE id_s = {call.from_user.id};"""
            )
            conn.commit()
        markup = InlineKeyboardMarkup()
        button_real = InlineKeyboardButton(text="Реализм", callback_data="реализм")
        button_art = InlineKeyboardButton(text="Арт", callback_data="арт")
        button_anime = InlineKeyboardButton(text="Аниме", callback_data="аниме")
        markup.add(button_real, button_anime, button_art)
        bot.send_message(chat_id=call.message.chat.id, text="Для начала необходимо выбрать стиль, в котором будет выполнена фотография 👇", reply_markup=markup)


    if call.data == "отправить картинку":
        PROMPT = GET_PROMPT(call.from_user.id)
        PROMPT = eval(", ".join(PROMPT) + '}')
        if len(PROMPT) == 1:
            bot.answer_callback_query(callback_query_id=call.id, text="Выбери хотя бы один параметр")
        else:
            if time_remain(call_id):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Запрос получен, осталось немного подождать 🕐")

                LIST = list(PROMPT.values())
                request = ', '.join(LIST)
                if ' woman' in request:
                    request += ', soft light, cinematic light, a neat vagina, beautiful, cute face, pretty face, without pants, full body, show vagina, shaved vagina, shaved body, correct anatomy of the fingers, two arms, '
                elif ' man' in request:
                    request += ', soft light, cinematic light, without pants, full body, handsome, correct anatomy of the fingers, two arms, '
                else:
                    request += ', soft light, cinematic light, without pants, full body, correct anatomy of the fingers, two arms, '
                style = ", ".join(GET_STYLE(call.from_user.id)).split('"')
                request += style[-2]
                link = zapros(request, style[-2])
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text="Сгенерировать еще одну картинку", callback_data="restart photo"))
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_photo(chat_id=call.message.chat.id, photo=f"{link}", caption=f"✌️ Фото сгенерировано успешно!\n\n\nPrompt: {request}", reply_markup=markup)
                UPDATE(call.from_user.id, '{"ccc":"naked", ')
                with conn.cursor() as cursorбот:
                    cursor.execute(
                        f"""UPDATE subscriptions   
                            SET MESSAGES = '{chr(123)}"shablon":"777", '
                	        WHERE id_s = {call.from_user.id};"""
                    )
                    conn.commit()
            else:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(text='1 месяц', callback_data="1 месяц"),
                           InlineKeyboardButton(text="3 месяца", callback_data="3 месяца подписка"),
                           InlineKeyboardButton(text="12 месяцев", callback_data="12 месяцев подписка"),
                           InlineKeyboardButton(text="Разовый платеж", callback_data="разовый платеж"),
                           InlineKeyboardButton(text="Отмена", callback_data="отмена"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Для того, чтобы получить сгенерированное фото, нужно обладать подпиской либо внести разовый платеж 👇", reply_markup=markup)


    if call.data == "Сгенерировать картинку" or call.data == "Сгенерировать еще одну картинку":
        if call.data == "Сгенерировать картинку":
            markup = InlineKeyboardMarkup()
            button_real = InlineKeyboardButton(text="Реализм", callback_data="реализм")
            button_art = InlineKeyboardButton(text="Арт", callback_data="арт")
            button_anime = InlineKeyboardButton(text="Аниме", callback_data="аниме")
            markup.add(button_real, button_anime, button_art)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Для начала необходимо выбрать стиль, в котором будет выполнена фотография 👇', reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup()
            button_real = InlineKeyboardButton(text="Реализм", callback_data="реализм")
            button_art = InlineKeyboardButton(text="Арт", callback_data="арт")
            button_anime = InlineKeyboardButton(text="Аниме", callback_data="аниме")
            markup.add(button_real, button_anime, button_art)
            bot.send_message(chat_id=call.message.chat.id, text='Для начала необходимо выбрать стиль, в котором будет выполнена фотография 👇', reply_markup=markup)


    if call.data == "я согласен":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"👋🏼 Привет, {call.from_user.first_name}!\n\n📝 Чтобы начать работу со мной, необходимо ознакомиться с <a href='https://telegra.ph/Polzovatelskoe-Soglashenie-bot-08-23'>пользовательским соглашением</a> 👇\n\n⚠️ Внимание! Нажимая кнопку «Я согласен», Вы подтверждаете, что Вам исполнилось 18 лет и Вы принимаете пользовательское соглашение", reply_markup=None, parse_mode="HTML")
        with conn.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO subscriptions
                    (id_s, sub_until, PROMPT, MESSAGES)
                    SELECT {call.from_user.id}, 0, '{chr(123)}"clothes":"naked", ', '{chr(123)}"shablon":"777", '
                    WHERE
                    NOT EXISTS (
                        SELECT id_s FROM subscriptions WHERE id_s = {call.from_user.id}
                        );"""

            )
            conn.commit()
        GREETING_START_MENU(call_id)
        #choice_menu(call_id)

    if call.data == "1 месяц":
        DURATION = call.data
        bot.send_invoice(
            call.message.chat.id,  # chat_id
            'Subscription for 1 month',  # title
            'This is test subscription with during 1 month',
            # description
            provider_token=PAYMASTER_TOKEN,  # provider_token
            currency='rub',  # currency
            prices=[PRICE_1_MONTH],
            is_flexible=False,  # True If you need to set up Ship/ыефкng Fee
            start_parameter='sub_1_month',
            invoice_payload="test-invoice-payload")
        TIME = str(int(time.time()) + days_to_sec(30))
        cursor.execute(
            f"""UPDATE subscriptions
                         SET sub_until = {TIME}
                         WHERE id_s = {call.message.from_user.id};
                       """
        )
        conn.commit()





    if call.data == "restart photo":
        markup = InlineKeyboardMarkup()
        button_real = InlineKeyboardButton(text="Реализм", callback_data="реализм")
        button_art = InlineKeyboardButton(text="Арт", callback_data="арт")
        button_anime = InlineKeyboardButton(text="Аниме", callback_data="аниме")
        markup.add(button_real, button_anime, button_art)
        bot.send_message(chat_id=call.message.chat.id, text="Для начала необходимо выбрать стиль, в котором будет выполнена фотография 👇", reply_markup=markup)

    if call.data == "стиль":
        markup = InlineKeyboardMarkup()
        button_real = InlineKeyboardButton(text="Реализм", callback_data="реализм")
        button_art = InlineKeyboardButton(text="Арт", callback_data="арт")
        button_anime = InlineKeyboardButton(text="Аниме", callback_data="аниме")
        markup.add(button_real, button_anime, button_art)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите, в каком стиле будет выполнена фотография 👇', reply_markup=markup)



    if call.data == "тату":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Да", callback_data="тату да"),
                   InlineKeyboardButton(text="Нет", callback_data="тату нет"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Будет ли у Вашего персонажа тату?', reply_markup=markup)

    if call.data == "тату да":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        if 'tattoo' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['tattoo'], text="✅ Тату: есть")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, "✅ Тату: есть").message_id
            TO_ADD = f'"tattoo":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += '"tattoo":"some tattooes", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data == "тату нет":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        if 'tattoo' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['tattoo'],
                                      text="✅ Тату: нет")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, "✅ Тату: нет").message_id
            TO_ADD = f'"gender":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += '"tattoo":"no tattoo", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data == "волосы":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Длинные", callback_data="long"),
                   InlineKeyboardButton(text="Средние", callback_data="middle-length"),
                   InlineKeyboardButton(text="Короткие", callback_data="short"),
                   InlineKeyboardButton(text="Коса", callback_data="braid"),
                   InlineKeyboardButton(text="Каре", callback_data="bob"),
                   InlineKeyboardButton(text="Хвост", callback_data="ponytail"),
                   InlineKeyboardButton(text="Ирокез", callback_data="mohawk"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите прическу персонажа 👇', reply_markup=markup)



    if call.data == "цвет волос":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Блонд", callback_data="blonde_h"),
                   InlineKeyboardButton(text="Брюнет(ка)", callback_data="brunette_h"),
                   InlineKeyboardButton(text="Рыжий", callback_data="orange_h"),
                   InlineKeyboardButton(text="Белый", callback_data="white_h"),
                   InlineKeyboardButton(text="Красный", callback_data="red_h"),
                   InlineKeyboardButton(text="Розовый", callback_data="pink_h"),
                   InlineKeyboardButton(text="Синий", callback_data="blue_h"),
                   InlineKeyboardButton(text="Желтый", callback_data="yellow_h"),
                   InlineKeyboardButton(text="Зеленый", callback_data="green_h"),
                   InlineKeyboardButton(text="Фиолетовый", callback_data="purple_h"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите цвет волос персонажа 👇', reply_markup=markup)



    if call.data == "цвет глаз":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Зеленые", callback_data="green_e"),
                   InlineKeyboardButton(text="Карие", callback_data="brown_e"),
                   InlineKeyboardButton(text="Серые", callback_data="grey_e"),
                   InlineKeyboardButton(text="Голубые", callback_data="blue_e"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите цвет глаз персонажа 👇', reply_markup=markup)

    if call.data == "одежда":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Голая(ый)", callback_data="naked"),
                   InlineKeyboardButton(text="Платье", callback_data="dress"),
                   InlineKeyboardButton(text="Хиджаб", callback_data="hijab"),
                   InlineKeyboardButton(text="Школьная форма", callback_data="school uniform"),
                   InlineKeyboardButton(text="Халат", callback_data="bathrobe"),
                   InlineKeyboardButton(text="Мини-юбка", callback_data="mini skirt"),
                   InlineKeyboardButton(text="Чулки", callback_data="cotton thick black stockings"),
                   InlineKeyboardButton(text="Купальник", callback_data="swimsuit"),
                   InlineKeyboardButton(text="Латексный костюм", callback_data="thick black latex suit"),
                   InlineKeyboardButton(text="Хеллоуин костюм", callback_data="halloween costume"),
                   InlineKeyboardButton(text="Корсет", callback_data="corset"),
                   InlineKeyboardButton(text="Античная одежда", callback_data="antique clothes"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите, какая одежда будет у персонажа 👇', reply_markup=markup)

    if call.data == "телосложение":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Накаченное", callback_data="muscular"),
                   InlineKeyboardButton(text="Пухлое", callback_data="plump"),
                   InlineKeyboardButton(text="Пышное", callback_data="busty"),
                   InlineKeyboardButton(text="Спортивное", callback_data="sporty"),
                   InlineKeyboardButton(text="Толстое", callback_data="fat"),
                   InlineKeyboardButton(text="Худое", callback_data="skinny"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите фигуру персонажа 👇', reply_markup=markup)


    if call.data == "грудь":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Огромная", callback_data="huge_b"),
                   InlineKeyboardButton(text="Большая", callback_data="big_b"),
                   InlineKeyboardButton(text="Средняя", callback_data="medium-sized_b"),
                   InlineKeyboardButton(text="Маленькая", callback_data="small_b"),
                   InlineKeyboardButton(text="Натуральная", callback_data="natural_b"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите размер груди персонажа 👇', reply_markup=markup)

    if call.data == "попа":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Огромные", callback_data="huge_a"),
                   InlineKeyboardButton(text="Большие", callback_data="big_a"),
                   InlineKeyboardButton(text="Средние", callback_data="medium-sized_a"),
                   InlineKeyboardButton(text="Маленькие", callback_data="small_a"),
                   InlineKeyboardButton(text="Круглые", callback_data="round_a"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите размер ягодиц персонажа 👇', reply_markup=markup)



    if call.data == "ляжки":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Толстые", callback_data="fat_l"),
                   InlineKeyboardButton(text="Пышные", callback_data="busty_l"),
                   InlineKeyboardButton(text="Спортивные", callback_data="sporty_l"),
                   InlineKeyboardButton(text="Худые", callback_data="skinny_l"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите размер ляжек персонажа 👇', reply_markup=markup)


    if call.data == "расы":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Человек", callback_data="human"),
                   InlineKeyboardButton(text="Ангел", callback_data="angel"),
                   InlineKeyboardButton(text="Демон", callback_data="demon"),
                   InlineKeyboardButton(text="Рептилия", callback_data="reptile"),
                   InlineKeyboardButton(text="Робот", callback_data="robot"),
                   InlineKeyboardButton(text="Суккуб", callback_data="succubus"),
                   InlineKeyboardButton(text="Фея", callback_data="fairy"),
                   InlineKeyboardButton(text="Фурри", callback_data="furry"),
                   InlineKeyboardButton(text="Эльф", callback_data="elf"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите расу персонажа 👇', reply_markup=markup)


    if call.data == "реализм" or call.data == "аниме" or call.data == "арт":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        if 'style' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['style'], text=f"✅ Выбран стиль фотографии: {call.data}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбран стиль фотографии: {call.data}").message_id
            TO_ADD = f'"style":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        if call.data == "реализм":
            ADD_STYLE(call.from_user.id, '"style":"photorealism"')
        elif call.data == "аниме":
            ADD_STYLE(call.from_user.id, '"style":"anime"')
        elif call.data == "арт":
            ADD_STYLE(call.from_user.id, '"style":"art"')
        choice_menu(call_id, call.from_user.id)
    if call.data == "пол":
        markup = InlineKeyboardMarkup()
        button_female = InlineKeyboardButton(text="Мужской", callback_data="мужской")
        button_male = InlineKeyboardButton(text="Женский", callback_data="женский")
        button_cancel = InlineKeyboardButton(text="Отмена", callback_data="отмена")
        markup.add(button_female, button_male, button_cancel)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите пол 👇', reply_markup=markup)
    if call.data == "мужской":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        if 'gender' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['gender'], text="✅ Выбран пол: мужской")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, "✅ Выбран пол: мужской").message_id
            TO_ADD = f'"gender":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += '"gender":"man", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)
    if call.data == "женский":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        if 'gender' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['gender'], text="✅ Выбран пол: женский")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, "✅ Выбран пол: женский").message_id
            TO_ADD = f'"gender":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += '"gender":"woman", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)



    if call.data == "нация":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Белые", callback_data="white"),
                   InlineKeyboardButton(text="Европейцы", callback_data="european"),
                   InlineKeyboardButton(text="Черные", callback_data="black"),
                   InlineKeyboardButton(text="Латины", callback_data="latin"),
                   InlineKeyboardButton(text="Русские", callback_data="russian"),
                   InlineKeyboardButton(text="Австрийцы", callback_data="austrian"),
                   InlineKeyboardButton(text="Американцы", callback_data="american"),
                   InlineKeyboardButton(text="Арабы", callback_data="arab"),
                   InlineKeyboardButton(text="Армяне", callback_data="armenian"),
                   InlineKeyboardButton(text="Белорусы", callback_data="belarusian"),
                   InlineKeyboardButton(text="Бразильцы", callback_data="brazilian"),
                   InlineKeyboardButton(text="Британцы", callback_data="british"),
                   InlineKeyboardButton(text="Румыны", callback_data="romanians"),
                   InlineKeyboardButton(text="Татары", callback_data="tatar"),
                   InlineKeyboardButton(text="Турки", callback_data="turk"),
                   InlineKeyboardButton(text="Вьетнамцы", callback_data="vietnamese"),
                   InlineKeyboardButton(text="Греки", callback_data="greek"),
                   InlineKeyboardButton(text="Грузины", callback_data="georgian"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"),
                   InlineKeyboardButton(text="Вперед>>", callback_data="вперед"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите нацию персонажа 👇", reply_markup=markup)


    if call.data == "вперед":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Египтяне", callback_data="egyptian"),
                   InlineKeyboardButton(text="Испанцы", callback_data="spaniard"),
                   InlineKeyboardButton(text="Итальянцы", callback_data="italian"),
                   InlineKeyboardButton(text="Казахи", callback_data="kazakhs"),
                   InlineKeyboardButton(text="Китайцы", callback_data="chinese"),
                   InlineKeyboardButton(text="Корейцы", callback_data="korean"),
                   InlineKeyboardButton(text="Японцы", callback_data="japanese"),
                   InlineKeyboardButton(text="Немцы", callback_data="german"),
                   InlineKeyboardButton(text="Персы", callback_data="persian"),
                   InlineKeyboardButton(text="Поляки", callback_data="pole"),
                   InlineKeyboardButton(text="Португальцы", callback_data="portuguese"),
                   InlineKeyboardButton(text="Украинцы", callback_data="ukrainians"),
                   InlineKeyboardButton(text="Французы", callback_data="french"),
                   InlineKeyboardButton(text="Чехи", callback_data="czech"),
                   InlineKeyboardButton(text="Шведы", callback_data="swede"),
                   InlineKeyboardButton(text="<<Назад", callback_data="назад"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена")
                   )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите нацию персонажа 👇", reply_markup=markup)

    if call.data == "назад":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Белые", callback_data="white"),
                   InlineKeyboardButton(text="Европейцы", callback_data="european"),
                   InlineKeyboardButton(text="Черные", callback_data="black"),
                   InlineKeyboardButton(text="Латины", callback_data="latin"),
                   InlineKeyboardButton(text="Русские", callback_data="russian"),
                   InlineKeyboardButton(text="Австрийцы", callback_data="austrian"),
                   InlineKeyboardButton(text="Американцы", callback_data="american"),
                   InlineKeyboardButton(text="Арабы", callback_data="arab"),
                   InlineKeyboardButton(text="Армяне", callback_data="armenian"),
                   InlineKeyboardButton(text="Белорусы", callback_data="belarusian"),
                   InlineKeyboardButton(text="Бразильцы", callback_data="brazilian"),
                   InlineKeyboardButton(text="Британцы", callback_data="british"),
                   InlineKeyboardButton(text="Румыны", callback_data="romanians"),
                   InlineKeyboardButton(text="Татары", callback_data="tatar"),
                   InlineKeyboardButton(text="Турки", callback_data="turk"),
                   InlineKeyboardButton(text="Вьетнамцы", callback_data="vietnamese"),
                   InlineKeyboardButton(text="Греки", callback_data="greek"),
                   InlineKeyboardButton(text="Грузины", callback_data="georgian"),
                   InlineKeyboardButton(text="Отмена", callback_data="отмена"),
                   InlineKeyboardButton(text="Вперед>>", callback_data="вперед"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите нацию персонажа 👇", reply_markup=markup)

    if call.data in NATIONS.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(NATIONS.values()).index(call.data)
        key = list(NATIONS.keys())[value]
        if 'nation' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['nation'], text=f"✅ Выбрана нация: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана нация: {key.lower()}").message_id
            TO_ADD = f'"nation":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"nation":"{call.data} nation", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in RACES.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(RACES.values()).index(call.data)
        key = list(RACES.keys())[value]
        if 'race' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['race'],
                                      text=f"✅ Выбрана раса: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана раса: {key.lower()}").message_id
            TO_ADD = f'"race":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"race":"{call.data} race", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in BODY.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(BODY.values()).index(call.data)
        key = list(BODY.keys())[value]
        if 'body' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['body'],
                                      text=f"✅ Выбрана фигура: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана фигура: {key.lower()}").message_id
            TO_ADD = f'"body":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        if call.data == "sporty":
            CURR_PROMPT += f'"body":"athletic figure", '
        else:
            CURR_PROMPT += f'"body":"{call.data} body", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)


    if call.data in BOOBS.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(BOOBS.values()).index(call.data)
        key = list(BOOBS.keys())[value]
        if 'boobs' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['boobs'],
                                      text=f"✅ Выбран размер груди: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбран размер груди: {key.lower()}").message_id
            TO_ADD = f'"boobs":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"boobs":"{call.data[:-2]} boobs", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in ASS.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(ASS.values()).index(call.data)
        key = list(ASS.keys())[value]
        if 'ass' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['ass'],
                                      text=f"✅ Выбран размер ягодиц: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбран размер ягодиц: {key.lower()}").message_id
            TO_ADD = f'"ass":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"ass":"{call.data[:-2]} ass", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in PLACES.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(PLACES.values()).index(call.data)
        key = list(PLACES.keys())[value]
        if 'place' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['place'],
                                      text=f"✅ Выбрана локация: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана локация: {key.lower()}").message_id
            TO_ADD = f'"place":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"place":"{call.data}", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in LEGS.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(LEGS.values()).index(call.data)
        key = list(LEGS.keys())[value]
        if 'legs' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['legs'],
                                      text=f"✅ Выбран размер ляжек: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбран размер ляжек: {key.lower()}").message_id
            TO_ADD = f'"legs":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"legs":"{call.data[:-2]} legs", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in HAIRCUT.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(HAIRCUT.values()).index(call.data)
        key = list(HAIRCUT.keys())[value]
        if 'haircut' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['haircut'],
                                      text=f"✅ Выбрана прическа: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана прическа: {key.lower()}").message_id
            TO_ADD = f'"haircut":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"haircut":"{call.data} haircut", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in HAIRCOLOR.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(HAIRCOLOR.values()).index(call.data)
        key = list(HAIRCOLOR.keys())[value]
        if 'haircolor' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['haircolor'],
                                      text=f"✅ Выбран цвет волос: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбран цвет волос: {key.lower()}").message_id
            TO_ADD = f'"haircolor":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"haircolor":"{call.data[:-2]} hair", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in EYESCOLOR.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(EYESCOLOR.values()).index(call.data)
        key = list(EYESCOLOR.keys())[value]
        if 'eyes color' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['eyes color'],
                                      text=f"✅ Выбран цвет глаз: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбран цвет глаз: {key.lower()}").message_id
            TO_ADD = f'"eyes color":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"eyes color":"{call.data[:-2]} eyes", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in CLOTHES.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(CLOTHES.values()).index(call.data)
        key = list(CLOTHES.keys())[value]
        if 'clothes' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['clothes'],
                                      text=f"✅ Выбрана одежда: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана одежда: {key.lower()}").message_id
            TO_ADD = f'"clothes":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"clothes":"{call.data}", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in POSES.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(POSES.values()).index(call.data)
        key = list(POSES.keys())[value]
        if 'pose' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['pose'],
                                      text=f"✅ Выбрана поза: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана поза: {key.lower()}").message_id
            TO_ADD = f'"pose":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"pose":"{call.data} pose", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        choice_menu(call_id, call.from_user.id)

    if call.data in EMOTIONS.values():
        bot.delete_message(call.message.chat.id, call.message.message_id)
        MESSAGES_IDS = eval(", ".join(GET_MESSAGES_IDS(call.from_user.id)) + '}')
        value = list(EMOTIONS.values()).index(call.data)
        key = list(EMOTIONS.keys())[value]
        if 'emotion' in MESSAGES_IDS.keys():
            try:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=MESSAGES_IDS['emotion'],
                                      text=f"✅ Выбрана эмоция: {key.lower()}")
            except:
                pass
        else:
            id_of_message = bot.send_message(call.message.chat.id, f"✅ Выбрана эмоция: {key.lower()}").message_id
            TO_ADD = f'"emotion":{id_of_message}, '
            ADD_MESSAGES_IDS(call.from_user.id, TO_ADD)
        CURR_PROMPT = ", ".join(GET_PROMPT(call.from_user.id))
        CURR_PROMPT += f'"emotion":"{call.data}", '
        UPDATE(call.from_user.id, CURR_PROMPT)
        FACE_MENU(call_id)



@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    bot.answer_shipping_query(shipping_query.id, ok=True)

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    global DURATION
    #global PROMPT
    global MESSAGES_IDS
    if len(DURATION):
        bot.send_message(message.chat.id, f"Спасибо за оформление подписки на {DURATION}!")
        bot.send_message(message.chat.id, f"Запрос получен, осталось немного подождать 🕐")

        if DURATION == "1 месяц":
            TIME = str(int(time.time()) + days_to_sec(30))
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""UPDATE subscriptions
                                 SET sub_until = {TIME}
                                 WHERE id_s = {message.from_user.id};
                               """
                )
                conn.commit()
    else:
        bot.send_message(message.chat.id, "Спасибо за покупку!")
        bot.send_message(message.chat.id, f"Запрос получен, осталось немного подождать 🕐")
    PROMPT = GET_PROMPT(message.from_user.id)
    PROMPT = eval(", ".join(PROMPT) + '}')
    LIST = list(PROMPT.values())
    request = ', '.join(LIST)
    if ' woman' in request:
        request += ', soft light, cinematic light, a neat vagina, beautiful, cute face, pretty face, without pants, full body, show vagina, shaved vagina, shaved body, correct anatomy of the fingers, two arms, '
    elif ' man' in request:
        request += ', soft light, cinematic light, without pants, full body, handsome, correct anatomy of the fingers, two arms, '
    else:
        request += ', soft light, cinematic light, without pants, full body, correct anatomy of the fingers, two arms, '
    style = ", ".join(GET_STYLE(message.from_user.id)).split('"')
    request += style[-2]
    link = zapros(request, style[-2])
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Сгенерировать еще одну картинку", callback_data="restart photo"))
    bot.send_photo(chat_id=message.chat.id, photo=f"{link}", caption=f"✌️ Фото сгенерировано успешно!"    ,
                   reply_markup=markup)
    UPDATE(message.from_user.id, '{"clothe":"naked", ')
    with conn.cursor() as cursor:
        cursor.execute(
            f"""UPDATE subscriptions   
                SET MESSAGES = '{chr(123)}"shablon":"777", '
    	        WHERE id_s = {message.from_user.id};"""
        )
        conn.commit()

bot.infinity_polling()
