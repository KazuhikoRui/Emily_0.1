import amino
import os
import time
import random
from Arts import Arts


#------Инициализация------#
mail = os.environ.get('E_NAME')
passw = os.environ.get('E_PASS')

client = amino.Client()
client.login(email=mail, password=passw) 
sub_client = amino.SubClient(comId='156542274', profile=client.profile)
reloadTime = time.time() + 197



print('Готова потрудиться!')
#------Иные функции------#



#------Код бота------#
names = ['эмили','эми', 'эми,']
hello = ['Ну, привет...', 'Отвали', 'Я занята', 'О боже, достали...']
friends = ['a1ffbd29-f7d6-46a8-9916-1386fd178c1f']
G_list = ['геншин','genshin', 'ganyu', 'diluc', 'diona', 'klee', 'xiao', 'hutao', 'zhongli', 'kaeya', 'mona', 'barbara', 'lisa', 'childe', 'venti','tartaglia', 'albedo', 'ayaka', 'rosaria']

def on_message(data):
  chatId = data.message.chatId
  content = data.message.content
  content = str(content).split(' ')
  
  #------Привет------#
  try:
    if content[0].lower() in names and "привет" in content[1].lower():
      if data.message.author.userId == '2bea0bed-ca93-4e67-9480-017a3572e3a7':
        sub_client.send_message(message="~Здравствуйте, хозяин...", chatId=chatId)
      elif data.message.author.userId in friends:
        sub_client.send_message(message="И вам здравствуйте!", chatId=chatId)
      else:
        sub_client.send_message(message=random.choice(hello), chatId=chatId)
  except:
    pass
      
  #------Артики------#
  try:
    if content[0].lower() in names and "артик" in content[1].lower():
      if data.message.author.userId == '2bea0bed-ca93-4e67-9480-017a3572e3a7' or data.message.author.userId in friends: 
        sub_client.send_message(message='Уже ищу!', chatId=chatId)
        Arts(' '.join(content[2:]).lower(), 50)
        with open('out.jpg', 'rb') as file:
          sub_client.send_message(chatId=chatId, file=file,fileType="image")
        os.remove("out.jpg")
      elif content[2].lower() in G_list:
        sub_client.send_message(message='Жди...', chatId=chatId)
        Arts("genshin" + content[2].lower(), 80)        
        with open('out.jpg', 'rb') as file:
          sub_client.send_message(chatId=chatId, file=file,fileType="image")
        sub_client.send_message(message='Подавись...', chatId=chatId)
        os.remove(".jpg")

  except:
     sub_client.send_message(message='Что-то не так...', chatId=chatId)


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
        except:pass
        print("### И снова в бой!... ###")
        reloadTime += 197
