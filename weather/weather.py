import requests
from bs4 import BeautifulSoup
import yandex_weather_api as yandex
from rich import print
from rich import console
from pprint import pprint
import os.path
import time
import json


import weatherdata

console = console.Console()


data_file = './config.json'
GETDATA = False
tmp = {}
LAT = 63.00
LON = 34.00
old_time = 0
now_time = int(time.time())
interval = 3600

def update_time():
    ...


def load_weatherdata(filename):
    data = None
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def check_time(old_t, new_t, interval):
    return (new_t - old_t) >= interval


def is_config(filename):
    if not os.path.isfile(filename) and not os.path.isdir(filename):
        if not filename.endswith('.json'):
            raise Exception('Не верное расширение файла.')
        return False
    return True


def save_data(filename, data:dict=None):
    _data = data
    if data is None:
        print('Файл не существует и будет создан с дефолтными значениями.')
        _data = weatherdata.default_data.copy()
    with open(filename, 'w') as f:
        print('Запись в файл.')
        json.dump(_data, f)
    


def get_data(api_key, lat, lon):
    resp = yandex.get(requests, api_key=api_key, rate='forecast', lat=lat, lon=lon)
    data = weatherdata.format_data(dict(resp['fact']))
    return data


if __name__ == '__main__':
    
    if not is_config(data_file):
        save_data(data_file)
        LAT = weatherdata.default_data['CONF']['LAT']
        LON = weatherdata.default_data['CONF']['LON']
        interval = weatherdata.default_data['CONF']['INTERVAL']
        GETDATA = True
    else:
        tmp = load_weatherdata(data_file)
        print('Load data:', tmp)
        old_time = tmp['CONF']['TIME']
        interval = tmp['CONF']['INTERVAL']
        LAT = weatherdata.default_data['CONF']['LAT']
        LON = weatherdata.default_data['CONF']['LON']
        if check_time(old_time, now_time, interval):
            GETDATA = True
    
    
    if GETDATA:
        tmp = get_data('962fe530-4a9f-4c35-a514-21cda42aea0e', LAT, LON)
        tmp = weatherdata.update_data(tmp)
        conf = {'TIME':now_time, 'LAT':LAT, 'LON':LON, 'INTERVAL':interval}
        conf = weatherdata.update_conf(conf)
        save_data(data_file, weatherdata.confdata)
        print('Getting data:', weatherdata.confdata)
















