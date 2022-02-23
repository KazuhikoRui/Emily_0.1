import aminofix
import os
import time
import random
from aiogram import Bot, Dispatcher, executor, types
import threading
import schedule



mail = os.environ.get('E_NAME')
passw = os.environ.get('E_PASS')
chats = [os.environ.get('RP'),os.environ.get('Flood'),os.environ.get('Ank')]

print('Готова потрудиться!')

client = aminofix.Client()

#---------Набор функций--------

def log(botLog, botPass):
	client.login(botLog, botPass)
	sub_client = aminofix.SubClient(comId=os.environ['ComID'], profile=client.profile)
	return sub_client
	
def unlog():
	client.logout()
	
def clearing(sub_client):
	i=0
	for chat in chats:
		msgs=sub_client.get_chat_messages(chatId=chat, size = 30)
		for msgC, msgT, msgCon, msgA in zip(msgs.type, msgs.messageId, msgs.content, msgs.author.userId):
			if (msgC in [56, 57, 58, 108, 109, 110] and msgCon != None) or (sub_client.get_user_info(msgA).level == 1 and msgCon != None):
				sub_client.delete_message(chatId=chat, messageId=msgT)
				i+=1
			else: 
				pass
		return i

def autoclean():
	sub_client = log(mail, passw)
	out=clearing(sub_client)
	unlog()
	times+=1
	
#---------Телега--------

times = 0

bot = Bot(token = os.environ.get('Token'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def hi_func(message: types.Message):
	await message.answer("Здравствуйте, хозяин!\nГотова потрудиться!")

@dp.message_handler(commands=['очистка'])
async def clear(message: types.Message):
	await message.answer("Начинаю проверку чатов...")
	sub_client = log(mail, passw)
	out=clearing(sub_client)
	if out == 0:
		await message.answer("Системные собщения не найдены")
	else:
		await message.answer(f"Удалено: {out} системных сообщений")
	unlog()

@dp.message_handler(commands=['счетчик'])
async def chet(message: types.Message):
	await message.answer(f"Было произведено {times} проверок")
	
def start_schedule_():
    schedule.every(30).minutes.do(autoclean)

    while True:
        schedule.run_pending()


t = threading.Thread(target=start_schedule_, name="Thread")
t.start()	
executor.start_polling(dp, skip_updates=True)
