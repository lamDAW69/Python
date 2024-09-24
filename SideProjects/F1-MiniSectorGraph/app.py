from flask import Flask, request, send_file, render_template
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd
import io
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def setup_plot():
    """Setup matplotlib for plotting."""
    plotting.setup_mpl()

def get_session_data(year, circuit, session_type):
    """Load session data dynamically."""
    session = ff1.get_session(year, circuit, session_type)
    session.load(laps=True, telemetry=True)
    return session

def get_fastest_lap_telemetry(session, driver):
    """Get telemetry of the fastest lap for a given driver."""
    laps = session.laps.pick_driver(driver)
    fastest_lap = laps.pick_fastest().get_telemetry().add_distance()
    fastest_lap['Driver'] = driver
    return fastest_lap

def calculate_minisectors(telemetry, num_minisectors=25):
    """Calculate minisectors for telemetry data."""
    total_distance = max(telemetry['Distance'])
    minisector_length = total_distance / num_minisectors
    telemetry['Minisector'] = telemetry['Distance'].apply(
        lambda dist: int((dist // minisector_length) + 1)
    )
    return telemetry

def determine_fastest_driver(telemetry):
    """Determine the fastest driver per minisector."""
    average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()
    fastest_driver = average_speed.loc[average_speed.groupby('Minisector')['Speed'].idxmax()]
    fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})
    telemetry = telemetry.merge(fastest_driver, on='Minisector')
    driver_mapping = {driver: idx + 1 for idx, driver in enumerate(telemetry['Fastest_driver'].unique())}
    telemetry['Fastest_driver_int'] = telemetry['Fastest_driver'].map(driver_mapping)
    return telemetry, driver_mapping

def plot_fastest_lap_comparison(telemetry, session, driver_mapping):
    """Generate and return the plot as a PNG image in memory."""
    x = np.array(telemetry['X'].values)
    y = np.array(telemetry['Y'].values)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)
    cmap = ListedColormap(['red', 'white'])  # Adjust colors as needed

    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
    lc_comp.set_array(fastest_driver_array)
    lc_comp.set_linewidth(5)

    plt.rcParams['figure.figsize'] = [18, 10]
    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
    plt.title(f'Comparison of the fastest laps in the {session.event["EventName"]} of {session.event["EventDate"].year}')

    # Create a color bar
    cbar = plt.colorbar(mappable=lc_comp)
    driver_labels = [name for name, idx in driver_mapping.items()]
    cbar.set_ticks([1.5, 2.5])  # Adjust tick positions dynamically if needed
    cbar.set_ticklabels(driver_labels)

    # Save plot to in-memory file
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=300)
    plt.close()
    img.seek(0)

    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        year = int(request.form['year'])
        circuit = request.form['circuit']
        session_type = request.form['session']
        driver1 = request.form['driver1']
        driver2 = request.form['driver2']

        # Setup and load session data
        setup_plot()
        session = get_session_data(year, circuit, session_type)

        # Get telemetry for both drivers
        telemetry_driver1 = get_fastest_lap_telemetry(session, driver1)
        telemetry_driver2 = get_fastest_lap_telemetry(session, driver2)

        # Merge telemetry data
        telemetry = pd.concat([telemetry_driver1, telemetry_driver2], ignore_index=True)

        # Calculate minisectors and determine the fastest driver
        telemetry = calculate_minisectors(telemetry)
        telemetry, driver_mapping = determine_fastest_driver(telemetry)

        # Plot and return the image
        img = plot_fastest_lap_comparison(telemetry, session, driver_mapping)
        return send_file(img, mimetype='image/png')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000)
