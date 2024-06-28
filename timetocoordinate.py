import gpxpy
import gpxpy.gpx
from datetime import datetime, timedelta

def read_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        return gpx

def find_nearest_coordinates(gpx, target_time):
    nearest_point = None
    smallest_time_diff = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                time_diff = abs(point.time - target_time)
                if smallest_time_diff is None or time_diff < smallest_time_diff:
                    nearest_point = point
                    smallest_time_diff = time_diff

    if nearest_point:
        return nearest_point.latitude, nearest_point.longitude, nearest_point.time
    else:
        return None

def main():
    file_path = '/Users/harrisonkim/Downloads/Activity16012543623.gpx'  # Replace with your GPX file path

    gpx = read_gpx(file_path)

    while True:
        target_time_str = input("Enter a time in ISO 8601 format (or 'quit' to exit): ")

        if target_time_str.lower() == 'quit':
            break

        try:
            target_time = datetime.fromisoformat(target_time_str.replace('Z', '+00:00'))
        except ValueError:
            print("Invalid time format. Please try again.")
            continue

        # Add 11 minutes to the input time
        target_time += timedelta(minutes=11)

        result = find_nearest_coordinates(gpx, target_time)
        if result:
            latitude, longitude, nearest_time = result
            print(f"Nearest coordinates to {target_time_str} + 11 minutes: {latitude}, {longitude} at {nearest_time}")
        else:
            print(f"No coordinates found for the time {target_time_str} + 11 minutes")

if __name__ == '__main__':
    main()
