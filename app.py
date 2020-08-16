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
                    all())
    station_temp_dict = {date: tobs for station, date, tobs in station_temp_results}
    jsonified_tobs = jsonify(station_temp_dict) 

    session.close

    return (
        
        jsonified_tobs
 
    )

@app.route("/api/v1.0/<start>")
def start_date_data():
    session = Session(engine)

    session.close

    return (
        
        jsonified_start_date_data
 
    )

@app.route("/api/v1.0/<start>/<end>")
def start_and_end_date_data():
    session = Session(engine)

    session.close

    return (
        
        jsonified_start_and_end_date_data
 
    )



if __name__ == "__main__":
    app.run(debug=True)
