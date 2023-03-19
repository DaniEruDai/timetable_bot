import requests
import numpy as np
import csv,io
from dataclasses import dataclass
from aiohttp import ClientSession
import asyncio

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

def get_table(tableid: str, gid: str = '0', encoding: str = 'utf-8') -> Table:
  """
Эта функция используется для получения данных из Google Sheets таблицы и преобразования их в объект класса Table.
  """
  __URL = f'https://docs.google.com/spreadsheets/d/{tableid}/gviz/tq?tqx=out:csv&sheet&gid={gid}'
  
  request = requests.get(__URL).content
  file = io.StringIO(request.decode(encoding=encoding))
  csv_data = csv.reader(file, delimiter=",") 
  rows = [row for row in csv_data]

  columns = []
  for index in range(len(max(rows))):
    column = [row[index] for row in rows]
    columns.append(column)
  
  return Table(columns)




