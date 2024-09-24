import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap


def enable_cache(cache_path='../cache'):
    """Enable FastF1 cache"""
    ff1.Cache.enable_cache(cache_path)

def setup_plot():
    """Setup the plot style using FastF1's defaults"""
    plotting.setup_mpl()

def load_session(year, location, session_type):
    """Load the session data"""
    session = ff1.get_session(year, location, session_type)
    session.load(laps=True, telemetry=True)
    return session

def get_fastest_lap_telemetry(session, driver_code):
    """Get the fastest lap telemetry for a driver"""
    laps = session.laps.pick_driver(driver_code)
    fastest_lap = laps.pick_fastest().get_telemetry().add_distance()
    fastest_lap['Driver'] = driver_code
    return fastest_lap

def get_minisector(telemetry): 
    #Grab the maximu value of distance that is known in the telemetry
    total_distance = total_distance (max(telemetry['Distance']))
    minisector_length = total_distance / num_minisector

    #initiate minisector variable, with 0 meters as a starting point
    minisectors = [0]

    #Add multiples of the minisector length to the minisector list
    for x in range(0, (num_minisector - 1)):
        minisectors.append(minisector_length * (x + 1))

    telemetry['Minisector'] = telemetry['Distance'].apply(
        lambda dist: (
            int((dist // minisector_length) + 1)
        )
    )

    # Calculate avg. speed per driver per mini sector
    average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

    #Select the driever with highest average speed 
    fastest_driver = average_speed.loc[average_speed.groupby('Minisector')['Speed'].idxmax()]

    #Ger rid of the speed column and rename the driver column 

    fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})
    
    telemetry = telemetry.merge(fastest_driver, on='Minisector')
    
    #Order the data by distance to make matplot not confused

    telemetry = telemetry.sort_values('Distance')
    
    #Convert Driver name to integer
    telemetry.loc[telemetry['Driver'] == 'VER', 'Driver'] = 1
    telemetry.loc[telemetry['Driver'] == 'HAM', 'Driver'] = 2