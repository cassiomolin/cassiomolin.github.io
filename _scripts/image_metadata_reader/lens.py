from PIL.ExifTags import Base


def extract_metadata(exif_tags):

    manufacturer = get_lens_manufacturer(exif_tags)
    model = get_lens_model(exif_tags)
    specification = get_specification(exif_tags)
    focal_length = get_focal_length(exif_tags)
    focal_length_in_35mm_format = get_focal_length_in_35mm_format(exif_tags)

    return {
        'manufacturer': manufacturer,
        'model': model,
        'specification': specification,
        'focal_length': f"{focal_length}mm" if focal_length else None,
        'focal_length_in_35mm_format': f"{focal_length_in_35mm_format}mm" if focal_length_in_35mm_format else None
    }


def get_lens_manufacturer(exif_tags):
    manufacturer = exif_tags.get(Base.LensMake.name)
    if manufacturer is None:
        return None
    return manufacturer.rstrip('\x00')


def get_lens_model(exif_tags):
    model = exif_tags.get(Base.LensModel.name)
    if model is None:
        return None
    return model.rstrip('\x00')


def get_lens_serial_number(exif_tags):
    serial_number = exif_tags.get(Base.LensModel.name)
    if serial_number is None:
        return None
    return serial_number.rstrip('\x00')


def get_specification(exif_tags):

    specification = exif_tags.get(Base.LensSpecification.name)
    if specification is None:

        fixed_focal_length = exif_tags.get(Base.FocalLength.name)
        min_f_number = exif_tags.get(Base.MaxApertureValue.name)

        if fixed_focal_length is None or min_f_number is None:
            return None

        fixed_focal_length = remove_trailing_dot_zero(fixed_focal_length)
        min_f_number = remove_trailing_dot_zero(min_f_number)

        return f"{fixed_focal_length}mm f/{min_f_number}"
    
    else:

        min_focal_length = remove_trailing_dot_zero(specification[0])
        max_focal_length = remove_trailing_dot_zero(specification[1])
        min_f_number_min_focal_length = remove_trailing_dot_zero(specification[2])
        min_f_number_max_focal_length = remove_trailing_dot_zero(specification[3])

        focal_length_range = ''
        if min_focal_length == max_focal_length:
            focal_length_range += min_focal_length
        else:
            focal_length_range += min_focal_length + '-' + max_focal_length
        
        f_number_range = ''
        if min_f_number_min_focal_length == min_f_number_max_focal_length:
            f_number_range += min_f_number_min_focal_length
        else:
            f_number_range += min_f_number_min_focal_length + '-' + min_f_number_max_focal_length

        return f"{focal_length_range}mm f/{f_number_range}"
        


def get_focal_length(exif_tags):
    focal_length = exif_tags.get(Base.FocalLength.name)
    if focal_length is None:
        return None
    return remove_trailing_dot_zero(focal_length)


def get_focal_length_in_35mm_format(exif_tags):
    focal_length_in_35mm_format = exif_tags.get(Base.FocalLengthIn35mmFilm.name)
    if focal_length_in_35mm_format is None:
        return None
    return remove_trailing_dot_zero(focal_length_in_35mm_format)

def remove_trailing_dot_zero(value):
    return ('%f' % value).rstrip('0').rstrip('.')