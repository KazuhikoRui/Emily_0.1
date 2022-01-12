import aminofix
import os
import time
import random

#------Инициализация------#
mail = os.environ.get('E_NAME')
passw = os.environ.get('E_PASS')
chats = [os.environ.get('RP'),os.environ.get('Flood'),os.environ.get('Ank')]

client = aminofix.Client()
client.login(mail, passw)
sub_client = aminofix.SubClient(comId=os.environ['ComID'], profile=client.profile)

reloadTime = time.time() + 197
print('Готова потрудиться!')


def on_message(data):
	print(data.message.author.nickname, data.message.content, data.message.chatId)
	
	if data.message.type == 101 and sub_client.get_user_info(data.message.author.userId).level < 6:
		sub_client.kick(userId=data.message.author.userId, chatId=data.message.chatId, allowRejoin = False)
	if data.message.type in [56, 57, 58, 108, 109, 110, 101, 102] and data.message.content != None:
		sub_client.delete_message(chatId=data.message.chatId, messageId=data.message.messageId)
	
methods = []
for x in client.chat_methods:
	methods.append(client.event(client.chat_methods[x].__name__)(on_message))


#------Перезагрузка сокета------#
while True:
	if time.time() >= reloadTime:
		print("### Перезагружаюсь!... ###")
		try:
			client.socket.close()
			client.socket.start()
		except:pass
		print("### И снова в бой!... ###")
		reloadTime += 197
