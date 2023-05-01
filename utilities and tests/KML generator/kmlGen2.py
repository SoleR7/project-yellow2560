import csv
from simplekml import Kml, Style, LineStyle

# Define the input and output file paths
input_file = 'LOG2.CSV'
output_file = 'racing_line2.kml'

# Create a new KML file and set the style for the racing line
kml = Kml()
racing_line_style = Style()
racing_line_style.linestyle = LineStyle(color='ffff0000', width=4)  # Red line, 4-pixel wide line

# Read the telemetry data from the CSV file and create a list of GPS points
with open(input_file) as f:
    reader = csv.reader(f)
    gps_points = []
    current_lap = None
    for row in reader:
        if current_lap is None:
            current_lap = row[10]
        elif current_lap != row[10]:
            # If we've reached a new lap, create a new line string in the KML file
            line = kml.newlinestring(name=f'Lap {current_lap} Racing Line')
            line.coords = gps_points
            line.style = racing_line_style
            gps_points = []
            current_lap = row[10]
        
        # Add the GPS point to the list
        gps_points.append((float(row[4]), float(row[3]), float(row[9])))

    # Create the last line string for the last lap
    line = kml.newlinestring(name=f'Lap {current_lap} Racing Line')
    line.coords = gps_points
    line.style = racing_line_style

# Create the KML file with the racing lines
kml.save(output_file)
