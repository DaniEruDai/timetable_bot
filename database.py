import sqlite3

class DB:

  def __init__(self):
    """Создание файла"""
    self.conn = sqlite3.connect('data.db')
    self.cur = self.conn.cursor()
  
  def create_tables(self):
    self.cur.execute("""CREATE TABLE IF NOT EXISTS chat(id INT,crowd TEXT);""")
    self.cur.execute("""CREATE TABLE IF NOT EXISTS user(id INT,stage INT,crowd TEXT);""")
    self.conn.commit()

  def writer(self,id,table_name,category,new):
    self.cur.execute(f"""UPDATE {table_name} set {category} = '{new}' where id = {id}""")
    self.conn.commit()

  def information(self,id,table_name):
    self.cur.execute(f"""SELECT * from {table_name} where id = {id}""")
    return self.cur.fetchone()
  
  """Для таблицы chat"""
  def new_chat(self,id):
    self.cur.execute("""SELECT * from chat """)
    id_list = [row[0] for row in self.cur.fetchall()]
    if id not in id_list:
      self.cur.execute(f"""INSERT INTO chat (id,crowd) VALUES ('{id}','')""")
      self.conn.commit()
  
  """Для таблицы user"""
  
  def mail_idlist(self):
    self.cur.execute(f"""SELECT * from user where stage = 3""")
    massive = self.cur.fetchall()
    return [(id[0],id[-1]) for id in massive]


  def new_user(self,id):
    self.cur.execute("""SELECT * from user """)
    id_list = [row[0] for row in self.cur.fetchall()]
    if id not in id_list:
      self.cur.execute(f"""INSERT INTO user (id,stage,crowd) VALUES ('{id}' ,0, '')""")
      self.conn.commit()
  
  def stage(self,id,stage):
    self.cur.execute(f"""UPDATE user set stage = {stage} where id = {id}""")
    self.conn.commit()

  def delete_user(self,id):
    self.cur.execute(f"""DELETE from user where id = {id}""")
    self.conn.commit()
    
