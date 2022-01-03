import time
import yandex_weather_api as yandex


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



import numpy as np

x = np.linspace(-1.0, 1.0, 50)
y = np.random.rand(50) - 0.5
r = np.ones(50)
g = np.zeros(50)
b = np.zeros(50)



vertices = np.dstack([x, y, r, g, b])
print(vertices)

vert = np.array([
        -0.3, 0.5,
        0.3, 0.5,
        0.5, 0.3,
        0.5, -0.3,
        0.3, -0.5,
        -0.3, -0.5,
        -0.5, -0.3,
        -0.5, 0.3
    ])

vert = vert.reshape((8,2))
print(vert)

col = np.array([
        [255.,255.,0.0],
        [255.,255.,0.0],
        [255.,255.,0.0],
        [255.,255.,0.0],
        [255.,255.,0.0],
        [255.,255.,0.0],
        [255.,255.,0.0],
        [255.,255.,0.0],
    ])
print()
print(np.concatenate((vert, col), axis=1))






