import amino
import os
import time
import random
from Arts import Arts
from google_images_download import google_images_download 
import shutil
import json




#------Инициализация------#
mail = os.environ.get('E_NAME')
passw = os.environ.get('E_PASS')

client = amino.Client()
client.login(email=mail, password=passw) 
sub_client = amino.SubClient(comId='156542274', profile=client.profile)
reloadTime = time.time() + 197



print('Готова потрудиться!')
#------Иные функции------#

def G_art(Req):
	response = google_images_download.googleimagesdownload()   
	arguments = {"keywords":Req,"limit":5,"print_urls":False, "size":'medium'}   
	paths = response.download(arguments)
	
def ImportAnks(Id,Url):
	m={}
	with open('Anks.json', 'r') as j:
		m = json.load(j)
		j.close()
	m[len(m)] = {'id': Id,'url': Url}
	with open('Anks.json', 'w') as j:
		j.write(json.dumps(m))
		j.close()

def DoneAnks(Url):
	m={}
	with open('Anks.json', 'r') as j:
		m = json.load(j)
		j.close()
	for i in range(0,len(m)):
		if m[str(i)]['url'] == Url:
			for j in range(i,len(m)-1):
				m[str(j)]=m[str(j+1)]
			del m[str(len(m)-1)]
			break
	with open('Anks.json', 'w') as j:
		j.write(json.dumps(m))
		j.close()

def CheckAnks(Url):
	m={}
	with open('Anks.json', 'r') as j:
		m = json.load(j)
		j.close()
	if len(m)==0:
		return 1
	for i in range(0,len(m)):
		if m[str(i)]['url'] == Url:
			return 0
		else: 
			return 1

def ListAnks():
	m={}
	a=''
	with open('Anks.json', 'r') as j:
		m = json.load(j)
		j.close()    
	for i in range(0,len(m)):
		a = a+'\n'+(m[str(i)]['url'])
	return a

def addAnketol(Id, Url):
	m={}
	with open('Anketol.json', 'r') as j:
		m = json.load(j)
		j.close()
	m[Id] = {'Url': Url}
	with open('Anketol.json', 'w') as j:
		j.write(json.dumps(m))
		j.close()

def remAnketol(Id):
	m={}
	with open('Anketol.json', 'r') as j:
		m = json.load(j)
		j.close()
	del m[Id]
	with open('Anketol.json', 'w') as j:
		j.write(json.dumps(m))
		j.close()

def loadAnketol():
	m = {}
	with open('Anketol.json', 'r') as j:
		m = json.load(j)
		j.close()
	return m

#------Код бота------#
names = ['эмили','эми', 'эми,']
hello = ['Ну, привет...', 'Отвали', 'Я занята', 'О боже, достали...']
friends = ['a1ffbd29-f7d6-46a8-9916-1386fd178c1f']
G_list = ['геншин','genshin', 'ganyu', 'diluc', 'diona', 'klee', 'xiao', 'hutao', 'zhongli', 'kaeya', 'mona', 'barbara', 'lisa', 'childe', 'venti','tartaglia', 'albedo', 'ayaka', 'rosaria']
anketol = loadAnketol()

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
		pass
     
	try:
		if content[0].lower() in names and "гарт" in content[1].lower():
			ROOT_DIR = os.path.dirname(os.path.abspath(__file__))+'//downloads'
			
			if data.message.author.userId == '2bea0bed-ca93-4e67-9480-017a3572e3a7' or data.message.author.userId in friends: 
				sub_client.send_message(message='Уже ищу!', chatId=chatId)
				G_art(' '.join(content[2:]).lower())
				dir_path = ROOT_DIR+'//'+' '.join(content[2:]).lower()
				with open(dir_path+'//'+random.choice(os.listdir(dir_path)), 'rb') as file:
					sub_client.send_message(chatId=chatId, file=file,fileType="image")
				shutil.rmtree(ROOT_DIR)
			elif content[2].lower() in G_list:
				sub_client.send_message(message='Жди...', chatId=chatId)
				G_art("genshin " + content[2].lower())
				dir_path = ROOT_DIR+'//genshin '+content[2].lower()       
				with open(dir_path+'//'+random.choice(os.listdir(dir_path)), 'rb') as file:
					sub_client.send_message(chatId=chatId, file=file,fileType="image")
				sub_client.send_message(message='Подавись...', chatId=chatId)
				shutil.rmtree(ROOT_DIR)
	except:
		pass
		
#------Анкеты------#
	try:
		if data.message.content == None and data.message.type == 101 and chatId == '58d4efe8-0283-4b61-a431-e19648902391':
			sub_client.send_message(message=f"<$@{data.message.author.nickname}$> Ну привет... Если хочешь подать анкету на проверку, то отправь мне команду:\nЭми анка [Ваша ссылка на анкету]",mentionUserIds=[data.message.author.userId], chatId = chatId)
	except:
		pass

	try:
		if content[0].lower() in names and "анка" in content[1].lower() and chatId == '58d4efe8-0283-4b61-a431-e19648902391':
			if content[2][0].lower() == 'h':
				if CheckAnks(content[2].lower()):
					ImportAnks(data.message.author.userId,content[2].lower())
					sub_client.send_message(message="Добавила анкету в очередь!", chatId=chatId, replyTo = data.message.messageId)
				else:
					sub_client.send_message(message="Анкета уже в очереди на проверку!", chatId=chatId, replyTo = data.message.messageId)
			else:
				sub_client.send_message(message="Неверная ссылка на анкету.", chatId=chatId, replyTo = data.message.messageId) 
	except:
		pass   	

	
	try:
		if content[0].lower() in names and "проверено" in content[1].lower() and chatId == '58d4efe8-0283-4b61-a431-e19648902391' and data.message.author.userId in anketol:
			if content[2][0].lower() == 'h':
				DoneAnks(content[2].lower())
				sub_client.send_message(message="Анкета успешно проверена!", chatId=chatId, replyTo = data.message.messageId)
			else:
				sub_client.send_message(message="Неверная ссылка на анкету.", chatId=chatId, replyTo = data.message.messageId)  
	except:
		pass	
	
	try:
		if content[0].lower() in names and "список" in content[1].lower() and chatId == '58d4efe8-0283-4b61-a431-e19648902391':
			sub_client.send_message(message=(f"Вот список:{ListAnks()}"), chatId=chatId, replyTo = data.message.messageId)
	except:
		pass
	
	
	try:
		if content[0].lower() in names and "добанк" in content[1].lower() and data.message.author.userId == '2bea0bed-ca93-4e67-9480-017a3572e3a7':
			if content[3][0].lower() == 'h':
				addAnketol(content[2].lower(), content[3].lower())
				sub_client.send_message(message="Анкетолог успешно добавлен!", chatId=chatId, replyTo = data.message.messageId)
			else:
				sub_client.send_message(message="Неверная ссылка.", chatId=chatId, replyTo = data.message.messageId) 
	except:
		pass
	
	try:
		if content[0].lower() in names and "убранк" in content[1].lower() and data.message.author.userId == '2bea0bed-ca93-4e67-9480-017a3572e3a7':
			if content[2][0].lower() == 'h':
				remAnketol(content[2].lower())
				sub_client.send_message(message="Анкетолог успешно убран!", chatId=chatId, replyTo = data.message.messageId)
			else:
				sub_client.send_message(message="Неверная ссылка.", chatId=chatId, replyTo = data.message.messageId) 
	except:
		pass
	
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
