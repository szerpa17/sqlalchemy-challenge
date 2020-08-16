# Dependencies
from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')

import numpy as np
import pandas as pd
import datetime as dt
from scipy import stats

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.sql import label


# Create Engine
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
connection = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement =  Base.classes.measurement
station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def HomePage():
    """Home Page"""
    # session.close
    return ("Welcome to Hawaii Climate Analysis API <br/>"
            "Available Routes:<br/>"
            "Precipitation: /api/v1.0/precipitation <br/>"
            "Stations: /api/v1.0/stations <br/>"
            "Temperature Observations: /api/v1.0/tobs <br/>"
            "Min, AVG, Max Temperature: /api/v1.0/<start> and /api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(func.max(measurement.date)).all()[0][0]
    #print(f'The max date in the dataset is: {last_date}, its type is {type(last_date)} \n')

    # Convert date to datetime format
    dt_max_date = dt.datetime.strptime(last_date, '%Y-%m-%d')

    # Calculate the date 1 year prior to last date in database
    date_year_prior = dt_max_date - dt.timedelta(days=365)
    #print(f'365 days prior to last date in dataset: {year_prior.date()} \n')

    # Perform a query to retrieve the data and precipitation scores
    results = (session.query(measurement.date, measurement.prcp).
            filter(measurement.date>=date_year_prior).
            filter(measurement.prcp != None).
            all())

    precip = {date: prcp for date, prcp in results}
    jsonified_precip = jsonify(precip)

    session.close

    return (
        
        jsonified_precip
 
    )

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_results = (session.query(station.name, station.station).
                group_by(station.name).
                all())
    
    station_dict = {station_id: name for name, station_id in station_results}
    jsonified_stations = jsonify(station_dict ) 
    
    session.close

    return (
        
        jsonified_stations
 
    )

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    station_temp_results = (session.query(measurement.station, measurement.date, measurement.tobs).
                    filter(station.station == 'USC00519281').
                    filter(measurement.tobs != None).
                    all())
    station_temp_dict = {date: tobs for station, date, tobs in station_temp_results}
    jsonified_tobs = jsonify(station_temp_dict) 

    session.close

    return (
        
        jsonified_tobs
 
    )

@app.route("/api/v1.0/<start>")
def start_date_data(start):
    """Fetch minimum temperature, the average temperature, 
    and the max temperature for a given date, 
    or a 404 if not."""

    session = Session(engine)
    dates = session.query(func.min(measurement.date),func.max(measurement.date)).all()[0]
    sel = [measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    single_date_data_return = (session.query(*sel).filter(func.strftime("%Y-%m-%d", measurement.date) == start).all())

    station_temp_dict = {}
    date_list = []

    for row in single_date_data_return:
        if row[0] == None:
            date_list.append(start)
            null_vals = jsonify({"error class": 404, 
                                    "error": f"Date input {start} is not available in the database.",
                                    "recommendations": {"format": "Correct query format is YYYY-MM-dd", 
                                                    "range": f"The database dates range between {dates[0]} and {dates[1]}"}})
            return null_vals
        else:
            station_temp_dict[row[0]] =  {'min temp':row[1], 'avg temp': row[2], 'max temp':row[3]}
            

    jsonified_single_date_data_return = jsonify(station_temp_dict)

    session.close

    return (jsonified_single_date_data_return)

    # except TypeError:
    #     type_error = jsonify({"error class": 404, "error": f"Date input {start} is not in correct format (YYYY-MM-dd)."})
    #     return type_error

    # except:
    #     return {jsonify({"error": f"Date input {start} has no data available"}), 404}

@app.route("/api/v1.0/<start>/<end>")
def start_and_end_date_data():
    """Fetch minimum temperature, the average temperature, 
    and the max temperature for a given start-end range, 
    or a 404 if not."""

    session = Session(engine)

    session.close

    return (
        
        jsonified_start_and_end_date_data
 
    )



if __name__ == "__main__":
    app.run(debug=True)
