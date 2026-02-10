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

'''
import telebot
from telebot import types

bot = telebot.TeleBot('token')

@bot.message_handler(commands=["start"])

def start(msg):
    bot.send_message(msg.chat.id,'Привіт сонце ❤️ \nТи ще заспана і напевне не розумієш шо робиться.'
                                 '\nЗараз я тобі все коротко поясню \nСьогодні день квестів для тебе, мене в гуртожитку вже немає і щоб мене знайти тобі треба пройти кілька завдань '
                                 'Кожне завдання це нова локація де я тебе буду чекати вони будуть протягом всьго дня і не вздумай знімати тіктоки перед виходом бо я все прорахував по часу\n(ЗАПІЗНИШСЯ НЕ ЗУСТРІНЕМОСЬ,БО Я БУДУ В ІНШОМУ МІСЦІ)'
                                 '\nПисати до мене теж марно я не відпишу,млжеш знімати відео як ти це проходиш або сісти з дівчатми проходити деякі завдання\n'
                                 'Пиши "Готова" і ми почнемо')
@bot.message_handler(content_types=["text"])
def first_qst(msg):
    if msg.text.lower() == "готова":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("вйо бо дощ",
                                              callback_data="send_zip"))
        bot.send_message(msg.chat.id,"(49.8448438, 24.0345???)\n Це локація першої нашої зустрічі\n"
                                     "Ти просто вставляєш це в гугл мепс і воно тобі видасть точку на карті\n"
                                     "Але як ти бачиш тут не вистачає трьох останніх цифр\nДля того щоб знайти ці цифри виконуй вказівки в повідомленні знизу")
        bot.send_message(msg.chat.id,"Для цього завдання тобі знадобиться ноутбук\nКоли відкриєш ноут зайди сюди і нажми кнопку знизу",
                         reply_markup=markup)
    elif msg.text.lower() == "675":
        bot.send_message(msg.chat.id,"Браво 👏\n"
                                     "Вирушай туди вже бо я вже зачекався\nРекомендую взяти шось більш повсякденне або спортивне\n"
                                     "Після нашого побачення напиши в чат 'іба чотко' і отримаєш нове завдання  ")
    else:
        bot.send_message(msg.chat.id,"Шукай уважніше")

        questions = [
            {
                "photos": ["files/f1_1.jpg", "files/f1_2.jpg", "files/f1_3.jpg"],
                "caption": "Моя улюблена команда в F1?",
                "buttons": [("McLaren", True), ("Ferrari", False), ("Mercedes", False)]
            },
            {
                "photos": ["files/q2.jpg"],
                "caption": "Яка перша команда вашого МУЩИНИ",
                "buttons": [("Тарпа (Угорщина)",True),("Динамо Львів", False), ("Скала Стрий", True)]
            },
            {

                "photos": ["files/f1_1.jpg", "files/f1_2.jpg", "files/f1_3.jpg"],
                "caption": "Моя улюблена команда в F1?",
                "buttons": [("McLaren", True), ("Ferrari", False), ("Mercedes", False)]
            }
        ]

        # Відправка питання
        def send_question(msg, q_index=0):
            q = questions[q_index]
            markup = types.InlineKeyboardMarkup()
            for text, correct in q["buttons"]:
                callback = f"{q_index}_{'right' if correct else 'wrong'}"
                markup.add(types.InlineKeyboardButton(text, callback_data=callback))

            for i, photo in enumerate(q["photos"]):
                if i == len(q["photos"]) - 1:
                    bot.send_photo(msg.chat.id, open(photo, "rb"), caption=q["caption"], reply_markup=markup)
                else:
                    bot.send_photo(msg.chat.id, open(photo, "rb"))

        # Обробка відповіді
        @bot.callback_query_handler(func=lambda call: True)
        def handle_answer(call):
            bot.answer_callback_query(call.id)
            q_index, result = call.data.split("_")
            q_index = int(q_index)

            if result == "right":
                bot.send_message(call.message.chat.id, "✅ Правильно!")
                # Наступне питання
                if q_index + 1 < len(questions):
                    send_question(call.message, q_index + 1)
                else:
                    bot.send_message(call.message.chat.id, "🎉 Всі питання пройдено!")
            else:
                bot.send_message(call.message.chat.id, "❌ Неправильно, спробуй ще раз.")


@bot.message_handler(content_types=["text"])
def next_qst(msg):
    if msg.text.lower() == "іба чотко":
        bot.send_photo(
            chat_id=msg.chat.id,
            photo=open("photo/iba_chotko.png", "rb"),
            caption="Наступне завдання це опитування"
        )


bot.polling(none_stop=True)
