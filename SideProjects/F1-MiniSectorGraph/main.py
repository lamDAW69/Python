
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap

# Enable the cache
#ff1.Cache.enable_cache('../cache')

# Setup plotting
plotting.setup_mpl()

# Load the session 
session = ff1.get_session(2021, 'Abu Dhabi', 'Q')

# Load the laps and telemetry
session.load(laps=True, telemetry=True)

# Get the laps from the drivers we want to compare
laps_ver = session.laps.pick_driver('VER')
laps_ham = session.laps.pick_driver('HAM')

# Get the telemetry data from their fastest lap
fastest_ver = laps_ver.pick_fastest().get_telemetry().add_distance() 
fastest_ham = laps_ham.pick_fastest().get_telemetry().add_distance()

# Add driver labels
fastest_ver['Driver'] = 'VER'
fastest_ham['Driver'] = 'HAM'

# Merge both lap telemetry DataFrames
import pandas as pd
telemetry = pd.concat([fastest_ver, fastest_ham], ignore_index=True)

#Wwe want 25 mini sector (this can be adjusted up and down)

num_minisector = 25

#Grab the maximu value of distance that is known in the telemetry 

total_distance = total_distance = max(telemetry['Distance']) #This calcluates the total distance of the lap

minisector_length = total_distance / num_minisector #This calculates the length of each minisector

#Initiate minisector variable, with 0 meters as a starting point 
minisectors = [0] 

#Add multiples of the minisector length to the minisector list

for x in range (0, (num_minisector - 1)):
    minisectors.append(minisector_length * (x + 1))

#Add the total distance to the minisector list
telemetry['Minisector'] = telemetry['Distance'].apply(
    lambda dist: (
        int((dist // minisector_length) +1 )
    )
)

#Group the data by minisector and driver
# Calculate avg. speed per driver per mini sector
average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

#Select the driever with highest average speed 
fastest_driver = average_speed.loc[average_speed.groupby('Minisector')['Speed'].idxmax()]

#Ger rid of the speed column and rename the driver column 

fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

#JOin the fastest driver per minisector with full telemtry 

telemetry = telemetry.merge(fastest_driver, on='Minisector')

#Order the data by distance to make matplotlib not consfused

telemetry = telemetry.sort_values(by=['Distance'])

#Convert driver name to integer 
telemetry.loc[telemetry['Fastest_driver'] == 'VER', 'Fastest_driver_int'] = 1
telemetry.loc[telemetry['Fastest_driver'] == 'HAM', 'Fastest_driver_int'] = 2

# Generate 'x' and 'y' coordinates from telemetry data
x = np.array(telemetry['X'].values)
y = np.array(telemetry['Y'].values)

# Create segments for the line collection
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create an array representing the fastest driver
fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)

# Ensure the values are 1 and 2
fastest_driver_array[~np.isin(fastest_driver_array, [1, 2])] = np.nan

# Define a custom colormap
cmap = ListedColormap(['red', 'white'])  # Red for VER, white for HAM

# Create the line collection
lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(fastest_driver_array)
lc_comp.set_linewidth(5)

# Graph settings
plt.rcParams['figure.figsize'] = [18, 10]
plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
plt.title(f'Comparison of the fastest lap between {telemetry["Driver"].iloc[0]} and {telemetry["Driver"].iloc[1]} in the {session.event["EventName"]} of {session.event["EventDate"].year}')
# Create the color bar
cbar = plt.colorbar(mappable=lc_comp, boundaries=[1, 2, 3])
cbar.set_ticks([1.5, 2.5])  # Only two ticks corresponding to the drivers
cbar.set_ticklabels(['VER', 'HAM'])  # Labels for the two ticks

# Save and show the graph
plt.savefig(f"2021_ver_ham_q.png", dpi=300)
plt.show()

print(telemetry)