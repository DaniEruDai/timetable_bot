import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkApi

import threading

import inspect
import types
import requests
import sqlite3

class _builder:
  """
Пустой класс в который передаются функции для исполнения
  """
  @staticmethod
  def add_to_loop(_object : object):
    if isinstance(_object,types.FunctionType):
      setattr(_builder,str(_object),_object)
    else :
      funcs = [func for func in _object.__dict__.values() if inspect.isfunction(func) and func != _builder.add_to_loop]
      for function in funcs:
        setattr(_builder,str(function),function)

class _database:

  def __init__(self,__table_name : str, __user_id : str, __conn = None) -> None:
    self.__conn = __conn
    self.__cur = self.__conn.cursor()
    
    self.__cur.execute("""CREATE TABLE IF NOT EXISTS user(id INT,state TEXT, mailing TEXT,object TEXT,config TEXT,ruobr_login TEXT, ruobr_password TEXT);""")
    self.__conn.commit()
    
    self.__table_name = __table_name
    self.__user_id = __user_id
  
  def get_titles(self) -> list:
    self.__cur.execute(f'PRAGMA table_info({self.__table_name})')
    titles = [i[1] for i in self.__cur.fetchall()]
    return titles 
  
  def update_field(self, user_id : int | str = None, category : str = None,  new : str = None):
    id = user_id if user_id else self.__user_id
    
    self.__cur.execute(f"""UPDATE {self.__table_name} set {category} = '{new}' where id = {id}""")
    self.__conn.commit()

  def get_information(self, __user_id : int | str = None )-> dict:
    id = __user_id if __user_id else self.__user_id
    
    self.__cur.execute(f"""SELECT * from {self.__table_name} where id = {id}""")
    values = self.__cur.fetchone()
    
    self.__cur.execute(f'PRAGMA table_info({self.__table_name})')
    titles = [i[1] for i in self.__cur.fetchall()]
    
    dictionary = {}
    
    
    for title,value in zip(titles,values):
      dictionary[title] = value
    return dictionary

  def _init_new_user(self, __user_id : int | str = None):
    id = __user_id if __user_id else self.__user_id
    __CONFIG__ = "(number)[time]|cabinet| lesson - default |distance|/n"
    self.__cur.execute("""SELECT * from user """)
    id_list = [row[0] for row in self.__cur.fetchall()]
    if id not in id_list:
      self.__cur.execute(f"""INSERT INTO user (id,state,mailing,object,config,ruobr_login,ruobr_password) VALUES ('{id}' ,'main_menu','False','','{__CONFIG__}','','')""")
      self.__conn.commit()

  def delete_user(self, __user_id : int | str = None):
    id = __user_id if __user_id else self.__user_id
    self.__cur.execute(f"""DELETE from user where id = {id}""")
    self.__conn.commit()

  def set_state(self,__new_state: str = None,user_id : int | str = None):
    id = user_id if user_id else self.__user_id
    self.__cur.execute(f"""UPDATE user set state = '{__new_state}' where id = {id}""")
    self.__conn.commit()

  def get_users(self) -> list | None:
    self.__cur.execute(f"""SELECT * from {self.__table_name} """)
    result = [elem[0] for elem in self.__cur.fetchall()]
  
    if not result:
      return None
    return result

class _handlers:
  @staticmethod
  def state(*states: str) -> None:
    def inner(function):
      def wrapper(self):
        if self.state in states:
          return function(self)
      _builder.add_to_loop(wrapper)
      return wrapper
    return inner

  @staticmethod
  def message(*commands:str) -> None:
    def inner(function):
      def wrapper(self):
          if self.text in commands:
            return function(self)
      _builder.add_to_loop(wrapper)
      return wrapper
    return inner

  @staticmethod
  def multiply(commands : list[str], states : list[str])-> None:
    def inner(function):
      def wrapper(self):
        if self.state in states and self.text in commands:
          return function(self)
      _builder.add_to_loop(wrapper)
      return wrapper
    return inner

class _utils:

  def __init__(self, __token : str, __user_id : int | str) -> None:
    self.__vk = vk_api.VkApi(token=__token)
    self.__user_id = __user_id
  
  def __upload_document(self,__name, __buffer: str | bytes) -> str:
    vk = self.__vk.get_api()
    response = vk.docs.getMessagesUploadServer(type='doc', peer_id=self.__user_id)
    upload_url = response['upload_url']
    files = {'file': (f'{__name}.xlsx', __buffer.getvalue())}
    response = requests.post(upload_url, files=files)
    doc_data = response.json()
    doc = vk.docs.save(file=doc_data['file'], title=f'{__name}')
    attachment=f"doc{doc['doc']['owner_id']}_{doc['doc']['id']}"
    return attachment
  
  def send_message(self, __message : str = None ,user_id : int | str = None, keyboard:dict = None,url:str = None, file : list[str,bytes] = None):
    id = user_id if user_id else self.__user_id
    
    if url:
      url = f'link,{url}'
      
    if file and not url:
      name,buffer = file
      url = self.__upload_document(name,buffer)
    
      
    self.__vk.method('messages.send',{'user_id': int(id), 'message': __message, 'random_id': 0, 'keyboard' : keyboard,'attachment' : url})
  
  def get_fullname(self, user_id : int | str = None) -> str:
    id = user_id if user_id else self.__user_id
    user = self.__vk.method("users.get", {"user_ids": int(id)})
    fullname = f"{user[0]['first_name']} {user[0]['last_name']}"
    return fullname

class UserBot:

  def __init__(self, __file : str, __table_name : str, __token : str) -> None:
    self.__token = __token
    self.__table_name = __table_name
    #Открытие файла базы данных
    self.__conn = sqlite3.connect(f'{__file}',check_same_thread=False)
    #Инициализация хэндлеров
    self.on = _handlers()

  def __loop(self) -> None:
    
    #Запуск дополнительных утилит
    self.db = _database(self.__table_name,self.user_id,self.__conn)
    self.utils = _utils(self.__token, self.user_id)
    
    # Инициализация новых пользователей
    self.db._init_new_user()
    
    #Получение атрибутов для user_id по тэгам базы данных
    data = self.db.get_information()
    for name,value in data.items():
      setattr(UserBot,name,value)

    # Получение функций-обработчиков
    funcs = [func for func in _builder.__dict__.values() if inspect.isfunction(func)]
    for execute_function in funcs:
      execute_function(self)

  def Start(self) -> None:
    
    longpoll = VkLongPoll(vk_api.VkApi(token=self.__token)) 
    for event in longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        self.user_id = event.user_id
        self.text = event.text
        
        
        
        """ЗАПУСК ПОТОКА С ОБРАБОТЧИКАМИ"""
        threading.Thread(target=self.__loop).start()
