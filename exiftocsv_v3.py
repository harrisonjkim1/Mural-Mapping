# as of 6/28/34 this works splendidly...

import os
import exifread
import pandas as pd

def get_exif_data(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
    exif_data = {}
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            exif_data[tag] = tags[tag]
    return exif_data

def convert_to_degrees(value):
    d = float(value[0].num) / float(value[0].den)
    m = float(value[1].num) / float(value[1].den)
    s = float(value[2].num) / float(value[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    if 'GPS GPSLatitude' in exif_data and 'GPS GPSLongitude' in exif_data:
        lat = exif_data['GPS GPSLatitude'].values
        lon = exif_data['GPS GPSLongitude'].values
        lat_ref = exif_data.get('GPS GPSLatitudeRef', 'N').values
        lon_ref = exif_data.get('GPS GPSLongitudeRef', 'E').values

        latitude = convert_to_degrees(lat)
        longitude = convert_to_degrees(lon)

        if lat_ref != 'N':
            latitude = -latitude
        if lon_ref != 'E':
            longitude = -longitude

        return latitude, longitude
    return None, None

def extract_exif_from_directory(directory):
    exif_list = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.tiff')):
            image_path = os.path.join(directory, filename)
            exif_data = get_exif_data(image_path)
            latitude, longitude = get_lat_lon(exif_data)
            exif_data['Latitude'] = latitude
            exif_data['Longitude'] = longitude
            exif_data['Filename'] = filename
            exif_list.append(exif_data)
    return exif_list

def save_exif_to_csv(exif_list, output_csv):
    df = pd.DataFrame(exif_list)

    # Renaming columns
    column_renames = {
        'EXIF DateTimeOriginal': 'Date Created',
        'EXIF ExposureTime': 'Exposure Time',
        'EXIF FNumber': 'Aperture',
        'EXIF ISOSpeedRatings': 'ISO Speed',
        'EXIF FocalLength': 'Focal Length',
        'Image Model': 'Camera Model',
        'Filename': 'Image Filename'
    }
    df.rename(columns=column_renames, inplace=True)

    # Removing unwanted columns
    columns_to_remove = [
        'EXIF Flash', 'EXIF WhiteBalance'  # Add any other columns you want to remove
    ]
    df.drop(columns=[col for col in columns_to_remove if col in df.columns], inplace=True)

    # Ensure all required columns are in the DataFrame
    for col in ['Date Created', 'Camera Model', 'Exposure Time', 'Aperture', 'ISO Speed', 'Focal Length', 'Latitude', 'Longitude', 'Image Filename']:
        if col not in df.columns:
            df[col] = None

    # Reordering columns
    columns_order = [
        'Image Filename', 'Date Created', 'Camera Model', 'Exposure Time', 
        'Aperture', 'ISO Speed', 'Focal Length', 'Latitude', 'Longitude'
    ]
    df = df[columns_order]

    # Output debug information
    print("Saving CSV to:", output_csv)
    print(df.head())

    df.to_csv(output_csv, index=False)

# Directory containing the images
image_directory = '/Users/harrisonkim/Pictures/Mural Mapping/day1/JPG'
# Output CSV file path
output_csv_path = '/Users/harrisonkim/Pictures/Mural Mapping/day1/day1exif.csv'

# Extract EXIF data from images in the directory
exif_data_list = extract_exif_from_directory(image_directory)
# Save the EXIF data to a CSV file
save_exif_to_csv(exif_data_list, output_csv_path)

print(f"EXIF data has been saved to {output_csv_path}")