import os
import types

import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType

import threading
import inspect
from vk.database import DB

def add_to_loop(_object : object):
  if isinstance(_object,types.FunctionType):
    setattr(_builder_,str(_object),_object)
  else :
    funcs = [func for func in _object.__dict__.values() if inspect.isfunction(func)]
    for function in funcs:
      setattr(_builder_,str(function),function)

def send_message(user_id : int, message : str, keyboard:dict = None,url:str = None):
  session = vk_api.VkApi(token=os.getenv('__TOKEN__'))
  if url:
    url = f'link,{url}'
  session.method('messages.send',{'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard' : keyboard,'attachment' : url})

def get_fullname(id) -> str:
  vk = vk_api.VkApi(token=os.getenv('__TOKEN__'))
  user = vk.method("users.get", {"user_ids": id}) # вместо 1 подставляете айди нужного юзера
  fullname = f"{user[0]['first_name']} {user[0]['last_name']}"
  
  return fullname

def state_handler(*state: str):
  def inner(function):
    def wrapper(self):
      if self.state in state:
        return function(self)
    add_to_loop(wrapper)
    return wrapper
  return inner

def message_handler(*commands:str):   
  def inner(function):
    def wrapper(self):
        if self.text in commands:
          return function(self)
    add_to_loop(wrapper)
    return wrapper
  return inner

def multiply_handler(commands : list[str], states : list[str]):
  def inner(function):
    def wrapper(self):
      if self.state in states and self.text in commands:
        return function(self)
    add_to_loop(wrapper)
    return wrapper
  return inner

def fix_timeout_error(function):
  def inner(*args, **kwargs):
    while True:
      try:
        return function(*args,**kwargs)
      except Exception:
        pass
  return inner

class CtxStorage():
  """
Данный класс CtxStorage представляет собой простой механизм хранения данных, доступных в рамках контекста выполнения программы.
  """
  @staticmethod
  def set(name : str , value : object):
    setattr(CtxStorage,str(name),value)

  @staticmethod
  def delete(name : str):
    delattr(CtxStorage,str(name))
  
  @staticmethod
  def get(name : str):
    return getattr(CtxStorage,str(name))

class _builder_():
  ...

class StartBot():

  def __init__(self) -> None:
    self.text = None
    self.user_id = None
    self.state = None
    self.object = None
    self.ctx_name : str = None
    self.ctx_ruobr_login : str = None
    self.ctx_ruobr_password : str = None
    self.__run_bot()


  def __main_loop(self) -> None:

    self.ctx_name = f'attr{self.user_id}'
   
    # Инициализация базы данных
    database = DB('data.db') 
    
    # Инициализация новых пользователей
    database.init_new_user(self.user_id) 
    
    # Получение информации о пользователе
    information = database.get_information_from('user',self.user_id)
    
    # Перезапись данных пользователя из базы данных
    self.state,self.object,self.config = information['state'],information['object'],information['config']
    self.ruobr_login,self.ruobr_password = information['ruobr_login'],information['ruobr_password']
    
    # Получение функций класса BOT для исполнения
    funcs = [func for func in _builder_.__dict__.values() if inspect.isfunction(func)]
    for execute_function in funcs:
      execute_function(self)

  @fix_timeout_error
  def __run_bot(self)-> None:
    
    longpoll = VkLongPoll(vk_api.VkApi(token=os.getenv('__TOKEN__')))
    for event in longpoll.listen():
      if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        self.user_id = event.user_id
        self.text = event.text
        threading.Thread(target=self.__main_loop).start()
