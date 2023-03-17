from itertools import chain
import requests
import numpy as np
import csv,io
from dataclasses import dataclass


class TableExceptions:
  class VoidValue(Exception):
    ...


@dataclass
class index_object:
  row : int
  column : int

class table(list):

  def bindex(self,word) -> index_object:
    l = np.array(self)
    index = np.argwhere(l == word).tolist()
    if len(index) == 0:
      raise TableExceptions.VoidValue(f'{word} - совпадений не обнаружено')
      
    return index_object(column = index[0][0],row=index[0][1])

  def bindex_disexact(self,word) -> dict:
    """TODO:Доработать"""
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
      self.__URL = f'https://docs.google.com/spreadsheets/d/{tableid}/gviz/tq?tqx=out:csv&sheet&gid={gid}'
      self.__table = self.__get_table__(encoding)

  def __get_table__(self,encoding:str = 'utf-8') -> list[list,list]: 
    request = requests.get(self.__URL).content
    file = io.StringIO(request.decode(encoding=encoding))
    csv_data = csv.reader(file, delimiter=",")
    result = [row for row in csv_data]
    return result

  def rows(self) -> table:
    return table(self.__table)

  def columns(self) -> table:
    rows = self.__table
    columns = []
    
    for index in range(len(max(rows))):
      column = [row[index] for row in rows]
      columns.append(column)
      
    return table(columns)

  def tofile(self, filename: str = 'file', file_format: str = 'xlsx'):
      url = f'https://docs.google.com/spreadsheets/d/{self.__tableid}/export?format={file_format}&id={self.__tableid}'
      r = requests.get(url)
      with open(f'{filename}.{file_format}', 'wb') as f:
          f.write(r.content)
