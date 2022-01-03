import time
import yandex_weather_api as yandex



seasons = {
    'winter':[],  # зима (с 1 декабря)
    'spring_fh':[],  # начало весны, примерно до 25 апреля
    'spring_sh':[],  # вторая половина весны
    'summer':[],  # лето
    'autumn_fh':[],  # начало осени(по середину или конец октября)
    'autumn_sh':[],  # вторая часть осени
}



# yandex.types.Condition

weather_keys = [
            'temp',
            'feels_like',
            'condition',
            'wind_speed',
            'wind_dir',
            'prec_type',
            'prec_strength',
            'phenom_condition',
        ]


conf_keys = [
        'TIME',
        'LAT',
        'LON',
        'INTERVAL',
    ]

default_data = {
                'CONF':{
                    'TIME':int(time.time()),
                    'LAT':63.44,
                    'LON':34.18,
                    'INTERVAL':3600,
                },
                'DATA':{
                    'temp':0.0,
                    'feels_like':0.0,
                    'condition':'clear',
                    'wind_speed':0.0,
                    'wind_dir':'c',
                    'prec_type':0,
                    'prec_strength':0,
                    'phenom_condition':'fog',
                 },
            }



condition_to_num = {
                    'clear':1,  # ясно
                    'partly-cloudy':2,  # малооблачно
                    'cloudy':3,  # облачно с прояснениями
                    'overcast':4,  # пасмурно
                    'drizzle':5,  # морось
                    'light-rain':6,  # небольшой дождь
                    'rain':7,  # дождь
                    'moderate-rain':8,  # умеренно сильный дождь
                    'heavy-rain':9,  # сильный дождь
                    'continuous-heavy-rain':10,  # длительный сильный дождь
                    'showers':11,  # ливень
                    'wet-snow':12,  # дождь со снегом
                    'light-snow':13,  # небольшой снег
                    'snow':14,  # снег
                    'snow-showers':15,  # снегопад
                    'hail':16,  # град
                    'thunderstorm':17,  # гроза
                    'thunderstorm-with-rain':18,  # дождь с грозой
                    'thunderstorm-with-hail':19,  # гроза с градом
                }

conditioncls_to_string = {}



condition_from_num = {
                    
                }

winddir_to_num = {
                
            }

winddir_from_num = {
                    
                }

phenom_to_num = {
                
            }

phenom_from_num = {
                
            }

data = default_data['DATA'].copy()
conf = {
        'TIME':int(time.time()),
        'LAT':63.44,
        'LON':34.18,
        'INTERVAL':3600,
        }

confdata = default_data.copy()

def update_data(datain:dict):
    global data
    for key in datain:
        if key in weather_keys:
            data[key] = datain[key]
    confdata['DATA'] = data
    return data
    
    

def update_conf(confin:dict):
    global conf
    for key in confin:
        if key in conf_keys:
            conf[key] = confin[key]
    confdata['CONF'] = conf
    return conf
    


def format_data(datain):
    data = dict()
    for key in datain:
        if key in weather_keys or key in conf_keys:
            if key == 'condition' and isinstance(datain[key], yandex.types.Condition):
                data[key] = str(datain[key])
                continue
            if key == 'wind_dir' and isinstance(datain[key], yandex.types.WindDir):
                data[key] = str(datain[key])
                continue
            data[key] = datain[key]
    return data







