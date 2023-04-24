import sqlite3
__CONFIG__ = "(number)[time]|cabinet| lesson - default |distance|/n"

class DB:

  def __init__(self, directory : str = 'data.db'):
    """
Эта функция инициализирует объект класса с подключением к базе данных SQLite, создает две таблицы "chat" и "user", если они еще не существуют, и получает курсор для этого соединения. Параметр 'directory' используется для указания пути к базе данных.
    """

    #Инициализация базы данных
    self.conn = sqlite3.connect(f'{directory}',check_same_thread=False)
    
    #Курсор
    self.cur = self.conn.cursor()
    
    #Создание таблицы для чатов
    self.cur.execute("""CREATE TABLE IF NOT EXISTS chat(id INT,object TEXT,config TEXT);""")
    #Создание таблицы для пользователей
    self.cur.execute("""CREATE TABLE IF NOT EXISTS user(id INT,state TEXT, mailing TEXT,object TEXT,config TEXT,ruobr_login TEXT, ruobr_password TEXT);""")
    #Закрепление изменений
    self.conn.commit()
    
  def _get_titles(self,table_name:str)-> list:
    self.cur.execute(f'PRAGMA table_info({table_name})')
    titles = [i[1] for i in self.cur.fetchall()]
    return titles  
    
  def update_field(self, id : int | str, table_name : str, category : str, new : str):
    """
Этот метод обновляет значение поля "category" в записи с указанным идентификатором (id) в таблице базы данных SQLite, переданной в параметре "table_name", на новое значение, переданное в параметре "new".
    """
    self.cur.execute(f"""UPDATE {table_name} set {category} = '{new}' where id = {id}""")
    self.conn.commit()

  def get_information_from(self, table_name: str, id : int | str)-> dict:
    """
Этот метод возвращает одну запись из таблицы базы данных SQLite с указанным идентификатором (id).
    """
    self.cur.execute(f"""SELECT * from {table_name} where id = {id}""")
    values = self.cur.fetchone()
    dictionary = {}
    
    for title,value in zip(self._get_titles(table_name),values):
      dictionary[title] = value
    return dictionary

  def init_new_chat(self, id : int | str):
    """
Этот метод добавляет новую запись в таблицу "chat" базы данных SQLite, если ее идентификатор (id) не существует в таблице.
    """
    self.cur.execute("""SELECT * from chat """)
    id_list = [row[0] for row in self.cur.fetchall()]
    if id not in id_list:
      self.cur.execute(f"""INSERT INTO chat (id,object,config) VALUES ('{id}','','{__CONFIG__}')""")
      self.conn.commit()

  def init_new_user(self, id : int | str):
    """
Этот метод добавляет новую запись в таблицу "user" базы данных SQLite, если ее идентификатор (id) не существует в таблице.
    """
    self.cur.execute("""SELECT * from user """)
    id_list = [row[0] for row in self.cur.fetchall()]
    if id not in id_list:
      self.cur.execute(f"""INSERT INTO user (id,state,mailing,object,config,ruobr_login,ruobr_password) VALUES ('{id}' ,'main_menu','False','','{__CONFIG__}','','')""")
      self.conn.commit()

  def delete_user(self,id : int | str):
    self.cur.execute(f"""DELETE from user where id = {id}""")
    self.conn.commit()

  def delete_chat(self,id : int | str):
    self.cur.execute(f"""DELETE from chat where id = {id}""")
    self.conn.commit()

  def swap_user_state(self,id : int | str ,new_state: str):
    """
Этот метод выполняет обновление записи в таблице "user" базы данных. Он меняет значение поля "state" на новое значение, переданное в параметре "new_state", где поле "id" равно значению, переданному в переменной "id"
    """
    self.cur.execute(f"""UPDATE user set state = '{new_state}' where id = {id}""")
    self.conn.commit()

  def get_all_ids_for_broadcast(self) -> list | None:
    self.cur.execute(f"""SELECT * from user where mailing = 'True' """)
    result = [(elem[0],elem[3],elem[4]) for elem in self.cur.fetchall() if elem[3] != '']
  
    
    if not result:
      return None
    return result

  def get_all_ids(self,table_name:str) -> list | None:
    self.cur.execute(f"""SELECT * from '{table_name}' """)
    result = [elem[0] for elem in self.cur.fetchall()]
  
    if not result:
      return None
    return result