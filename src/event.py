import os

from schedule.timetable import Timetable,get_dict
from schedule.tjson import *
from vk.database import DB

import vk_api
import vk_api.exceptions

import threading
import time

import logging 
logging.basicConfig(filename="/root/timetable_bot/src/event.log", format='%(asctime)s %(message)s', 
filemode='w')

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

  def __get_old(self) -> dict:
    try:
      return read_json(_json)
    except Exception:
      return {}

  def __get_new(self) -> dict:
    try:
      return get_dict()
    except Exception:
      return {}

  def __listener(self) -> tuple:
    time.sleep(self._reload_time)
    while True:
      old : dict = self.__get_old()
      new : dict = self.__get_new()
      yield old,new

  @staticmethod
  def __thread(user_id,default,config,obj):
    try:
      text = Timetable(obj,default,config).get_text()
      send_message(user_id, text)
    except vk_api.exceptions.ApiError as e:
      logging.exception(f"Ошибка доступа для {user_id} : {e}")
  
  def start(self):
    for old,new in self.__listener():
      mailing_data =  self.database.get_mailing_id()
      for user_id,default,config in mailing_data :
        if old.get(default) != new.get(default):
          threading.Thread(target=self.__thread,args=[user_id,default,config,new]).start()

        
      write_json(_json, new)

Event(1200).start()