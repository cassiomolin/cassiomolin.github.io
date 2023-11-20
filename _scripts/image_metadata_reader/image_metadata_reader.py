from PIL import ExifTags, Image, ImageOps
from PIL.ExifTags import IFD, Base
from datetime import datetime
import itertools

import image_metadata_reader.aspect_ratio as aspect_ratio
import image_metadata_reader.camera as camera
import image_metadata_reader.dominant_colour as dominant_colour
import image_metadata_reader.exposure as exposure
import image_metadata_reader.file as file
import image_metadata_reader.fujifilm_jpeg as fujifilm_jpeg
import image_metadata_reader.lens as lens
import image_metadata_reader.gps as gps

metadata_version = '0.0.1'

def get_exif_tags(exif):
    return {
        ExifTags.TAGS[key]: value
        for key, value in itertools.chain(exif.items(), exif.get_ifd(IFD.Exif).items())
        if key in ExifTags.TAGS
    }


def get_gps_tags(exif):
    return {
        ExifTags.GPSTAGS[key]: value
        for key, value in exif.get_ifd(IFD.GPSInfo).items()
        if key in ExifTags.GPSTAGS
    }


def get_maker_note(exif):
    try:
        return exif.get_ifd(IFD.Makernote)
    except:
        return {}


def get_date_time(exif_tags):
    date_time = exif_tags.get(Base.DateTimeOriginal.name)
    if date_time is None:
        return None
    return datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')


def extract_metadata(image):

    exif = image.getexif()
    exif_tags = get_exif_tags(exif)
    gps_tags = get_gps_tags(exif)
    maker_note = get_maker_note(exif)

    # for key, value in maker_note.items():
    #     print(f"{key:#0{6}x}: {value}")

    date_time = get_date_time(exif_tags)

    ratio = aspect_ratio.calculate(image.width, image.height)
    colour = dominant_colour.calculate(image)

    file_metadata = file.extract_metadata(image.filename)
    camera_metadata = camera.extract_metadata(exif_tags)
    lens_metadata = lens.extract_metadata(exif_tags)
    exposure_metadata = exposure.extract_metadata(exif_tags)
    gps_metadata = gps.extract_metadata(gps_tags)
    fujifilm_jpeg_metadata = fujifilm_jpeg.extract_metadata(maker_note)

    return {
        'metadata_version': metadata_version,
        'date_time': date_time.strftime("%Y-%m-%d %H:%M:%S") if date_time else None,
        'aspect_ratio': ratio,
        'dominant_colour': colour,
        'original_file': file_metadata,
        'camera': camera_metadata,
        'lens': lens_metadata,
        'exposure': exposure_metadata,
        'gps': gps_metadata,
        'fujifilm_jpeg': fujifilm_jpeg_metadata,
    }
