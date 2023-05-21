from schedule._students import get_dictionary_for_students
from schedule._teachers import get_dictionary_for_teachers
from schedule.tjson import read_json




def get_dict() -> dict:
  return get_dictionary_for_students() | get_dictionary_for_teachers()

class Timetable():
  def __init__(self,_object : str | dict, _key:str, _config : str) -> None:
    self._object = _object
    self._config = self.__get_formating_string(_config)
    self._key = _key
  
  @staticmethod
  def __get_formating_string(config : str) -> str:
    for v in ('default','lesson','cabinet' ,'time','number','distance'):
      config = config.replace(v,'{%s}'%v)
    config = config.replace('/n','\n')
    return config
  
  @staticmethod
  def __read(_object : str | dict) -> dict:
    if isinstance(_object ,str):
      return read_json(_object)
    elif isinstance(_object, dict):
      return _object
    else: 
      raise TypeError('Объект не является словарем или строкой')
    
  

  def get_text(self) -> str:
 
    try:
      table = self.__read(self._object)[self._key]
    except KeyError: 
      return f'Ошибка чтения! Расписание для {self._key} отсутствует в таблице'
    if not table: 
      return f'Расписание отсутствует, приятного отдыха!'

    rows = ''
    for value in zip(*table.values()):
      _keys = table.keys()
      _format = {k : v for k, v in zip(_keys,value)}
      
      """Пропуск строки , если нет данных"""
      if [True for i in ('default','lesson','cabinet') if not _format[i]]:
        continue
      
      row = self._config.format(**_format)
      rows += row
    
    date = table['date']
    return f'Расписание на {date}\n{self._key} \n\n{rows}'
