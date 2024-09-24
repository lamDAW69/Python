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

def calculate_minisectors(telemetry, num_minisector=25):
    """Calculate minisectors for telemetry data"""
    total_distance = telemetry['Distance'].max()  # Calculate total lap distance
    minisector_length = total_distance / num_minisector  # Length of each minisector

    # Assign minisectors to the telemetry data
    telemetry['Minisector'] = telemetry['Distance'].apply(
        lambda dist: int((dist // minisector_length) + 1)
    )
    return telemetry

def determine_fastest_driver(telemetry):
    """Determine the fastest driver per minisector dynamically and convert driver names to integers"""
    # Calculate average speed per driver and minisector
    average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()

    # Select the driver with the highest average speed in each minisector
    fastest_driver = average_speed.loc[average_speed.groupby('Minisector')['Speed'].idxmax()]

    # Clean up columns
    fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

    # Merge with telemetry data
    telemetry = telemetry.merge(fastest_driver, on='Minisector')

    # Create a dynamic mapping of driver names to integers
    driver_mapping = {driver: idx + 1 for idx, driver in enumerate(telemetry['Fastest_driver'].unique())}

    # Apply the mapping to convert driver names to integers
    telemetry['Fastest_driver_int'] = telemetry['Fastest_driver'].map(driver_mapping)

    return telemetry, driver_mapping


def plot_fastest_lap_comparison(telemetry, session, driver_mapping, output_file='fastest_lap_comparison.png'):
    """Plot the comparison of fastest laps between drivers"""
    # Generate 'x' and 'y' coordinates from telemetry data
    x = np.array(telemetry['X'].values)
    y = np.array(telemetry['Y'].values)

    # Create segments for the line collection
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Fastest driver array
    fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)

    # Define colormap dynamically based on the number of drivers
    cmap = ListedColormap(['red', 'white'])  # Adjust colors if needed

    # Create the line collection for the plot
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
    lc_comp.set_array(fastest_driver_array)
    lc_comp.set_linewidth(5)

    # Plot settings
    plt.rcParams['figure.figsize'] = [18, 10]
    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
    plt.title(f'Comparison of the fastest laps in the {session.event["EventName"]} of {session.event["EventDate"].year}')

    # Create the color bar
    cbar = plt.colorbar(mappable=lc_comp, boundaries=[1, 2, 3])
    
    # Set ticks dynamically based on driver mapping
    driver_labels = [name for name, idx in driver_mapping.items()]
    cbar.set_ticks([1.5, 2.5])  # Adjust ticks based on the number of drivers
    cbar.set_ticklabels(driver_labels)  # Dynamic labels based on the drivers

    # Save and show the graph
    plt.savefig(output_file, dpi=300)
    plt.show()

def main():
    # Enable cache and setup plot
    # enable_cache()  # Uncomment if you want to enable caching
    setup_plot()

    # Load session data
    session = load_session(2021, 'Monaco', 'Q')

    # Get telemetry for both drivers
    telemetry_driver1 = get_fastest_lap_telemetry(session, 'ALO')
    telemetry_driver2 = get_fastest_lap_telemetry(session, 'OCO')

    # Merge telemetry data
    telemetry = pd.concat([telemetry_driver1, telemetry_driver2], ignore_index=True)

    # Calculate minisectors
    telemetry = calculate_minisectors(telemetry)

    # Determine the fastest driver per minisector dynamically
    telemetry, driver_mapping = determine_fastest_driver(telemetry)

    # Plot and compare the laps
    plot_fastest_lap_comparison(telemetry, session, driver_mapping, output_file='2021_ver_ham_q.png')

if __name__ == "__main__":
    main()
