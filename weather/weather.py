import requests
from bs4 import BeautifulSoup
import yandex_weather_api as yandex
from rich import print
from rich import console
from pprint import pprint
import os.path
import time
import json
import rich
import time
from pathlib import Path

try:
    import weatherdata
    import secret
except:
    from . import weatherdata
    from . import secret

console = console.Console()

data_file = Path(__file__).resolve().parent.joinpath('config.json')
GETDATA = False
tmp = {}
LAT = 63.00
LON = 34.00
old_time = 0
now_time = int(time.time())
interval = 3600

DATA = None

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
    resp = yandex.get(requests, api_key=api_key, rate='informers', lat=lat, lon=lon)
    rich.print(resp)
    data = weatherdata.format_data(dict(resp['fact']))
    return data


def get_angle_sun_at_noon(latitude):
    winter = 66 - latitude
    equinox = 90 - latitude
    summer = 180 - 66 - latitude
    return winter, equinox, summer


def get_sun_path_lenght(lenght_day):
    '''
    расчитывается длина солнечного пути
    
    lenght_day - int, продолжительность дня в минутах 
    '''
    ...
    

def get_sun_position(sunrise, sunset, current_time=None):
    '''
    
    производится расчет положения солнца в определенный момент времени
    
    sunrise - time.struct_time
    sunset - time.struct_time
    current_time = time.struct_time
    '''
    curtime = current_time if current_time is not None else time.gmtime(time.time())
    hour = curtime.tm_hour
    minutes = curtime.tm_min


def get_season(current_date=None):
    '''
    current_date - time.struct_time или str или tuple
    строка должна иметь такой формат DD.MM (01.07 - первое июля)
    кортеж сотоит из двух элементов int - (число, месяц)
    
    '''
    month = None
    day = None
    
    if current_date is not None:
        if isinstance(current_date, time.struct_time):
            day = current_date.tm_mday
            month = current_date.tm_mon
        elif isinstance(current_date, str):
            day, month = list(map(int, current_date.split('.')))
        elif isinstance(current_date, tuple) or isinstance(current_date, list):
            day, month = list(map(int, current_date))
        else:
            raise TypeError('Не верный тип. Требуется time.struct_time, tuple, list, str')
    else:
        current_date = time.gmtime(time.time())
        day = current_date.tm_mday
        month = current_date.tm_mon
    
    if month == 12 or month == 1 or month == 2:
        # зима
        return 0
    elif month == 3 or (month == 4 and day <= 23):
        # первая часть весны, со снегом
        return 1
    elif (month == 4 and day > 23) or month == 5:
        # вторая часть весны, без снега, молодая листва
        return 2
    elif month > 5 and month < 9:
        # лето
        return 3
    elif month == 9 or (month == 10 and day < 16):
        # золотая осень
        return 4
    elif (month == 10 and day >= 16) or month == 11:
        # осень
        return 5
    raise Exception('Передана неверная дата.')






class Weather:
    
    # путь к файлу в котором хранятся настройки и данные погоды
    data_file = Path(__file__).resolve().parent.joinpath('config.json')
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.DATASTATE = False # переменная определяет нужно ли получать новые данные погоды
        self.__create_conf()  # создание config.json если он не существует
        self.data = self.load_weatherdata()
        self.old_time = self.data['CONF']['TIME']
        self.interval = self.data['CONF']['INTERVAL']
        self.lat = self.data['CONF']['LAT']
        self.lon = self.data['CONF']['LON']
        
        if self.__check_time():
            self.DATASTATE = True
        
        if self.DATASTATE:
            print('Получение новых погодных данных')
            tmp_data = self.get_data()
            weatherdata.update_data(tmp_data)
            
            conf = {'TIME':time.time(), 
                    'LAT':self.lat, 
                    'LON':self.lon, 
                    'INTERVAL':self.interval}
            weatherdata.update_conf(conf)
            save_data(data_file, weatherdata.confdata)
            self.data = self.load_weatherdata()
    
    
    
    def __create_conf(self):
        '''
        проверка существования файла
        если не существует, то создается с дефолтными значениями
        '''
        if not os.path.isfile(Weather.data_file):
            _data = weatherdata.default_data.copy()
            with open(filename, 'w') as f:
                json.dump(_data, f)
                print('Создание файла config.json')
            seld.DATASTATE = True
    
    def load_weatherdata(self):
        data = None
        with open(self.data_file, 'r') as f:
            data = json.load(f)
        return data
    
    def __check_time(self):
        return (time.time() - self.old_time) >= self.interval
    
    def get_data(self):
        resp = yandex.get(
                    requests, 
                    api_key=self.api_key, 
                    rate='informers', 
                    lat=self.lat, 
                    lon=self.lon
                )
        rich.print(resp)
        data = weatherdata.format_data(dict(resp['fact']))
        return data



if __name__ == '__main__':
    
    get_season()
    
    w = Weather(secret.token)
    rich.print(w.data)
    
    # if not is_config(data_file):
        # save_data(data_file)
        # LAT = weatherdata.default_data['CONF']['LAT']
        # LON = weatherdata.default_data['CONF']['LON']
        # interval = weatherdata.default_data['CONF']['INTERVAL']
        # GETDATA = True
    # else:
        # tmp = load_weatherdata(data_file)
        # print('Load data:', tmp)
        # old_time = tmp['CONF']['TIME']
        # interval = tmp['CONF']['INTERVAL']
        # LAT = weatherdata.default_data['CONF']['LAT']
        # LON = weatherdata.default_data['CONF']['LON']
        # if check_time(old_time, now_time, interval):
            # GETDATA = True
    
    
    # if GETDATA:
        # tmp = get_data(secret.token, str(LAT), str(LON))
        # tmp = weatherdata.update_data(tmp)
        # conf = {'TIME':now_time, 'LAT':LAT, 'LON':LON, 'INTERVAL':interval}
        # conf = weatherdata.update_conf(conf)
        # save_data(data_file, weatherdata.confdata)
        # print('Getting data:', weatherdata.confdata)
















