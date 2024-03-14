# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) 
    # to a dictionary using date as the key and prcp as the value
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= pd.to_datetime(session.query(func.max(measurement.date)).scalar()).date() - dt.timedelta(days=365))

    session.close()

    # Create a dictionary from the row data and return as JSON (key = date, value = precipitation)
    precip = []
    for date, prcp in results:
        precip_dict= {}
        precip_dict[date] = prcp
        precip.append(precip_dict)

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset
    results = session.query(station.station).all()

    session.close()

    station_list = {"Station": results}
    
    # for station in results:
    #     station_list.append(station)

    return jsonify(station_list)




if __name__ == '__main__':
    app.run(debug=True)
