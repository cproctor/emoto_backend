from django.conf import settings
import requests
import random

def get_weather(latitude, longitude):
    url = "http://api.wunderground.com/api/{}/conditions/forecast/alert/q/{},{}.json"
    response = requests.get(url.format(settings.WUNDERGROUND_KEY, latitude, longitude))
    if response.ok:
        obs = response.json()['current_observation']
        return {
            'time_zone': obs['local_tz_long'],
            'weather': obs['weather'],
            'temperature': obs['temp_f'],
            'weather_icon_url': obs['icon_url'],
            'city': obs['display_location']['full']
        }
        
def generate_pair_code():
    alphabet = [chr(x) for x in range(65, 91)]
    return ''.join(random.sample(alphabet, 6))
        
