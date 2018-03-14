
# coding: utf-8

# In[79]:

import os
print os.getcwd()
import inspect
import logging
from datetime import datetime
#Creating a logfile
logging.basicConfig(filename='Weather_Data.log',level=logging.DEBUG)

import pdb


# In[37]:

import json
import pandas as pd
from pprint import pprint
pd.set_option('display.float_format', lambda x: '%.3f' % x)


file_name = 'city_list.json'
data = json.load(open('city_list.json'))
#pprint (data)
id1 = str(data[0]['id'])
country = data[1]['country']

f = open('countrycodes.txt','w+')
f.write(id1)
f.write(",")
f.write(country)
f.close()


# In[ ]:

get_ipython().magic(u'debug')


# In[38]:

print data[0]


# #### Population is present in current_city_list_min.json

# In[39]:


city_data = json.load(open('current_city_list_min.json'))
pprint (city_data[0])
print ("Printing population and city ID")
print (city_data[0]['stat']['population'])
print (city_data[0]['id'])


# In[40]:

f = open('countrycodes.txt','w+')
header_line_country="Country"
header_line_id="City_ID"
header_line_population="Population"
f.write(header_line_country+","+header_line_id+","+header_line_population+"\n" )
for val in city_data:
    write_line = (val['country']+ "," +str(val['id'])+","+str(val['stat']['population'])+'\n')
    #print write_line
    f.write(write_line)  
f.close()    
   


# In[41]:

#importing data frame
import pandas as pd
df = pd.read_csv("countrycodes.txt", sep=",")
df.head()
print df.shape
df.describe()


# In[42]:

top_50_df =df.sort_values(by=['Population'], ascending=False).head(50)


# In[43]:

top_50_df


# In[44]:

#writing top 50 cities to a doc


# In[77]:

header_line_country="Country_OW"
header_line_id="City_ID_OW"
header_line_city_name="City_Name_OW"
header_line_date_time = "Local_date_time_OW"
header_line_temp = "Temparature_OW"
header_line_pressure = "Pressure_OW"
header_line_humidity = "Humidity_percent_OW"
header_line_clouds = "Clouds_all_OW"
header_line_wind = "Wind_Speed_OW"
header_line_rain = "Rain_3h_OW"
header_line_snow = "Snow_3h_OW"
header_line_weather_description = "Weather_Description_OW"
f = open('OpenWeather_data.txt','w+')

f.write(header_line_country+","
        +header_line_id+","
        +header_line_city_name+","
        +header_line_date_time+","
        +header_line_temp+","
        +header_line_pressure+","
        +header_line_humidity+","
        +header_line_clouds+","
        +header_line_wind+","
        +header_line_rain+","
        +header_line_snow+","
        +header_line_weather_description+'\n')

    
f.close()


# In[78]:

import requests
#api_url = "api.openweathermap.org/data/2.5/forecast/daily?id=1796236&appid=fee946e78e969fefcc503b47b1108419"
list_of_cities = top_50_df['City_ID'].tolist()
list_of_cities = [int(city) for city in list_of_cities]
print list_of_cities
for city_id in list_of_cities:
    logging.info("Fetching data for City_id"+str(city_id))
    api_url= "http://api.openweathermap.org/data/2.5/forecast?id="+str(city_id)+"&APPID=fee946e78e969fefcc503b47b1108419"
    logging.info(api_url)
    response = requests.get(api_url)
    logging.info(response.status_code)
    #print response.text
    data1 = response.json()
    #print list_of_cities
    f = open('OpenWeather_data.txt','a+')
    count = data1['cnt']
    logging.info(str(datetime.now())+"The number of rows to be fetched is "+str(count)+" for "+str(city_id))
    for val in range(0,count,1):
        city_country_ow = data1['city']['country']
        city_id_ow = str(data1['city']['id'])
        city_name_ow = data1['city']['name']    
        datetime_ow = str(data1['list'][val]['dt_txt'])
        temp_ow = str(data1['list'][val]['main']['temp'])
        pressure_ow = str(data1['list'][val]['main']['pressure'])
        humidity_percent_ow = str(data1['list'][val]['main']['humidity'])
        clouds_all_ow = str(data1['list'][val]['clouds']['all'])
        wind_speed_ow = str(data1['list'][val]['wind']['speed'])

        try:
            rain_3h_ow = str(data1['list'][val]['rain']['3h'])
        except KeyError:
            logging.debug(str(datetime.now())+"Key Error Encountered setting rain to Zero for "+str(datetime_ow))
            rain_3h_ow = str(0.0)
        try:
            snow_3h_ow = str(data1['list'][val]['snow']['3h'])
        except KeyError:    
            logging.debug(str(datetime.now())+"Key Error Encountered setting snow to Zero for "+str(datetime_ow))
            snow_3h_ow = str(0.0)
        weather_description_ow = str(data1['list'][val]['weather'][0]['description'])    
        f.write(city_country_ow+","
           +city_id_ow+","
           +city_name_ow+","
           +datetime_ow+","
           +temp_ow+","
           +pressure_ow+","
           +humidity_percent_ow+","
           +clouds_all_ow+","
           +wind_speed_ow+","
           +rain_3h_ow+","
           +snow_3h_ow+","
           +weather_description_ow+"\n")
    
    
