import telebot
import config
import random


from telebot import types

bot = telebot.TeleBot(config.TOKEN)

user = bot.get_me()


@bot.message_handler(commands=['start'])
def welcome(message):

	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("🎲 Рандомное число")
	item2 = types.KeyboardButton("😊 Как дела?")
	item3 = types.KeyboardButton("®")

	markup.add(item1, item2, item3)

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == '🎲 Рандомное число':
			random_unit = str(random.randint(0,100))
			bot.send_message(message.chat.id, random_unit)
			f = open('random.txt', 'a')
			f.write(random_unit + '\n')
			f.close()

		elif message.text == '😊 Как дела?':

			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
			item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

			markup.add(item1, item2)

			bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)

		elif message.text == '®':
			bot.send_message(message.chat.id, '{0.last_name}'.format(message.from_user, bot.get_me()))
			bot.send_message(message.chat.id, '{0.first_name}'.format(message.from_user, bot.get_me()))
			bot.send_message(message.chat.id, '{0.id}'.format(message.from_user, bot.get_chat(message.chat.id)))
			bot.send_message(message.chat.id, bot.get_me())

		else:
			bot.send_message(message.chat.id, message.text)
			f = open('text.txt', 'a')
			f.write(message.text + ' ' + '{0.first_name}'.format(message.from_user, bot.get_me()) + ' ' + '{0.last_name}'.format(message.from_user, bot.get_me()) + '\n')
			f.close()

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Бывает 😢')

			# remove inline buttons
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
				reply_markup=None)

			# show alert
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

	except Exception as e:
		print(repr(e))




# RUN
bot.polling(none_stop=True)
