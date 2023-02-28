import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import threading
import __init__
from schedule.schedule import Scarecrow
from database import DB

DB().create_tables() # Создаем бд / Инициализируем таблицы user и chat
__GROUPS__ = Scarecrow('1ИСИП-21-9').allgr()
__CONF__= ('number', 'time', 'cabinet', 'lesson' , 'teacher'), ('(&)', ' [&]', ' |&| ', '&',' - &')


class ChatVk:
  
  def __init__(self):
    self.session = vk_api.VkApi(token=os.getenv('__TOKEN__'))
    self.chat_id,self.text = None,None
    self.group = None

  def send_message_chat(self,chat_id, message):
    self.session.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': 0})

  def handler_configurator_group(self):
    if self.text.startswith('!группа_'):
      group = self.text.split('_')[-1]
      
      if group in __GROUPS__:
        DB().writer(self.chat_id,'chat','crowd',f'{group}')
        self.send_message_chat(self.chat_id,'Группа успешно обновлена!')
      else : self.send_message_chat(self.chat_id,'Группа не найдена')
    
    if self.text == '!группа':
      self.send_message_chat(self.chat_id,'Введите нужную группу после нижнего подчеркивания\nНапример :!группа_1ИСИП-21-9')

  def schedule(self,chat_id,group):
    schedule = Scarecrow(group,__CONF__).get_text()
    self.send_message_chat(chat_id,schedule)

  def handler_schedule(self):
    if self.text == '!р':
      if self.group != '':
        
        threading.Thread(target=self.schedule,args=[self.chat_id,self.group,]).start()
      else: 
        self.send_message_chat(self.chat_id,'Группа не выбрана\nВы можете настроить группу, написав : \n!группа_ВАША-ГРУППА')

  def run(self):
    longpoll = VkBotLongPoll(self.session, group_id=os.getenv('__GROUPID__'))
    for event in longpoll.listen():
      if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
        self.chat_id = event.chat_id
        self.text = event.message['text']
        self.group = DB().information(self.chat_id,'chat')[-1]
        
        DB().new_chat(self.chat_id) # Инициализация беседы внутри БД
        
        self.handler_configurator_group()
        self.handler_schedule()


if __name__ == "__main__":
  ChatVk().run()