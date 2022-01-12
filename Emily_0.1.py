import aminofix
import os
import time
import random

#------Инициализация------#
mail = os.environ.get('E_NAME')
passw = os.environ.get('E_PASS')
chats = [os.environ.get('RP'),os.environ.get('Flood'),os.environ.get('Ank')]

client = aminofix.Client()
client.login(os.environ['Mail'], os.environ['Pass'])
sub_client = aminofix.SubClient(comId=os.environ['ComID'], profile=client.profile)

reloadTime = time.time() + 197
print('Готова потрудиться!')


def on_message(data):
	print(data.message.author.nickname, data.message.content, data.message.chatId)
	
	if data.message.type == 101 and sub_client.get_user_info(data.message.author.userId).level < 6:
		sub_client.kick(userId=data.message.author.userId, chatId=data.message.chatId, allowRejoin = False)
		sub_client.delete_message(chatId=data.message.chatId, messageId=data.message.messageId)
	
def check_chats():
	for name in chats:
		msgs=sub_client.get_chat_messages(name, size = 30)
		for msgC, msgT, msgCon, msgA in zip(msgs.type, msgs.messageId, msgs.content, msgs.author.userId):
			if (msgC in [56, 57, 58, 108, 109, 110] and msgCon != None) or (sub_client.get_user_info(msgA).level == 1 and msgCon != None):
				sub_client.delete_message(chatId=name, messageId=msgT)
			else:
				continue

methods = []
for x in client.callbacks.chat_methods:
	methods.append(client.callbacks.event(client.callbacks.chat_methods[x].__name__)(on_message))


#------Перезагрузка сокета------#
while True:
	if time.time() >= reloadTime:
		print("### Перезагружаюсь!... ###")
		try:
			client.socket.close()
			client.socket.start()
			methods = []
			check_chats()
		except:pass
		print("### И снова в бой!... ###")
		reloadTime += 197
