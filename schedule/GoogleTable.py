import requests
import numpy as np
import csv,io
from dataclasses import dataclass
from aiohttp import ClientSession
import openpyxl

@dataclass
class IndexObject:
  """
Датакласс IndexObject определяет объект, содержащий индексы строки и столбца для определенного элемента таблицы.
\nЭто может быть полезно, когда необходимо получить доступ к конкретному элементу в таблице, и иметь возможность быстро получить его координаты.
  """
  row : int
  column : int

class Table(list):

  def get_index(self,word) :
    """
Метод используется для поиска индекса (номера строки и столбца) первого вхождения заданного слова в объекте Table.
    """
    l = np.array(self)
    index = np.argwhere(l == word).tolist()
    if len(index) == 0: return None
    return IndexObject(column = index[0][0],row=index[0][1])

def get_table(worksheet_name : str ):
  """
Эта функция используется для получения данных из Google Sheets таблицы и преобразования их в объект класса Table.
  """
  __URL = f'https://docs.google.com/spreadsheets/u/0/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/export?format=xlsx&id=1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU'

  request = requests.get(__URL).content
  file = io.BytesIO(request)
  
  # Открытие файла Excel
  workbook = openpyxl.load_workbook(file)
  
  # Выбор листа с нужными строками
  ws = workbook[worksheet_name]
  
  # Обход выбранных строк и получение значений ячеек
  all_columns = []
  for column in ws.iter_cols():
    column_data = []
    for cell in column:
      value = cell.value
      if isinstance(value,float):
        value = int(value)
      
      elif value is None:
        value = ''
        

      column_data.append(str(value))
    all_columns.append(column_data) 
  return all_columns

