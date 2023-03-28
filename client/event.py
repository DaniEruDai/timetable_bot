import sys,os
sys.path.append(os.path.join(sys.path[0],'..'))
from message_func import send_message_user
import time
import logging
from schedule.Timetable import TimeTable,write_json,get_dict,read_json
from database import DB

json_filename = 'timetable.json'
logging.basicConfig(filename='events.log',format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,encoding='utf-8')


def listener(couldown : str = 120):
  while True:
    try:
      yield get_dict()
    except Exception as e: logging.critical(f'Произошла ошибка {e}')
    time.sleep(couldown)
 
def main():
  for temp_dictionary in listener():
    try:
      non_temp_dictionary = read_json(json_filename)
    except FileNotFoundError: 
      logging.exception("Файл не найден, будет произведена перезапись")
      write_json(json_filename,temp_dictionary)
      logging.info('JSON перезаписан')
      non_temp_dictionary = read_json(json_filename)
      
    #Обновление JSON при несовпадении
    if temp_dictionary != non_temp_dictionary:
      logging.info('Перезапись JSON')
      write_json(temp_dictionary)
      logging.info('JSON перезаписан')
      
      
    #Рассылка по пользователям       
    for user_id,default,config in DB('data.db').get_all_ids_for_broadcast():
      print(config)
      # send_message_user(user_id,TimeTable('timetable.json',default=default,config_string=config))
      
DB('data.db').init_new_user(435170678)
# if __name__ == '__main__':
  
#   main()

