import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard,VkKeyboardColor
import threading

import sys,os
sys.path.append(os.path.join(sys.path[0],'..'))
from schedule.schedule import Scarecrow
from database import DB
from message_func import send_message_user




DB().create_tables() # Создаем бд / Инициализируем таблицы user и chat
__GROUPS__ = Scarecrow('1ИСИП-21-9').allgr()
__CONF__= ('number', 'time', 'cabinet', 'lesson' , 'teacher'), ('(&)', ' [&]', ' |&| ', '&',' - &')

def default_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Подписаться', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Изменить', color=VkKeyboardColor.PRIMARY)
    
    
    return keyboard.get_keyboard()

class UserVk():
  
  def __init__(self):
    self.text, self.user_id =None, None
    self.stage = None
    self.group = None

  def handler_start(self):

    if self.stage == 0:
      send_message_user(self.user_id, 'Введите свою группу : ')
      DB().stage(self.user_id,1)

    if self.stage == 1:
      if self.text in __GROUPS__:
        DB().writer(self.user_id,'user','crowd',self.text)
        DB().stage(self.user_id,3)
        send_message_user(self.user_id, 'Рассылка включена!',self.key)
      else: 
        send_message_user(self.user_id, 'Попробуйте заново!')

  def handler_mail(self):
    if self.stage == 2 and self.text == 'Подписаться':
      DB().stage(self.user_id,3)
      send_message_user(self.user_id,'Вы подписались!', self.key)

    elif self.stage == 3 and self.text == 'Отписаться':
      DB().stage(self.user_id,2)
      send_message_user(self.user_id,'Вы отписались!', self.key)

    elif self.stage == 2 and self.text == 'Отписаться':
      send_message_user(self.user_id,'Вы не подписаны!', self.key)

    elif self.stage == 3 and self.text == 'Подписаться':
      send_message_user(self.user_id,'Вы уже подписаны!', self.key)

  def handler_change_group(self):
    if self.text == 'Изменить' and self.stage >2 :
      DB().stage(self.user_id,0)
      send_message_user(self.user_id,'Напишите что-нибудь для продолжения')

  def handler_schedule(self):
    def schedule(user_id:int,group:str):
      schedule = Scarecrow(group,__CONF__).get_text()
      send_message_user(user_id,schedule)
  

    if self.text == '!р' and self.stage > 2:
      threading.Thread(target=schedule,args=[self.user_id,self.group]).start()

  def run(self):
    longpoll = VkLongPoll(vk_api.VkApi(token=os.getenv('__TOKEN__')))
    for event in longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        self.user_id = event.user_id
        self.text = event.text
      
      
        DB().new_user(self.user_id)
        information = DB().information(self.user_id,'user')
        self.stage,self.group = information[1],information[-1]
        
        self.key = default_keyboard()
        
        self.handler_start()
        self.handler_mail()
        self.handler_change_group()
        self.handler_schedule()


if __name__ =="__main__":
  UserVk().run()