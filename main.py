'''тг бот з завданнями
список завдань : ШОСЬ З ХОЛОСТЯКОМ
ЛАБІРИНТ ПАПОК
ШОСЬ З АВТО
ШОСЬ З Ф1
ШОСЬ З ФУТБОЛОМ
ШОСЬ З МАЧО І БОТАН
ШОСЬ З ІЛЮЗІЯ ОБМАНУ
ШОСЬ З ВЕРТЕПОМ

ЦЕ ВСЕ ЗЄДНАТИ В ШЛЯХ ДО РІЗНИХ ТОЧОК
СПИСОК ТОЧОК : КАТОК
РЕСТОРАН - КАФЕ
КВІТИ
ПРИТУЛОК (49.8448438, 24.0345675)
_________________________
bot.send_location(chat_id, latitude=49.8397, longitude=24.0297) - наділмсати локкаію

'''
import telebot
from telebot import types
bot = telebot.TeleBot('8406651789:AAGH8ysyQfP_EyQgLp9wQ2MADgVuxWPk_LY')

questions = [
    {
        "photos": ["photo/mercerdes.png", "photo/Mclaren.png","photo/ferarri.png"],
        "caption": "Моя улюблена команда в F1?",
        "buttons": [("McLaren", True), ("Ferrari", False), ("Mercedes", False)]
    },
    {
        "photos": ["photo/dunamo.png","photo/skala.png","photo/torpa.png"],
        "caption": "Яка перша команда вашого МУЩИНИ",
        "buttons": [("Тарпа (Угорщина)",False),("Динамо Львів", False), ("Скала Стрий", True)]
    },
    {
        "photos": ["files/f1_1.jpg", "files/f1_2.jpg", "files/f1_3.jpg"],
        "caption": "Мій улюблений актор?",
        "buttons": [("Кевін Харт ( 1 фото )", True), ("Метю Макконехі", False), ("Mercedes", False)]
    }
]



@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_location(msg.chat.id, latitude=49.8397, longitude=24.0297)
    bot.send_message(msg.chat.id,'Привіт сонце ❤️ \nТи ще заспана і напевне не розумієш шо робиться.'
                                 '\nЗараз я тобі все коротко поясню \nСьогодні день квестів для тебе, мене в гуртожитку вже немає і щоб мене знайти тобі треба пройти кілька завдань '
                                 'Кожне завдання це нова локація де я тебе буду чекати вони будуть протягом всьго дня і не вздумай знімати тіктоки перед виходом бо я все прорахував по часу\n(ЗАПІЗНИШСЯ НЕ ЗУСТРІНЕМОСЬ,БО Я БУДУ В ІНШОМУ МІСЦІ)'
                                 '\nПисати до мене теж марно я не відпишу,млжеш знімати відео як ти це проходиш або сісти з дівчатми проходити деякі завдання\n'
                                 'Пиши "Готова" і ми почнемо')

@bot.message_handler(content_types=["text"])
def first_qst(msg):
    if msg.text.lower() == "готова":
        bot.send_message(msg.chat.id,"(49.8448438, 24.0345???)\n Це локація першої нашої зустрічі\n"
                                     "Ти просто вставляєш це в гугл мепс і воно тобі видасть точку на карті\n"
                                     "Але як ти бачиш тут не вистачає трьох останніх цифр\nДля того щоб знайти ці цифри виконуй вказівки в повідомленні знизу")
        bot.send_message(msg.chat.id,"Для цього завдання тобі знадобиться ноутбук\nКоли відкриєш ноут засунь сюди флешлку\n"
                                     "ФЛЕШКА ЦЕ ГОНЩИК ЗА РУЛЕМ БОЛІДА В МОЇЙ КІМНАТІ")
    elif msg.text.lower() == "675":
        bot.send_message(msg.chat.id,"Браво 👏\n"
                                     "49.8448438, 24.0345675\n"
                                     "Вирушай туди вже бо я вже зачекався\nРекомендую взяти шось більш повсякденне або спортивне\n"
                                     "Після нашого побачення напиши в чат 'іба чотко' і отримаєш нове завдання  ")
    elif msg.text.lower() == "іба чотко":
        send_question(msg, 0)
    elif msg.text.lower() == "код":
        last_quest(msg)



    else:
        bot.send_message(msg.chat.id,"Шукай уважніше")


def send_question(msg, q_index=0):
    q = questions[q_index]

    if q_index == 0:
        bot.send_message(msg.chat.id, "📝 Наступне завдання - це опитування!\nВідповідай правильно 😉")

    # Створюємо кнопки
    markup = types.InlineKeyboardMarkup()
    for text, correct in q["buttons"]:
        callback = f"{q_index}_{'right' if correct else 'wrong'}"
        markup.add(types.InlineKeyboardButton(text, callback_data=callback))

    # Відправка фото групою (media group)
    try:
        if len(q["photos"]) > 1:
            # Створюємо медіа-групу
            media = []
            for i, photo in enumerate(q["photos"]):
                if i == 0:
                    # Перше фото з підписом
                    media.append(types.InputMediaPhoto(open(photo, "rb"), caption=q["caption"]))
                else:
                    # Інші фото без підпису
                    media.append(types.InputMediaPhoto(open(photo, "rb")))

            # Відправляємо групу фото
            bot.send_media_group(msg.chat.id, media)

            # Відправляємо кнопки окремим повідомленням
            bot.send_message(msg.chat.id, "Обери відповідь:", reply_markup=markup)
        else:
            # Якщо одне фото - відправляємо як раніше
            bot.send_photo(msg.chat.id, open(q["photos"][0], "rb"), caption=q["caption"], reply_markup=markup)

    except FileNotFoundError as e:
        bot.send_message(msg.chat.id, f"❌ Помилка: файл не знайдено\n{e}")

# Обробка відповіді
@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    bot.answer_callback_query(call.id)


    q_index, result = call.data.split("_")
    q_index = int(q_index)

    if result == "right":
        bot.send_message(call.message.chat.id, "✅ Правильно!")

        if q_index + 1 < len(questions):
            send_question(call.message, q_index + 1)
        else:
            bot.send_message(call.message.chat.id, "🎉 Всі питання пройдено!")
    else:
        bot.send_message(call.message.chat.id, "❌ Неправильно, спробуй ще раз.")

def last_quest(msg):
        bot.send_message(msg.chat.id,"Супер перейдемо до останього завдання напиши кодд ")
        if msg.text.lower() == "кодд":
            bot.send_message(msg.chat.id,"вітаю ти заврлшп")





bot.polling(none_stop=True)
