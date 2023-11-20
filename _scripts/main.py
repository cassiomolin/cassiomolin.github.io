from PIL import Image, ImageOps
import yaml
import os
from datetime import datetime
import re
from os.path import isfile, join
from os import listdir
import traceback
import colorama
from colorama import Back, Fore, Style
import sys

from image_metadata_reader import image_metadata_reader
from image_resizer import image_resizer

script_directory = os.path.dirname(__file__)


def fix_orientation(image):
    ImageOps.exif_transpose(image, in_place=True)


def remove_keys_with_null_values(data):

    # See https://stackoverflow.com/a/33529384/1426227
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = remove_keys_with_null_values(v)
        if not v in (u'', None, {}):
            new_data[k] = v
    return new_data


def create_metadata_file(metadata, output_dir, image_identifier, omit_properties_with_null_values=True, skip_if_exists=True):

    if omit_properties_with_null_values == True:
        metadata = remove_keys_with_null_values(metadata)

    file_name = f"{image_identifier}.yml"
    file_path = os.path.join(output_dir, file_name)

    if skip_if_exists is True and os.path.isfile(file_path) is True:
        print(f'{Fore.YELLOW}Skipping writing metadata file that already exists: {file_name}{Style.RESET_ALL}')
        return

    with open(file_path, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)

    print(f'Created metadata file: {file_path}')


def create_image_identifier(metadata, length=5):

    sha256 = metadata.get('original_file', {}).get('sha256')
    if sha256 is None:
        raise RuntimeError(
            'original_file.sha256 could not be found in metadata')
    else:
        return sha256[:length]


def search_for_images(source_path):

    file_paths = []

    # https://stackoverflow.com/a/3207973/1426227
    # https://stackoverflow.com/a/954522/1426227
    for dirpath, dirnames, filenames in os.walk(source_path):
        for filename in [f for f in filenames if re.match(r'^.*\.jpg$', f, re.IGNORECASE)]:
            file_paths.append(os.path.join(dirpath, filename))

    return file_paths


def process_image(image_path, target_config):

    print(f"\n📸 {Fore.GREEN}Processing {image_path}{Style.RESET_ALL}")
    image = Image.open(image_path)
    fix_orientation(image)

    metadata = image_metadata_reader.extract_metadata(image)
    image_identifier = create_image_identifier(metadata, target_config['identifier-length'])

    create_metadata_file(metadata, target_config['path'], image_identifier, skip_if_exists=target_config['skip-if-exists'])

    max_size=(target_config['max-size']['width'], target_config['max-size']['height'])
    image_resizer.create_resized_image(image, target_config['path'], image_identifier, append_width_to_file_name=False, quality=target_config['quality'], max_size=max_size, skip_if_exists=target_config['skip-if-exists'])

    return image_identifier


def delete_content_of_directory(directory):

    file_names = [ f for f in os.listdir(directory) ]

    if len(file_names) == 0:
        print("There are no files to be deleted")
        return

    print(f"The following {len(file_names)} files will be deleted from {directory}: ")
    for file_name in sorted(file_names):
        print(f"  {file_name}")

    if query_yes_no("Do you want to proceed?", default="no") == True:
        for file_name in file_names:
            file_path = os.path.join(directory, file_name)
            print(f"{Fore.YELLOW}Deleting {file_path}{Style.RESET_ALL}")
            os.remove(file_path)


def query_yes_no(question, default="yes"):

    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """

    # See https://stackoverflow.com/a/3041990/1426227
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def print_gallery_syntax(image_identifiers):

    if (not image_identifiers):
        return

    length = len(image_identifiers);
    print(f"Here's the gallery syntax for the {length} image{'s'[:length^1]} that {'has' if length == 1 else 'have'} been processed:")
    print()

    print("{{< photography-gallery min-item-height=\"200\">}}")
    for identifier in sorted(image_identifiers):
        print(f"  {{{{< photograph id=\"{identifier}\" >}}}}")
    print("{{< /photography-gallery >}}")


def read_config(config_file_path):
    try:
        return yaml.safe_load(open(config_file_path))
    except yaml.YAMLError as exc:
        print(exc)


if __name__ == "__main__":

    colorama.init()

    config_file_path = os.path.join(script_directory, "config.yml")
    config = read_config(config_file_path)

    source_config = config['source']
    target_config = config['target']

    if target_config['delete-content'] == True:
        delete_content_of_directory(target_config['path'])

    image_identifiers = []
    image_paths = search_for_images(source_config['path'])

    if (not image_paths):
        print("There are no images to be processed")

    else:
        print()
        print(f"Processing {len(image_paths)} image(s)")
        for image_path in image_paths:
            try:
                image_identifier = process_image(image_path, target_config)
                image_identifiers.append(image_identifier)
            except Exception:
                print(f"{Fore.RED}Ouch! Looks like {image_path} cannot be processed{Style.RESET_ALL}")
                traceback.print_exc()

        print()
        print_gallery_syntax(image_identifiers)
