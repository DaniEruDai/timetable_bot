from itertools import chain
import pandas as pd
import requests
import numpy as np

class TableExceptions:
  class VoidValue(Exception):
    ...

class table(list):

  def bindex(self,word) -> list:
    l = np.array(self)
    index = np.argwhere(l == word).tolist()

    if len(index) == 0:
      raise TableExceptions.VoidValue(f'{word} - совпадений не обнаружено')
    return index[0]

  def bindex_disexact(self,word) -> dict:
    l = np.array(self)
    coincident = [[ellement for ellement in row if word in ellement] for row in l.tolist()]
    coincident = set(chain(*coincident))
    
    if len(coincident) == 0: 
      raise TableExceptions.VoidValue(f'{word} - совпадений не обнаружено')
    
    dictionary = {}
    for group in coincident:
      index = np.argwhere(l == group).tolist()
      dictionary[group] = index
    return dictionary

class GoogleTable:

  def __init__(self, tableid: str, gid: str = '0', encoding: str = 'utf-8'):
      self.__tableid = tableid
      self.__URL = f'https://docs.google.com/spreadsheets/d/{self.__tableid}' \
                    f'/export?format=csv&id={self.__tableid}&gid={gid} '
      self.__df = pd.read_csv(self.__URL, keep_default_na=False, na_filter=False, encoding=encoding)

  def rows(self) -> table:
    rows = self.__df.values.tolist()
    return table(rows)

  def columns(self,column_names_as_first_ellement: bool = False) -> table:
    rows = self.__df.values.tolist()
    columns = []
    
    for index in range(len(max(rows))):
      column = [row[index] for row in rows]
      columns.append(column)
      
      if column_names_as_first_ellement:
        column.insert(0, self.__df.columns[index])
    return table(columns)

  def column_names(self) -> list:
      return self.__df.columns

  def tofile(self, filename: str = 'file', file_format: str = 'xlsx'):
      url = f'https://docs.google.com/spreadsheets/d/{self.__tableid}/export?format={file_format}&id={self.__tableid}'
      r = requests.get(url)
      with open(f'{filename}.{file_format}', 'wb') as f:
          f.write(r.content)


print(GoogleTable('1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU').columns().bindex_disexact('КСК'))







