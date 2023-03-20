import json,os,time
from TimetableStudents import get_dictionary_for_students
from TimetableTeachers import get_dictionary_for_teachers


def update_json_file() -> None:
  dictionary = get_dictionary_for_students() | get_dictionary_for_teachers()
  with open("timetable.json",'w',encoding='UTF-8') as js:
    json.dump(obj=dictionary,
              fp = js,
              ensure_ascii=False,
              indent=4)


class TimeTable():
  
  def __init__(self,default:str,config_string : str = '(number)[time]|cabinet| lesson - default\n') -> None:
    self.config_string = config_string
    self.default = default

  def __get_clean_row(self)->str:
    string = self.config_string
    for value in ('default','lesson','cabinet' ,'time','number'):
      if value in self.config_string:
        string = string.replace(value,"{"+str(value)+"}")
    return string
    
  def __get_reverse_values(self)->list:
    values = []
    for value in ('default','lesson','cabinet' ,'time','number'):
      if value not in self.config_string:
        values.append(value)
        
    return values

  @staticmethod
  def __read_json_data() -> None:
      with open("timetable.json",'r',encoding='UTF-8') as js:
        json_data = json.loads(js.read())
        return json_data
  
  @staticmethod
  def __get_creation_date() -> str:
    created_time = os.path.getctime('timetable.json')
    created_time_str = time.strftime('%d.%m.%Y в %H:%M:%S', time.localtime(created_time))
    return created_time_str

  def get_text(self) -> str:
    
    json_data : dict = self.__read_json_data()[self.default]
    if json_data is None: return 'Расписание отсутствует,\nприятного отдыха!'
    
    
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
    rows = f'Расписание на {date} для {self.default} \n(от {date_of_creation})\n\n' + rows
    return rows






