import sqlite3
string_config = str("(number)[time]|cabinet| lesson - default |distance|/n")


class DB:

  def __init__(self, directory : str = 'data.db'):
    """
Эта функция инициализирует объект класса с подключением к базе данных SQLite, создает две таблицы "chat" и "user", если они еще не существуют, и получает курсор для этого соединения. Параметр 'directory' используется для указания пути к базе данных.
    """

    #Инициализация базы данных
    self.conn = sqlite3.connect(f'{directory}')
    
    #Курсор
    self.cur = self.conn.cursor()
    
    #Создание таблицы для чатов
    self.cur.execute("""CREATE TABLE IF NOT EXISTS chat(id INT,crowd TEXT,config TEXT);""")
    #Создание таблицы для пользователей
    self.cur.execute("""CREATE TABLE IF NOT EXISTS user(id INT,stage INT,crowd TEXT,config TEXT);""")
    #Закрепление изменений
    self.conn.commit()
    
  def update_field_in_table(self, id : int | str, table_name : str, category : str, new : str):
    """
Этот метод обновляет значение поля "category" в записи с указанным идентификатором (id) в таблице базы данных SQLite, переданной в параметре "table_name", на новое значение, переданное в параметре "new".
    """
    self.cur.execute(f"""UPDATE {table_name} set {category} = '{new}' where id = {id}""")
    self.conn.commit()

  def get_information_from(self, table_name: str, id : int | str):
    """
Этот метод возвращает одну запись из таблицы базы данных SQLite с указанным идентификатором (id).
    """
    self.cur.execute(f"""SELECT * from {table_name} where id = {id}""")
    return self.cur.fetchone()

  def init_new_chat(self, id : int | str):
    """
Этот метод добавляет новую запись в таблицу "chat" базы данных SQLite, если ее идентификатор (id) не существует в таблице.
    """
    self.cur.execute("""SELECT * from chat """)
    id_list = [row[0] for row in self.cur.fetchall()]
    if id not in id_list:
      self.cur.execute(f"""INSERT INTO chat (id,crowd,config) VALUES ('{id}','','{string_config}'""")
      self.conn.commit()

  def init_new_user(self, id : int | str):
    """
Этот метод добавляет новую запись в таблицу "user" базы данных SQLite, если ее идентификатор (id) не существует в таблице.
    """
    self.cur.execute("""SELECT * from user """)
    id_list = [row[0] for row in self.cur.fetchall()]
    if id not in id_list:
      self.cur.execute(f"""INSERT INTO user (id,stage,crowd,config) VALUES ('{id}' ,0, '','{string_config}'""")
      self.conn.commit()

  def swap_user_stage(self,new_stage: int | str, id : int | str):
    """
Этот метод выполняет обновление записи в таблице "user" базы данных. Он меняет значение поля "stage" на новое значение, переданное в параметре "new_stage", где поле "id" равно значению, переданному в переменной "id"
    """
    self.cur.execute(f"""UPDATE user set stage = {new_stage} where id = {id}""")
    self.conn.commit()

  def get_all_ids_for_broadcast(self):
    self.cur.execute(f"""SELECT * from user where stage = 3""")
    return [(elem[0],elem[2],elem[3]) for elem in self.cur.fetchall()]