f.close()


# #### Do not execute below cell

# In[46]:

#data1['list']


city_id_ow = data1['city']['id']
city_name_ow = data1['city']['name']
city_country_ow = data1['city']['country']
datetime_ow = data1['list'][0]['dt_txt']
temp_ow = data1['list'][0]['main']['temp']
pressure_ow = data1['list'][0]['main']['pressure']
humidity_percent_ow = data1['list'][0]['main']['humidity']
clouds_all_ow = data1['list'][0]['clouds']['all']
wind_speed_ow = data1['list'][0]['wind']['speed']

try:
    rain_3h_ow = data1['list'][0]['rain']['3h']
except KeyError:
    logging.debug("Key Error Encountered setting rain to Zero for "+str(datetime_ow))
    rain_3h_ow = 0.0
try:
    _3h_ow = data1['list'][0]['snow']['3h']
except KeyError:    
    logging.debug("Key Error Encountered setting snow to Zero for "+str(datetime_ow))
    snow_3h_ow = 0.0
weather_description_ow = data1['list'][0]['weather'][0]['description']





# ##### Writing the OpenWeather data to a file 

# In[55]:




# In[48]:

print type(snow_3h_ow)


# In[59]:

f = open('OpenWeather_data.txt','a+')
count = data1['cnt']
logging.info(str(datetime.now())+"The number of rows to be fetched is "+str(count)+" at "+str(datetime_ow))
for val in range(0,count,1):
    city_country_ow = data1['city']['country']
    city_id_ow = str(data1['city']['id'])
    city_name_ow = data1['city']['name']    
    datetime_ow = str(data1['list'][val]['dt_txt'])
    temp_ow = str(data1['list'][val]['main']['temp'])
    pressure_ow = str(data1['list'][val]['main']['pressure'])
    humidity_percent_ow = str(data1['list'][val]['main']['humidity'])
    clouds_all_ow = str(data1['list'][val]['clouds']['all'])
    wind_speed_ow = str(data1['list'][val]['wind']['speed'])

    try:
        rain_3h_ow = str(data1['list'][val]['rain']['3h'])
    except KeyError:
        logging.debug(str(datetime.now())+"Key Error Encountered setting rain to Zero for "+str(datetime_ow))
        rain_3h_ow = str(0.0)
    try:
        snow_3h_ow = str(data1['list'][val]['snow']['3h'])
    except KeyError:    
        logging.debug(str(datetime.now())+"Key Error Encountered setting snow to Zero for "+str(datetime_ow))
        snow_3h_ow = str(0.0)
    weather_description_ow = str(data1['list'][val]['weather'][0]['description'])    
    f.write(city_country_ow+","
           +city_id_ow+","
           +city_name_ow+","
           +datetime_ow+","
           +temp_ow+","
           +pressure_ow+","
           +humidity_percent_ow+","
           +clouds_all_ow+","
           +wind_speed_ow+","
           +rain_3h_ow+","
           +snow_3h_ow+","
           +weather_description_ow+"\n")
    
    
f.close()


# In[50]:

str(datetime.now())


# In[51]:




# In[52]:

data1['list'][val]['wind']['speed']


# In[53]:

data1['cnt']


# In[54]:

print data1['list'][0]['dt_txt']


# ##### The parameters pulled are the following 
# ###### OpenWeather parameter = weatherbit equivalent
# * city.id = city_id 
# * city.name = city_name
# * city.country = country_code
# * list.dt_txt =datetime [This is local date time]
# * list.main.temp (K) = temp(degrees C) 
# * list.main.pressure(hpa) = pres(mb)
# * list.main.humidity(%) = rh(%)
# * list.weather.description = description
# * list.clouds.all(%) = clouds(%)
# * list.wind.speed(m/s) = wind_spd(m/s)
# * list.rain.3h (mm) = precip (mm) [_This is set to zero when the field is not available_]
# * list.snow.3h(mm) = snow (mm) [_This is set to zero when the field is not available_]
# 
# ##### The data pulled from OpenWeather is at 3 hr level and data from weatherbit is 1 hr level. So reasonable assumptions are made to convert 1 hr level data into 3 hour level data. The assumptions are as follows

# 

# In[51]:

f.close()


# In[ ]:



