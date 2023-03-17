
import io
import csv
import asyncio
from aiohttp import ClientSession
import requests
import time
import array
from dataclasses import dataclass



def __get_table__():

  async def tasks():
    urls = ('https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet&gid=1202329550',
            'https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet&gid=0')
    return await asyncio.gather(*[asyncio.create_task(__fetch__(url = url)) for url in urls])

  async def __fetch__(url):
    async with ClientSession() as session:
      async with session.get(url) as response:
        file = io.StringIO(await response.text())
        csv_data = csv.reader(file, delimiter=",")
        result = [row for row in csv_data]
        return result
  
  async def handler():
    return [table for table in await tasks()]
      
  return asyncio.run(handler())

def __get_table_2__():

  async def __fetch__():
    async with ClientSession() as session:
      async with session.get('https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet&gid=0') as response:
        file = io.StringIO(await response.text())
        csv_data = csv.reader(file, delimiter=",")
        result = [row for row in csv_data]
        return result

  return asyncio.run(__fetch__())

def __get_table_3__():
  r = requests
  response = r.get('https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet&gid=0')
  file = io.StringIO(response.text)
  csv_data = csv.reader(file, delimiter=",")
  result = [row for row in csv_data]
  return result


import asyncio
import json

