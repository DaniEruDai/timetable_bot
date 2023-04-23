from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('__additional_files__\\.env'))
import os

from schedule.kgtt.timetable import TimeTable,write_json,get_dict,read_json
from vk.database import DB

import vk_api

import logging
import threading
import time


logging.basicConfig(filename='events.log',format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,encoding='utf-8')

def send_message_user(user_id, message):
  session = vk_api.VkApi(token=os.getenv('__TOKEN__'))
  session.method('messages.send',{'user_id': user_id, 'message': message, 'random_id': 0})

def listener(__couldown : int = 120):
  while True:
    _new = get_dict()
    
    try:
      _old = read_json('timetable.json')
    except FileNotFoundError:
      write_json('timetable.json',get_dict())
      continue

    yield _old,_new
    time.sleep(__couldown)

def send_message_for_user(obj,default,config_string,user_id):
  text = TimeTable(obj,
                  default=default,
                  config_string=config_string).get_text()
  send_message_user(user_id,text)
  logging.info(f'Message sent to the user - |vk.com/id{user_id}| ({default})')

def __main__():
  database = DB('data.db')
  for old,new in listener():
    db_data =  database.get_all_ids_for_broadcast()
    if not db_data:
      logging.exception("IDs not found")
      continue

    for user_id,default,config in db_data :
      if old[default] != new[default]:
        threading.Thread(target=send_message_for_user,args=[new,default,config,user_id]).start()

    write_json('timetable.json', new)
    logging.info('JSON was update')

if __name__ == '__main__':
  __main__()
