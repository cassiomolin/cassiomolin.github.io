from PIL.ExifTags import Base


def extract_metadata(exif_tags):

    manufacturer = get_camera_manufacturer(exif_tags)
    model = get_camera_model(exif_tags)
    software = get_software(exif_tags)

    return {
        'manufacturer': manufacturer,
        'model': model,
        'software': software
    }


def get_camera_manufacturer(exif_tags):
    manufacturer = exif_tags.get(Base.Make.name)
    if manufacturer is None:
        return None
    return manufacturer.rstrip('\x00')


def get_camera_model(exif_tags):
    model = exif_tags.get(Base.Model.name)
    if model is None:
        return None
    return model.rstrip('\x00')


def get_software(exif_tags):
    software = exif_tags.get(Base.Software.name)
    if software is None:
        return None
    return software.rstrip('\x00')
    
