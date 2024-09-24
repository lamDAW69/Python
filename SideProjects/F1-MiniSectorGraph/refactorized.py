import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap


num_minisector = 25

def get_data_session(year, circuit, session_type): 

    #SetUpPlotting 
    plotting.setup_mpl()
    session = ff1.get_session(year, circuit, session_type)

    session.load(laps=True, telemetry=True)
    return session

def get_drivers_laps(session, driver1, driver2): 
    
    laps_driver1 = session.laps.pick_driver(driver1)
    laps_driver2 = session.laps.pick_driver(driver2)

    fastest_lap_driver1 = laps_driver1.pick_fastest().get_telemetry().add_distance()
    fastest_lap_driver2 = laps_driver2.pick_fastest().get_telemetry().add_distance()

    #Add driver labels
    fastest_lap_driver1['Driver'] = driver1
    fastest_lap_driver2['Driver'] = driver2

    #Merge Both Lap Telemetry DataFrames
    telemetry = pd.concat([fastest_lap_driver1, fastest_lap_driver2], ignore_index=True)
    return telemetry

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