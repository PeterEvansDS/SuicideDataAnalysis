#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:21:20 2021

@author: peterevans
"""

#SUICIDE DATA ANALYSIS

#%% IMPORT DATA
import pandas as pd
import numpy as np
who_data = pd.read_csv(r'/Users/peterevans/UniCloud/Scripting/Assignment1/who_suicide_statistics_modifed3.csv')

#%% 1a) list individual countries


#display unique values of country
countries_list = who_data.country.unique()
print(countries_list)

#%% 1b) show any problem with missing data, bad formatting etc


#check to see how many nan values in each column
num_nan = who_data.isna().sum()
print("NULL VALUES:\n\n", num_nan)

#check sex column
sex_values = pd.unique(who_data.sex)
print("\nSEX VALUES:\n", sex_values)
print("TYPE:", who_data.sex.dtypes)

#check year column
year_values = who_data.year.unique()
print("\nYEAR VALUES:\n", year_values)
print("TYPE:", who_data.year.dtypes)

#check age column
age_values = who_data.age.unique()
print("\nAGE VALUES:\n", age_values)
print("TYPE:", who_data.age.dtypes)

#check suicide values column
print("\nSUICIDE NUMBER TYPE:", who_data.suicides_no.dtypes)
suicide_int = pd.to_numeric(who_data.suicides_no, errors='coerce')
null_suicide = suicide_int.isnull()
print("NUMBER OF NULL VALUES:", null_suicide.sum())
print("NUMBER OF NEGATIVE VALUES:", suicide_int[suicide_int < 0].count())

#check population column
print("\nPOPULATION TYPE:", who_data.population.dtypes)
print("NUMBER OF NEGATIVE VALUES:", who_data.population[who_data.population < 0].count())

#check HDI for year
print('\nHDI FOR YEAR TYPE:', who_data["HDI for year"].dtypes)
null_hdi = who_data['HDI for year'].isnull()
hdi_without_null = who_data['HDI for year'].loc[~null_hdi]
print("NUMBER OF NON-NULL VALUES OUTSIDE RANGE 0.0-1.0:", 
      hdi_without_null[(0.0 > hdi_without_null) | (hdi_without_null > 1.0)].count())

#check gdp
print('\nGDP FOR YEAR TYPE:', who_data[" gdp_for_year ($) "].dtypes)
gdp_int = pd.to_numeric(who_data[' gdp_for_year ($) '].map(lambda x: 
                                x.replace(',', '')), errors = 'coerce')
null_gdp = gdp_int.isnull()
print("NUMBER OF NULL VALUES:", null_gdp.sum())
print("NUMBER OF NEGATIVE VALUES:", gdp_int[gdp_int < 0].count())

#%% 1c) Clean and transform the data into the correct datatypes

#format age column to remove years from data
who_data['age'] = who_data['age'].map(lambda x: x.replace(" years", ""))
who_data.rename(columns = {'age': 'age (years)'}, inplace=True)

#set suicide null values to 0
print("NUMBER OF SUICIDE VALUES EQUAL TO 0: ", who_data.suicides_no[who_data.suicides_no == 0].count())
suicide_int[null_suicide] = 0
who_data.suicides_no = suicide_int

#change GDP to int
who_data[' gdp_for_year ($) '] = gdp_int

#make second dataframe without HDI null values
who_data_with_HDI = who_data[~null_hdi]

#%% 1d) Add a new column “suicides/100k” and generate its data

who_data['suicides/100k'] = who_data.suicides_no/(who_data.population/100000)
print(who_data[['country', 'sex', 'age (years)', 'suicides/100k']].sample(10))

#%% 1e) Add a new column “generation” and fill up its data according to X criteria

#find the lower limit of age
age_lower = who_data['age (years)'].map(lambda x: x.replace("-", " "))
age_lower = age_lower.map(lambda x: x.replace("+", " "))
age_lower = age_lower.map(lambda x: int(x.split()[0]))

birthdate = who_data.year - age_lower
range_lower = [1883, 1901, 1928, 1946, 1965, 1981, 1996, 2011]
range_upper = [1900, 1927, 1945, 1964, 1980, 1995, 2010, 2025]
generation_list = ['Lost Generation', 'G.I. Generation', 'Silent', 'Boomers', \
                   'Generation X', 'Millenials', 'Generation Z', 'Generation A']

def find_generation(birth):
    generation = np.NaN
    for i in range(len(range_lower)):
        if (range_lower[i] <= birth) and (range_upper[i] >= birth):
            generation = generation_list[i]
    if generation == np.NaN:
        print("ERROR")
    return generation

who_data['Generation'] = birthdate.map(lambda x: find_generation(x))

print(who_data[['country', 'sex', 'age (years)', 'Generation']].sample(10))

#%% 1f) Add a new column “gdp_per_capita” and fill its data.

#find total population per country per year
gdp_cap = who_data.groupby(['country', 'year']).sum()[['population']]
gdp_cap.rename(columns = {'population':'total population'}, inplace=True)
who_data = pd.merge(who_data, gdp_cap, on=["country", "year"])

#check for null values
print('NULL VALUES OF JOIN:', who_data['total population'].isnull().sum())

#add gdp per capita
who_data['gdp_per_capita'] = who_data[' gdp_for_year ($) '] / who_data['total population']
print(who_data[['country', 'year', 'total population', 'gdp_per_capita']].sample(10))

#%% 1g) Rank countries by total suicides

country_table = who_data.groupby('country')['suicides_no'].sum().sort_values(ascending = False)
print(country_table.head(10))

#%% 1h) Find total suicides by continent

import pycountry_convert as pc

#clean country names to match ISO 3166-1 alpha-2 names
who_data.replace({'Republic of Korea':'Korea, Republic Of', 
                 'Saint Vincent and Grenadines':'Saint Vincent and the Grenadines'}, inplace=True)

#add country code to data
who_data['country code'] = who_data.country.map(lambda x: 
                    pc.country_name_to_country_alpha2(x, cn_name_format="default"))

#find continent
who_data['continent code'] = who_data['country code'].map(lambda x: pc.country_alpha2_to_continent_code(x))
continents = {'AF': 'Africa', 'AS':'Asia', 'EU': 'Europe', 'NA':'North America','OC':'Oceania', 'SA':'South America'}
who_data['continent'] = who_data['continent code'].map(lambda x: continents[x])

#groupby and rank by no suicides
continent_table = who_data.groupby('continent')['suicides_no'].sum().sort_values(ascending = False)
print(continent_table)

#%% 1i) Find correlations between suicides, GDP per capita and population.

corr_df = who_data[['suicides_no', 'population', 'gdp_per_capita']]
print(corr_df.corr(method='pearson'))

#%% 1j) Use appropriate visual notation to visualise total suicides over years.

import matplotlib.pyplot as plt

#show the total number of suicides per year
suicide_year = who_data.groupby('year')['suicides_no'].sum()
plot1 = plt.figure(1)
plt.plot(suicide_year)
plt.xlabel('Year')
plt.ylabel('Total Suicides')
plt.title('Total Suicides per Year')


#find the number data values per year
suicide_value_count = who_data.groupby('year')['suicides_no'].count()
plot2 = plt.figure(2)
plt.plot(suicide_value_count)
plt.xlabel('Year')
plt.ylabel('Number of Values')
plt.title('Total Suicide Datapoints per Year')
plt.show()


#find the average suicide/100k per year
suicide_rate = who_data.groupby('year').mean()['suicides/100k']
plot4 = plt.figure(4)
plt.plot(suicide_rate)
plt.xlabel('Year')
plt.ylabel('Suicides/100k')
plt.title('Rate of Global Suicides per Year')
plt.show()

#compare the rate over individual countries
suicide_rate_ind = suicide_rate = pd.DataFrame(who_data.groupby(['country', 'year'])\
                                               .mean()['suicides/100k'])
uk = suicide_rate.loc['United Kingdom']
france = suicide_rate.loc['France']
usa = suicide_rate.loc['United States']
plot5 = plt.figure(5)
plt.plot(uk, label = 'UK')
plt.plot(france, label = 'France')
plt.plot(usa, label = 'USA')
plt.legend()
plt.title('Suicide Rate Compared')
plt.xlabel('Year')
plt.ylabel('Suicides/100k people')
plt.show()

#%% 1k) Compare suicides by gender over years and state your conclusions
import seaborn as sns
suicide_rate_by_gender = pd.DataFrame(who_data.groupby(['sex', 'year']).mean()['suicides/100k'])
suicide_rate_by_gender.reset_index(inplace=True)

#make line plot of suicide rate per year
sns.set_theme()
sns.lineplot(data=suicide_rate_by_gender, x="year", y='suicides/100k', hue="sex")
plt.show()

#%% 1l) Calculate and Visualise suicides on generation and on age group. 

#find average suicide rate per generation
gen_rate = who_data.groupby('Generation', as_index=False).mean()[['Generation', 'suicides/100k']]
plot1 = plt.figure(1)
sns.barplot(data = gen_rate, x = 'Generation', y='suicides/100k', 
            order = ['G.I. Generation', 'Silent', 'Boomers', \
                   'Generation X', 'Millenials', 'Generation Z'])
plt.show()

age_rate = who_data.groupby('age (years)', as_index=False).mean()[['age (years)', 'suicides/100k']]
plot2 = plt.figure(2)
sns.barplot(data = age_rate.sort_values('age (years)'), x = 'age (years)', y='suicides/100k',
            order = ['5-14','15-24', '25-34', '35-54', '55-74', '75+'])
plt.show()