import os

from schedule.timetable import Timetable,get_dict
from schedule.tjson import *
from vk.database import DB

import vk_api

import threading
import time

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('.env'))

_token = os.getenv('TOKEN')
_json = os.getenv('js_path')
_db = os.getenv('db_path')


def send_message(user_id : int, message : str):
  session = vk_api.VkApi(token=_token)
  session.method('messages.send',{'user_id': user_id, 'message': message, 'random_id': 0})

class Event:
  def __init__(self,_reload_time : int) -> None:
    self._reload_time = _reload_time
    self.database = DB(_db)

  def _listener(self):
    while True:
      try:
        old = read_json(_json) # Словарь из файла
      except FileNotFoundError:
        old = None
      
      new = get_dict() # Словарь из интернета
      yield old,new
      time.sleep(self._reload_time)
  
  @staticmethod
  def _thread(user_id,default,config,obj):
    try:
      text = Timetable(obj,default,config).get_text()
      send_message(user_id, text)
    except KeyError:
      pass

  def start(self):
    for old,new in self._listener():    
      mailing_data =  self.database.get_mailing_id()
      for user_id,default,config in mailing_data :
        try:
          if old[default] != new[default]:
            threading.Thread(target=self._thread,args=[user_id,default,config,new]).start()
        except TypeError:
          pass
        
      write_json(_json, new)

Event(30).start()