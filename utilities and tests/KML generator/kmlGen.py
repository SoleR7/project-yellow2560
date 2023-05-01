import csv
from simplekml import Kml, Style

# Open the CSV file
with open('LOG.CSV') as csvfile:
    reader = csv.reader(csvfile)

    # Create a new KML object
    kml = Kml()

    # Create a new style for the line
    line_style = Style()
    line_style.linestyle.color = 'ff0000ff'  # Blue color
    line_style.linestyle.width = 5

    # Create a new folder to hold the placemarks
    folder = kml.newfolder(name='My Placemarks')

    # Loop through each row in the CSV file
    for row in reader:
        # Extract the timestamp, latitude, and longitude columns from the row
        timestamp, _, _, latitude, longitude, *_ = row

        # Create a new placemark with the timestamp as its name
        placemark = folder.newpoint(name=timestamp, coords=[(longitude, latitude)])

        # Apply the line style to the placemark
        placemark.style = line_style

    # Save the KML file
    kml.save('test2.kml')