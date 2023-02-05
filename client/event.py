import sys,os
sys.path.append(os.path.join(sys.path[0],'..'))
from schedule.schedule import Scarecrow
from time import sleep
import threading

import sys,os
sys.path.append(os.path.join(sys.path[0],'..'))
from schedule.schedule import Scarecrow
from database import DB
from message_func import send_message_user
__CONF__= ('number', 'time', 'cabinet', 'lesson' , 'teacher'), ('(&)', ' [&]', ' |&| ', '&',' - &')



def Wcache(object,fn = 'schedule.cache'):
  open(f'{fn}', 'w').write(object)
  
def Rcache(fn = 'schedule.cache') -> str:
  return open(f'{fn}', 'r').read()

def listen(cooldown : int = 60):
    while True:
        yield Scarecrow('1ИСИП-21-9').get_information()
        sleep(cooldown)

def mailing_handler(id_group):
    id,group = id_group[0],id_group[-1]
    schedule = Scarecrow(group,__CONF__).get_text()
    send_message_user(id,schedule)

def run():
  for pre_cache in listen(30):
    cache = Rcache()
    if pre_cache != cache:
      ids = DB().mail_idlist()
      for data in ids:
        threading.Thread(target=mailing_handler,args = [data]).start()
        Wcache(pre_cache)
    else:
      Wcache(pre_cache) # Записываем кэш

if __name__ == "__main__":
  run()

