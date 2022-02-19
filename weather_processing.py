"""
Created on Mon Feb  7 14:10:42 2022

@author: Okhrimchuk Roman
for Sierentz Global Merchants

Test task
"""


# TODO Import the necessary libraries
import pandas as pd
import numpy as np
import copy
import datetime
import re

# TODO Import the dataset 

path = r'./data/weather_dataset.data'
df = pd.read_csv(path, delimiter=r"\s+")

# TODO  Assign it to a variable called data and replace the first 3 columns by a proper datetime index
data = copy.deepcopy(df)
data['datetime'] = '19' + data['Yr'].astype(str) + "-" + data['Mo'].astype(str) + "-" + data['Dy'].astype(str)
data['datetime'] = data['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
data.index = data['datetime']
data = data.drop(columns = ['Yr','Mo','Dy','datetime'], axis = 1)

# TODO Check if everything is okay with the data. Create functions to delete/fix rows with strange cases and apply them


# TODO Write a function in order to fix date (this relate only to the year info) and apply it

def fix(col):
    for i in col.index:
        try:
            if (float(col[i]) < 0) or (float(col[i]) > 100):
                col[i] = None
        except ValueError:
            reg = re.compile('[^0-9.]')
            if col[i] not in ['NAN', 'NaN', 'nan', np.nan, '', None, 'None', 'Nodata', 'nodata', 'NONE']:
                c = reg.sub('', col[i])
                if (float(c) < 0) or (float(c) > 100):
                    col[i] = None
            else:
                col[i] = None
    return col

for col in data.columns:
    data[col] = fix(data[col])

# TODO Set the right dates as the index. Pay attention at the data type, it should be datetime64[ns]


# TODO Compute how many values are missing for each location over the entire record

print(data.isnull().sum())

# TODO Compute how many non-missing values there are in total

print(len(data) * len(data.columns) - data.isnull().sum().sum())

# TODO Calculate the mean windspeeds of the windspeeds over all the locations and all the times

for col in data.columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')
print(data.mean().values.mean())

# TODO Create a DataFrame called loc_stats and calculate the min, max and mean windspeeds and standard deviations of the windspeeds at each location over all the days

loc_stats = pd.DataFrame(columns=['Location', 'Max_ws', 'Min_ws', 'Mean_ws', 'Stand_dev_ws'])

for col in data.columns:
    row = {'Location' : col, 'Max_ws' : data[col].max(), 'Min_ws' : data[col].min(), 'Mean_ws' : data[col].mean(), 'Stand_dev_ws' : data[col].std()}
    loc_stats = loc_stats.append(row, ignore_index=True)

# TODO Find the average windspeed in January for each location

data[data.index.month == 1].mean()

# TODO Downsample the record to a yearly frequency for each location

data_year = copy.deepcopy(data)
data_year['year'] = data_year.index.year
data_year = data_year.groupby('year').mean()

# TODO Downsample the record to a monthly frequency for each location

data_month = copy.deepcopy(data)
data_month['year'] = data_month.index.year
data_month['month'] = data_month.index.month
data_month['year_month'] = data_month['year'].astype(str) + "-" + data_month['month'].astype(str)
data_month = data_month.groupby('year_month').mean()

# TODO Downsample the record to a weekly frequency for each location

data_week = copy.deepcopy(data)
data_week['year'] = data_week.index.year
data_week['week'] = data_week.index.week
data_week['year_week'] = data_week['year'].astype(str) + "-" + data_week['week'].astype(str)
data_week = data_week.groupby('year_week').mean()

# TODO Calculate the min, max and mean windspeeds and standard deviations of the windspeeds across all locations for each week (assume that the first week starts on January 2 1961) for the first 21 weeks

loc_stats_week = pd.DataFrame(columns=['Week', 'Max_ws', 'Min_ws', 'Mean_ws', 'Stand_dev_ws'])
cols = ['param1', 'param2', 'param3', 'param4', 'param5', 'param6', 'param7', 'param8', 'param9', 'param10', 'param11', 'param12']

data_21_week = copy.deepcopy(data)
data_21_week['week'] = data_21_week.index.week
data_21_week['year'] = data_21_week.index.year
min_year = data_21_week['year'].min()
data_21_week = data_21_week[data_21_week['year'] == min_year][data_21_week['week'] < 22]
for i in range(21):
    r = [i + 1, data_21_week[data_21_week['week'] == i+1][cols].max().max(), data_21_week[data_21_week['week'] == i+1][cols].min().min(),
        data_21_week[data_21_week['week'] == i+1][cols].mean().mean(), data_21_week[data_21_week['week'] == i+1][cols].std().std()]
    row = {'Week' : i+1, 'Max_ws' : data_21_week[data_21_week['week'] == i+1][cols].max().max(),
           'Min_ws' : data_21_week[data_21_week['week'] == i+1][cols].min().min(),
           'Mean_ws' : data_21_week[data_21_week['week'] == i+1][cols].mean().mean(),
           'Stand_dev_ws' : data_21_week[data_21_week['week'] == i+1][cols].std().std()}
    loc_stats_week = loc_stats_week.append(row, ignore_index=True)
