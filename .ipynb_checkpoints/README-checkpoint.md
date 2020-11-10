# SQLAlchemy Challenge

<!-- ![surfs-up.png](Images/surfs-up.png) -->

Challenge to analyze climate in Honolulu, Hawaii through the use of a climate database.

Analysis may be found in the [climate.ipynb](https://github.com/szerpa17/sqlalchemy-challenge/blob/master/climate.ipynb) file.

## Tools
* Python
* Python Packages:
    * SQLAlchemy
    * Matplotlib
    * Pandas
    * Scipy - Stats
    * Datetime

## Climate Analysis and Exploration

Used Python and SQLAlchemy to conduct climate analysis and data exploration of the climate database. 

### Precipitation Analysis

* Designed a query to retrieve the last 12 months of precipitation data.

* Selected only the `date` and `prcp` values.

* Loaded the query results into a Pandas DataFrame and set the index to the date column.

* Sorted the DataFrame values by `date`.

* Ploted the results using the DataFrame `plot` method.

* Used Pandas to print the summary statistics for the precipitation data.

![Precipitation data bar plot](https://github.com/szerpa17/sqlalchemy-challenge/blob/master/images/precipitation.png?raw=true)


### Station Analysis

* Designed a query to calculate the total number of stations.

* Designed a query to find the most active stations.

  * Listed the stations and observation counts in descending order.

  * Identified the station with the highest number of observations.

* Designed a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filtered by the station with the highest number of observations.

  * Ploted the results as a histogram with `bins=12`.

![station-histogram](https://github.com/szerpa17/sqlalchemy-challenge/blob/master/images/temperature%20frequency.png?raw=true)

- - -

## Climate App

Designed a Flask API based on the developed queries.

The Flask app may be reviewed [here](https://github.com/szerpa17/sqlalchemy-challenge/blob/master/app.py). 

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


### Temperature Analysis

* Identifed the average temperature in June and December at all stations across all available years in the dataset. 

* Used the t-test to determine whether the difference in the means, if any, is statistically significant. 

#### Results
* Hypothesis:
    * Null: There is no change in Hawaii temperatures, regardless of the month data is obtained in.
    * Alternative: December temperatures are lower in Hawaii

* T-Test Reasoning:
An independent t-test was used because two different months were compared, which means that the months are independent of each other (and samples from two individual groups).

* Results
The small p-value result (pvalue=3.9025129038616655e-191) demonstrates that the Null Hypothesis is not true, therefore, the change in temperatures between June and December is not significant.

### Temperature Analysis II

* Calculated the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").

* Ploted the min, avg, and max temperature from the previous query as a bar chart.

![Trip average temperatures](https://github.com/szerpa17/sqlalchemy-challenge/blob/master/images/trip%20avg%20temp.png?raw=true)


### Daily Rainfall Average

* Calculated the rainfall per weather station using the previous year's matching dates.

* Calculated the daily normals. Normals are the averages for the min, avg, and max temperatures.

* Calculated the normals for each date string and appended the results to a list.

* Loaded the list of daily normals into a Pandas DataFrame and set the index equal to the date.

* Used Pandas to plot an area plot (`stacked=False`) for the daily normals.

![Daily Normals Plot](https://github.com/szerpa17/sqlalchemy-challenge/blob/master/images/temperature%20daily%20normals.png?raw=true)



