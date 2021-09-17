# SuicideDataAnalysis
### My first project using Pandas, a basic EDA of a dataset of world suicide statistics.


### 1. List all of countries in the dataset

A list of unique values is found using pandas’ unique() function.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_1_countries_unique.png?raw=true)

### 2. Show any problem with the data including missing data, data format etc.

Firstly let’s look at the null values in each column. We can see that there are only two columns with missing values. But we need to check the others to make sure they are all formatted correctly even though they may not have any null values.

We know there is no problem with the __countries__ column as we have already created a list of the unique countries, and all were genuine values, no typos etc.

Next let’s look at the __sex__ column. The easiest way to check the state of this column’s data is to look at the unique values it contains using the pandas ‘unique’ function. We can see that it only contains ‘male’ and ‘female’, with no bad data entries. The type of the data is object, but since we do not need to manipulate the values we shouldn’t need to convert to a string.

Next, the __year__ column. Again by using the unique function we can check there are no odd inputs that don’t fit with the data. This is not the case and all values are formatted correctly as years. By inspecting the type we can see that these are also all integers, which could be useful for calculations later on.

Once again can use the unique function for the __age__ column, and see there are only 6 values, all uniformly formatted, so no problem here either. Although, it’s likely we will want to withdraw the unit, ‘years’,  from the data and specify it in the column title. 

The __suicide values__ column contains too many values for us to inspect them by eye after using the unique function. We can see that the column is of the object type though, so it is going to be necessary to convert to ints. By doing this we can identify what elements of the column aren’t formatted correctly, as they won’t be able to be converted. Making use of the pandas to_numeric() function, with the parameter errors = ‘coerce’, we make every value of the column that cannot be converted into a NaN. We now have the positions of all the incorrectly formatted values. Additionally, another check is carried out to make sure that all the int values obtained are over positive, as a negative amount of suicides would be impossible. This is the case for all values.

The __population__ column is found to be of type int, with no null values and no negative values either. So there is no problem here.

For the __HDI__ for year column, by inspecting the type we see that it is already a float variable. Therefore we find where the null values are using the is.null() function. We can check that all non-null values are between the range of 0 and 1 as anything outside would not be a legitimate HDI value. It is found that all the non-null values are legitimate so we will only need to deal with the null values.

For __GDP__ we know there are no null values, but would like to check to make sure the given values are still reasonable, i.e. positive. To do this we must convert them to integer values, so once again we use pd.to_numeric, then we can count the number of nulls and negative values, and find both at 0.

### 3. Clean and transform the data into the correct data types
Again, let’s look at the columns one at a time. The __sex__ column does not need altering as it only has two values of male or female. __Year__ doesn’t need to be changed either as it is formatted correctly in the int data type.

We format the __age__ column, to remove the unit from the values and put it into the column title. 

Next we have the __number of suicides__. This column contains a large number of null values. In this case, we will set all the null values to 0. This is obviously an assumption that all values with no data are 0, however there is not a single value that is explicitly written as the number 0, so it is a reasonable assumption to make. Given we already have a boolean list of the null values from b), these are easily changed.

The __population__ column is already in the correct data type as shown in b), and the __GDP__ column was already changed into the int type in b), and just needs to be changed in the who_data dataframe. 

As there are a very large number of null values in the __HDI__ column, it doesn’t make any sense to delete entire rows if they have no HDI, nor does it make sense to set null values to 0. As there is no analysis for the rest of the task that requires the HDI value, we shall simply leave the null values as null. But we can make another dataframe cutting out the null value rows for the case that analysis is required.

### 4. Add a new column “suicides/100k” and generate its data
Data is printed using .sample() in order to demonstrate that the desired outcome has been achieved across the whole column.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_2_suicides_per_100k.png)

### 5. Add a new column “generation” and fill up its data according to X criteria.

First we must find the lower limit of age, done by extracting the punctuation from the age range and then splitting into a list, and selecting the lower number.
Next, combining the map and lambda functions can assign a generation to each data value, where the year boundaries and generations are stored in lists.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_3_generation.png)

### 6. Add a new column “gdp_per_capita” and fill its data. GDP per Capita of a country is GDP divided by the population of that country.

In order to be able to calculate the GDP per capita, we need the total population of each country, as the GDP data we have is for the entire population. To get this total population we use the groupby function on the ‘country’ and ‘age’ columns combined with the sum function and make a separate table. Now we have the total population of each country each year, but need to input this back into the main dataframe, which is done using Pandas’ merge function. Note: this method is assuming that the population of children under 5 years is disregarded, as there is no data available for this age range.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_4_gdp_per_capita.png)

### 7. Rank countries by total suicides
Using the groupby and sum functions, can get a list of the countries ranked by suicide (first 10 shown).

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_5_ranked.png)

### 8. Find total suicides by continents
The python library pycountry_convert is used to find the continent in which each country is situated (done by converting to alpha-2 country codes, then to continent codes, then code to continent name through a dictionary).  Finally we can sum and rank the suicides using groupby.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_6_total_continent.png)

### 9. Find correlations between suicides, GDP per capita and population.
It is assumed that the question is asking about the population of each group, not the total population. Correlation is achieved through the pandas function, pandas.DataFrame.corr(), with the method chosen as the standard Pearson method.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_7_correlations.png)

### 10. Use appropriate visual notation to visualise total suicides over years.
We can use groupby to sum the total amount of suicides per year, but when we do so we find an unexpected result.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_8_total_suicides.png)

The sudden drop in numbers in 2015, 2016 is suspicious. One possibility is that there is not sufficient data for these years. To investigate, the sum of the number of data points per year is plotted.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_9_suicide_datapoints.png)

By doing so we can see that not only is the drop off in suicides a result of a drop in the number of data entries, but that the general shape of the graphs are very similar too - we cannot draw any conclusions between the number of suicides and the year.

One alternative is to instead look at the suicide rate, per 100k people. The mean rate can be taken every year. This shouldn’t be affected by the change in the volume of data for different years. 

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_10_suicide_rate.png)

This shows a peak rate around 1994. However, it’s still likely that we can’t draw any useful conclusions from this graph as although the rate may not depend on the number of datapoints, it will depend on which countries are included. I.e. if one country with a high rate is missing one year then the global rate will drop, and it’s not clear if this is true from this graph. Therefore it’s best to stick to looking at individual countries, for example the below graph compares the suicide rate between the UK, France and the USA.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_11_rate_compared.png)

Here it can be seen that the rate has not changed much over the years for the UK or the USA, but for France there’s been a general downtrend.

### 11. Compare suicides by gender over years and state your conclusions.

Here once again we have the same problem if we use total suicides, where there could be years where there are more male groups included than female etc, so once again, the suicide rate shall be utilised. By using groupby and mean on year and gender, we can see how the rate changes for each gender over the years.
We can see here the large difference between the male suicide rate and the female one, with the male rate consistently multiple times higher.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_12_suicides_gender.png)

### 12. Calculate and visualise suicides on generation and on age group. Describe your findings.
The average suicide rate is found for each generation and for each age group, using groupby then plotted using seaborn. Results are shown below.

![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_13_suicides_generation.png)
![alt text](https://github.com/PeterEvansDS/SuicideDataAnalysis/blob/main/images/_14_suicides_age.png)

We can see that there is a clear relationship between the age group/ generation and the suicide rate, with the rate increasing with age. This agrees with previous analysis completed on similar data (Shah, A. (2007). The relationship between suicide rates and age: an analysis of multinational data from the World Health Organization, Cambridge University Press, International Psychogeriatrics, 19(6), 1141-1152. doi:10.1017/S1041610207005285).
