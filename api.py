import requests
from dotenv import load_dotenv
import os

load_dotenv()


# this function finds the lat, long of a place using autocomplete by Mapbox
# due to multiple place could be found, sample indicates which index of address
def get_coordi(borough, sample = 0):
  MAPBOX_BASE_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
  MAPBOX_KEY = os.getenv("MAPBOX_KEY")
  options = '&autocomplete=true&country=gb'
  url = MAPBOX_BASE_URL+borough+'.json?access_token='+MAPBOX_KEY + options
  # print(url)

  response = requests.get(url)
  if response.status_code == 200:
    # print(borough,'API ok')
    resp = response.json()

  longitude = resp['features'][sample]['center'][0]
  latitude = resp['features'][sample]['center'][1]

  return latitude, longitude


# this function finds the lat, long of a place using defined number of points
def get_multi_coordi(borough, points = 2):
  coordi_list = []
  for point in range(points):
    lat, long = get_coordi(borough, point)
    # check if the coordinates are in greater london
    if long >= -0.5 and long <= 0.5 and lat <= 51.7 and lat >= 51.2:
      coordi_list.append([lat, long])
  return coordi_list


def get_air_quality(lat, long, hours=6):
  AQI_BASE_URL='https://api.breezometer.com/air-quality/v2/historical/hourly?'
  BREEZO_KEY = os.getenv("BREEZO_KEY")
  options = "lat=%s&lon=%s&key=%s&hours=%s" %(lat,long,BREEZO_KEY,hours)
  url = AQI_BASE_URL+options

  # print(url)

  r = requests.get(url)
  call = r.json()

  aqi_list = []

  for data in call['data']:
      if data['data_available']==True:
          aqi_list.append(data['indexes']['baqi']['aqi'])

  return aqi_list


# helper function to flatter list in a list
def flatten_list(l):
  flat_list = [item for sublist in l for item in sublist]
  return flat_list


# get the air quality data of a place, returns a list
def get_place_aqi(df, area, hours=6):
  coordi_list = df[df['area']==area].coordi.values[0]
  # print(coordi_list)

  aqi_list = []

  for coordi in coordi_list:
    aqi_list.append(get_air_quality(coordi[0],coordi[1],hours))

  final_list = flatten_list(aqi_list)

  return final_list





