import requests
import csv
import io


  

def get_table() -> list[list,list]: 
  __URL__ ='https://docs.google.com/spreadsheets/d/1rGJ4_4BbSm0qweN7Iusz8d55e6uNr6bFRCv_j3W5fGU/gviz/tq?tqx=out:csv&sheet'
  request = requests.get(__URL__).content
  file = io.StringIO(request.decode())
  csv_data = csv.reader(file, delimiter=",")
  return[row for row in csv_data]


  





