import math
from PIL.ExifTags import GPS


def extract_metadata(gps_tags):

    altitude = get_altitude(gps_tags)
    latitude = get_latitude(gps_tags)
    longitude = get_longitude(gps_tags)

    return {
        'altitude': f"{altitude}m" if altitude else None,
        'latitude': latitude,
        'longitude': longitude
    }


def get_altitude(gps_tags):
    altitude = gps_tags.get(GPS.GPSAltitude.name)
    if altitude is None or is_nan(altitude):
        return None
    return int(altitude)


def get_latitude(gps_tags):
    latitude = gps_tags.get(GPS.GPSLatitude.name)
    reference = gps_tags.get(GPS.GPSLatitudeRef.name)
    return format_coordinate(latitude, reference)


def get_longitude(gps_tags):
    longitude = gps_tags.get(GPS.GPSLongitude.name)
    reference = gps_tags.get(GPS.GPSLongitudeRef.name)
    return format_coordinate(longitude, reference)


def format_coordinate(coordinate, reference):

    if coordinate is None or len(coordinate) != 3 or reference is None:
        return None

    degrees = coordinate[0]
    minutes = coordinate[1]
    seconds = coordinate[2]

    if is_nan(degrees) or is_nan(minutes) or is_nan(seconds):
        return None

    degrees = int(degrees)
    minutes = int(minutes)
    return f"{degrees}°{minutes}'{seconds}\"{reference}"


def is_nan(value):
    return math.isnan(float(str(value)))
