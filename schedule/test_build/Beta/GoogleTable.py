import requests
import numpy as np
import csv,io
from dataclasses import dataclass
from itertools import chain

@dataclass
class IndexObject:
  row : int
  column : int

class Table(list):

  def get_index(self,word) :
    l = np.array(self)
    index = np.argwhere(l == word).tolist()
    if len(index) == 0: return None
    return IndexObject(column = index[0][0],row=index[0][1])

def get_table(tableid: str, gid: str = '0', encoding: str = 'utf-8') -> Table:
  
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
