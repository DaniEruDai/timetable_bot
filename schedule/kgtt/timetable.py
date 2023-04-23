from ._students import get_dictionary_for_students
from ._teachers import get_dictionary_for_teachers

import os
import json,time




def get_dict() -> dict:
  return get_dictionary_for_students() | get_dictionary_for_teachers()

def read_json(filename:str = 'timetable.json') -> dict:
  with open(filename,'r',encoding='UTF-8') as js:
    json_data = json.loads(js.read())
    return json_data

def write_json(filename : str = 'timetable.json',dictionary : dict =  None) -> None:
  with open(filename,'w',encoding='UTF-8') as js:
    json.dump(obj=dictionary,
              fp = js,
              ensure_ascii=False,
              indent=4)

class TimeTable():
  
  def __init__(self,__object : str | dict, default:str,config_string : str = '(number)[time]|cabinet| lesson - default |distance|/n') -> None:
    self.object = __object
    self.config_string = config_string
    self.default = default

  def __get_clean_row(self)->str:
    string = self.config_string
    for value in ('default','lesson','cabinet' ,'time','number','distance'):
      if value in self.config_string:
        string = string.replace(value,"{"+str(value)+"}")
    string = string.replace('/n','\n')
    return string
    
  def __get_reverse_values(self)->list:
    values = []
    for value in ('default','lesson','cabinet' ,'time','number'):
      if value not in self.config_string:
        values.append(value)
        
    return values

  def __read_json_data(self) -> dict:
    if isinstance(self.object,str):
      with open(self.object,'r',encoding='UTF-8') as js:
        json_data = json.loads(js.read())
        return json_data
    else: return self.object
      
  @staticmethod
  def __get_creation_date() -> str:
    created_time = os.path.getmtime('timetable.json')
    created_time_str = time.strftime('%d.%m.%Y в %H:%M:%S', time.localtime(created_time))
    return created_time_str

  def get_text(self) -> str:
    
    json_data : dict = self.__read_json_data()[self.default]
    if json_data is None: return f'Расписание для {self.default} отсутствует,\nприятного отдыха!'
    
    
    for key in self.__get_reverse_values():
      del json_data[key]
    

    rows = ''
    keys = list(json_data.keys())
    for value in zip(*json_data.values()):
      format_dict = {k:v for k, v in zip(keys, value)}
      row = self.__get_clean_row().format(**format_dict)
      
      
      void_counter = len([i for i in list(format_dict.values())[:-1] if i == ''])
      el_counter = len([i for i in list(format_dict.values())[:-1] if i != ''])
      if void_counter > el_counter: row = ''
      
      rows = rows + row
      
    date = json_data['date']
    date_of_creation = self.__get_creation_date()
    # \n(от {date_of_creation})\n\n
    rows = f'Расписание на {date}\n{self.default} \n\n' + rows
    return rows
