from PIL.ExifTags import Base
from fractions import Fraction


def extract_metadata(exif_tags):

    f_number = get_f_number(exif_tags)
    shutter_speed = get_shutter_speed(exif_tags)
    iso = get_iso(exif_tags)
    exposure_compensation = get_exposure_compensation(exif_tags)

    return {
        'f_number': f"f/{f_number}" if f_number else None,
        'shutter_speed': shutter_speed,
        'iso': iso,
        'exposure_compensation': exposure_compensation
    }


def get_f_number(exif_tags):
    f_number = exif_tags.get(Base.FNumber.name)
    if f_number is None:
        return None
    return remove_trailing_dot_zero(f_number)


def get_shutter_speed(exif_tags):
    shutter_speed = exif_tags.get(Base.ExposureTime.name)
    if shutter_speed is None:
        return None
    return str(Fraction(str(shutter_speed)).limit_denominator())


def get_iso(exif_tags):
    iso = exif_tags.get(Base.ISOSpeedRatings.name)
    if iso is None:
        return None
    return str(iso)


def get_exposure_compensation(exif_tags):

    exposure_compensation = exif_tags.get(Base.ExposureBiasValue.name)
    if exposure_compensation is None:
        return None

    exposure_compensation = float(exposure_compensation)
    is_positive = True if exposure_compensation > 0 else False

    exposure_compensation = round(exposure_compensation, ndigits=1)
    exposure_compensation = remove_trailing_dot_zero(
        exposure_compensation)

    if is_positive:
        exposure_compensation = '+' + exposure_compensation

    return exposure_compensation

def remove_trailing_dot_zero(value):
    return ('%f' % value).rstrip('0').rstrip('.')