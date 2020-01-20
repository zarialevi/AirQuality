"""
This module is for your data cleaning.
It should be repeatable.

## PRECLEANING
There should be a separate script recording how you transformed
the json api calls into a dataframe and csv.

## SUPPORT FUNCTIONS
There can be an unlimited amount of support functions.
Each support function should have an informative name and return the
partially cleaned bit of the dataset.
"""
import pandas as pd

import requests
from dotenv import load_dotenv
import os
import api

load_dotenv()

def borough_auto_rename(dataset):
  ORIGINAL_COLS = dataset.columns

  # rename the columns, and rearrange so similar data is together
  dataset.rename(columns=lambda x:x.split()[0].lower()
                  if x.split()[0] not in ['Number','Average']
                  else x.split()[2].lower(),
                inplace=True)
  return dataset

def borough_rename(dataset):
  dataset.rename(columns={
                'new':'code',
                'inner/':'inner_outer',
                'active':'active_business',
                'median':'house_price',
                'd':'council_tax',
                'rented':'council_rental',
                '%':'greenspace',
                'total':'carbon_emmision',
                'cars,':'cars',
                'transport':'pub_transport'
                }, inplace=True)

  return dataset

# def support_function_three(example):
#     pass

def get_coordi(borough):
  MAPBOX_BASE_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
  MAPBOX_KEY = os.getenv("MAPBOX_KEY")
  options = '&autocomplete=true&country=gb'
  url = MAPBOX_BASE_URL+borough+'.json?access_token='+MAPBOX_KEY + options

  response = requests.get(url)
  if response.status_code == 200:
    resp = response.json()

  longitude = resp['features'][0]['center'][0]
  latitude = resp['features'][0]['center'][1]

  return latitude, longitude



def full_clean():
  """
  This is the one function called that will run all the support functions.
  Assumption: Your data will be saved in a data folder and named "dirty_data.csv"
  :return: cleaned dataset to be passed to hypothesis testing and visualization modules.

  # we only need 19 columns, skip an empty row & inner london as it has
  lots of missing value, also skip the summary rows at the end
  """
  cols_to_use = [1,2,3,7,32,47,49,52,53,57,59,60,62,65,66,73,75,76,80]
  dirty_borough_data = pd.read_csv('./data/london-borough-profiles-2016.csv',
                            usecols = cols_to_use,
                            skiprows = [1],
                            # skiprows = [1,2],
                            nrows=33)
  borough_renamed1 = borough_auto_rename(dirty_borough_data)
  borough_data = borough_rename(borough_renamed1)
  borough_data.to_csv('./data/borough_data_cleaned.csv')

  borough_data['coordi'] = borough_data.area.map(lambda x: api.get_multi_coordi(x,1))
  # manually found out the coordinates of sutton, input it in
  # sutton = [[51.366136, -0.176360]]
  borough_data.at[28,'coordi'] = [[51.366136, -0.176360]]
  borough_data.to_csv('./data/borough_data_cleaned_coordi.csv', index=True)

  return borough_data


def aqi_data(borough_data, hours=24):
  borough_data['aqi_24'] = borough_data.area.map(lambda x: api.get_place_aqi(borough_data,x,hours))
  borough_data.to_csv('./data/borough_data_cleaned_aqi.csv', index=True)

  return borough_data



