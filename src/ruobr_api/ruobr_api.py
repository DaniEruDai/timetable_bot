from ._schedule import Schedule
from ._marks import Marks
from ._excel import Excel
from .exceptions import RuobrException

from dataclasses import dataclass

import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://cabinet.ruobr.ru/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

def get_tomorrow() -> str:
  return datetime.strftime(datetime.today() + relativedelta(days=1),'%d.%m.%Y')

def check_format(__date : str) -> bool:
  match len(__date):
    case 4:
      return __date.isdigit()
    case 7:
      tmp_list = __date.split(".")
      length_check = len(tmp_list[0]) == 2 and len(tmp_list[1]) == 4
      digit_check = tmp_list[0].isdigit() and tmp_list[1].isdigit()
      month_check = 0 < int(tmp_list[0]) <= 12
      return length_check and digit_check and month_check
    
    case 10:
      tmp_list = __date.split(".")
      length_check = len(tmp_list[0])== 2 and len(tmp_list[1]) == 2 and len(tmp_list[2]) == 4
      digit_check = tmp_list[0].isdigit() and tmp_list[1].isdigit() and tmp_list[2].isdigit()
      month_check = 0 < int(tmp_list[1]) <= 12
      return length_check and digit_check and month_check
    
    case _:
      return False

def key_to_date(__key : str) -> str:
    match __key:
      case 'day':
        return datetime.now().strftime('%d.%m.%Y')
      case 'month':
        return datetime.now().strftime('%m.%Y')
      case 'year':
        return (datetime.now() - relativedelta(years=1)).strftime('%Y')

class MarkObject:
  def __init__(self, __date : str , __lesson : str, __mark : str):
    self._date = datetime.strptime(__date,'%d.%m.%Y')
    self._lesson = __lesson
    self._mark = self.__to_nums(__mark)

  def init(cls):
    return cls.mrk(date=cls._date, lesson=cls._lesson, mark=cls._mark)

  @staticmethod
  def __to_nums(mark : str) -> int :
    return {'отлично': 5,'хорошо': 4,'удовлетворительно': 3,'неудовлетворительно': 2}[mark]

  @dataclass
  class mrk:
    date : datetime
    lesson : str
    mark : int
 
class Ruobr:

    def __init__(self, username, password):
        self.__username, self.__password = username, password
        self.__cookie = self.__cookies()

    def __cookies(self) -> dict:
        session = requests.Session()
        session.get('https://cabinet.ruobr.ru/login/', headers=headers)
        data = {'username': f'{self.__username}', 'password': f'{self.__password}',
                'csrfmiddlewaretoken': dict(session.cookies)['csrftoken']}
        session.post('https://cabinet.ruobr.ru/login/', headers=headers, data=data)
      
        result = dict(session.cookies)
        if len(result) != 2:
          raise RuobrException.AuthException('Логин или пароль указаны неверно!')
        
        return result

    def __get_esimation(self) -> list:

        async def __taskmaster():
            pagination = await __pagination()
            tasks = []
            urls = (f'https://cabinet.ruobr.ru//student/progress/?page={num}' for num in range(1, pagination))

            async with ClientSession() as session:
                for url in urls:
                    tasks.append(asyncio.create_task(__fetch(url, session)))
                    await asyncio.sleep(0.02)

                return await asyncio.gather(*tasks)

        async def __fetch(url, session):
            async with session.get(url, cookies=self.__cookie) as response:
                return await response.text()

        async def __pagination():
            async with ClientSession() as session:
                async with session.get('https://cabinet.ruobr.ru//student/progress/?page=1',
                                       cookies=self.__cookie) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    pagination = int([link.get('href') for link in soup.find_all('a')][-2].split('=')[1]) + 1
                    return pagination

        async def __handler():
            all_marks = []
            for request in await __taskmaster():
              soup = BeautifulSoup(request, 'html.parser')
              data = list(map(str, soup.find_all('tr')))
              for t in data:
                cleantext = BeautifulSoup(t, 'html.parser').text.split('\n')[3:6]
                if cleantext != ['Дата', 'Дисциплина', 'Отметка']:
                  all_marks.append(MarkObject(cleantext[0],cleantext[1],cleantext[2]).init())
                
            return all_marks

        return asyncio.run(__handler())
    
    def __get_schedule_response(self,__date) -> list: 
      date = datetime.strptime(__date, "%d.%m.%Y")
      start = date.strftime('%Y-%m-%d')
      end = start
    
      params = {'start': start,
                'end': end}
      
      session = requests.Session()
      response = session.get('https://cabinet.ruobr.ru/student/get_schedule/g0/',cookies=self.__cookie, headers=headers, params=params )
      response = response.json()
      if response:
        return response
      else :
        raise RuobrException.EmptyScheduleException(f'Расписания на {__date} не найдено!')

    def get_marks(self, __date:str) -> Marks:
      if __date in ('day', 'month', 'year'):
        __date = key_to_date(__date)
      
      if check_format(__date):
        ALL_MARKS = self.__get_esimation()
        return Marks(list_of_marks = ALL_MARKS, date = __date)
      else:
        raise RuobrException.DateException('Неверный формат даты')
   
    def get_schedule(self, __date : str) -> Schedule:
      if check_format(__date):
       return Schedule(self.__get_schedule_response(__date))
      else:
        raise RuobrException.DateException('Неверный формат даты')

    def get_excel(self,__year : str) -> Excel:
      def check_format_year(__date : str) -> bool:
        match len(__date):
          case 4:
            return __date.isdigit()
          case _:
            return False
      
      if __year == 'now':
        __year = (datetime.now() - relativedelta(years=1)).strftime('%Y')
      
      if not check_format_year(__year):
        raise RuobrException.DateException('Неверный формат даты')
      list_of_marks = self.__get_esimation()
      return Excel(list_of_marks,__year)
    


