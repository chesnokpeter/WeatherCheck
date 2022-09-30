from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
import telebot
from telebot import types
import random
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
config_dict = get_default_config()
config_dict["language"] = "RU"
owm = OWM('a99967bc9ee70d5b4bd387902982f400')
mgr = owm.weather_manager()
bot = telebot.TeleBot("5707305838:AAE2OHw5EmcY_kHENwRWt8BVOzlivWtq4co")

fact = [
  "Атмосфера Земли имеет толщину 480 км и состоит из смеси около 16 газов",
  "Атмосфера делится на 5 слоёв: Тропосфера, Стратосфера, Мезосфера, Термосфера и Экзосфера",
  "По мере увеличения высоты атмосфера становится все тоньше и тоньше. Давление воздуха в экзосфере (самый высокий слой) чрезвычайно низкое из-за его большой высоты и расстояния между молекулами, которые у него есть",
  "Глобальный климат нагревался и охлаждался на протяжении всей истории. В настоящее время мы наблюдаем необычное быстрое потепление. Это происходит из-за парниковых газов, которые увеличиваются из-за человеческой деятельности, и они задерживают тепло в атмосфере",
  "Одной из самых важных вещей в атмосфере является озоновый слой. Это 19-32 км над поверхностью Земли. Это острый запах голубого газа, который поглощает большую часть ультрафиолетового излучения солнца",
  "Метеоры сгорают в холодной атмосфере Земли – слой мезосферы. Когда метеорит начинает входить в этот слой, он быстро натыкается на частицы мезосферы и царапает их. А поскольку скорость метеорита очень высока, он быстро генерирует большое количество тепла (из-за высокого трения между частицами мезосферы и метеором). Он начинает светиться",
  "Показатель преломления воздуха немного больше 1. Изменения показателя преломления могут привести к смешиванию световых лучей по длинным оптическим путям. Показатель преломления воздуха зависит от температуры. Эффекты преломления возрастают с увеличением градиента температуры. Мираж - прекрасный пример"
]

words_ = [
  "Хорошего дня:)\nУ тебя всё получится",
  "Приятного дня!",
  "Не забудь взять самое важное ^_^", 
  "Хорошего времяпровождения ^_^",
  "Прекрасного дня! :)"
]

print("Excellent!")

@bot.message_handler(commands=['start'])
def start_message(message):
	markup = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton("Искать", switch_inline_query_current_chat="")
	button2 = types.InlineKeyboardButton("Интересный факт!", callback_data='fact')
	markup.add(button1, button2)
	bot.send_message(message.chat.id, text="Привет, друг!\nЧтобы узнать погоду, нажми на кнопку ниже\nИ вводи любой город России\nБот сам предложит тебе нужный город", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.data == 'fact':
		nummes1 = random.randint(0, 6)
		bot.send_message(call.message.chat.id, fact[nummes1])

@bot.inline_handler(lambda query: len(query.query) > 2)
def query_text(inline_query):
        ntt = inline_query.query
        response = requests.get(f'http://k92900u9.beget.tech/api.php?q={ntt}&limit=5', headers=headers)
        cities = response.json()
        label = []

        for citie in cities:
            print(citie)
            label.append(types.InlineQueryResultArticle(citie["id"], citie["name"], types.InputTextMessageContent(citie["name"])))

        bot.answer_inline_query(inline_query.id, label)

@bot.message_handler(commands=['check'])
def start_message(message):
	bot.send_message(message.chat.id, "Я работаю!")

@bot.message_handler(commands=['about'])
def start_message(message):
	bot.send_message(message.chat.id, "Этот бот создан для конкурса Sk Kids Challenge\nНад проектом работал:\n\n<chesnok/> 🧑🏻‍💻 — Разработка, тестирование\n(@chesnokpeter)\nАнтон 👾 — Наставник\n(https://vk.com/a_d_elec)")

@bot.message_handler(content_types=['text'])
def send_echo(message):		
	try:
		observation = mgr.weather_at_place(message.text)
		w = observation.weather
		temp = w.temperature('celsius')["temp"]
		wind = w.wind()['speed']

		if temp < 5:
			tips = "🧥 На улице холодно, Бот советует одеть куртку "

		elif temp > 25:
			tips = "👕 На улице достаточно жарко, Бот советует одеть майку"

		elif temp < -15:
			tips = "❄️ На улице очень холодно, "

		else:
			tips = "🌤 На улице комфортно"

		nummes2 = random.randint(0, 4)
		words = words_[nummes2]

		answer = f"⭐️ Выбран город: {message.text}\n\n☁️ Сейчас {w.detailed_status}\n💡 Температура: {round(temp, 1)}° С\n🌬 Скорость вертра: {round(wind, 0)} м/с\n\n{tips}\n\n{words}"

	except:
		answer = "Ошибка!"

	finally:
		bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)
