from flask import Flask, jsonify
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine('sqlite:///Resources/hawaii.sqlite')
connection = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement =  Base.classes.measurement
station = Base.classes.station
session = Session(engine)

# can also specify config in flask

# generates the engine to the correct sqlite file
# Uses automap_base() and reflects the database schema
# Correctly saves references to the tables in the sqlite file
# (measurement and station)
# creates and binds  the session between the python  app and database

# measurement_table = session.query(measurement).all()
# station_table = session.query(station).all()

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
    session.close
    return ("Welcome to Hawaii Climate Analysis API <br/>"
            "Available Routes:<br/>"
            "Precipitation: /api/v1.0/precipitation <br/>"
            "Stations: /api/v1.0/stations <br/>"
            "Temperature Observations: /api/v1.0/tobs <br/>"
            "Min, AVG, Max Temperature: /api/v1.0/<start> and /api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    lastDate = session.query(func.max(measurement.date)).all()[0][0]
    dt_max_date = dt.datetime.strptime(lastDate, '%Y-%m-%d')
    # print(f'Max Date: {dt_max_date}' )

    # Calculate the date 1 year prior to last date in database
    date_year_prior = dt_max_date - dt.timedelta(days=365)
    # print(f'Prior Date: {date_year_prior}')

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date>=date_year_prior).all()
    # for r in results:
    #     print(r)

    precip = {date: prcp for date, prcp in results}
    jsonified = jsonify(precip)

    session.close
    
    return (
        
        jsonified
 
    )



if __name__ == "__main__":
    app.run(debug=True)
