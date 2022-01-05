from ogl import mainwindow
from weather import weather, secret
from ogl.mainwindow import Models

from rich import console

cons = console.Console()

# ==================================

mainwindow.set_window_size()

# ==================================

season = weather.get_season()
weather_data = weather.Weather(secret.token).data['DATA']
cons.print(weather_data)


models = Models()

if season == 0:
    models.landscape = 'landscape_winter.glb'
    models.house = 'wooden_house_wint.glb'


# ==================================

if __name__ == '__main__':
    
    world = mainwindow.World(models)
    world.run()


