import os.path
from PIL import Image
import colorama
from colorama import Back, Fore, Style

def create_resized_image(original_image, target_directory, identifier="", quality=90, max_size=(3000,3000), append_width_to_file_name=True, skip_if_exists=False):

    image = original_image.copy()  # Do not mess up with the original image
    image.thumbnail(max_size, Image.Resampling.LANCZOS)

    if append_width_to_file_name is True:
        file_name = f"{identifier}-{image.width}w.jpg"
    else:
        file_name = f"{identifier}.jpg"

    file_path = os.path.join(target_directory, file_name)

    if skip_if_exists is True and os.path.isfile(file_path) is True:
        print(f'{Fore.YELLOW}Skipping writing image file that already exists: {file_name}{Style.RESET_ALL}')
        return

    image.save(file_path, quality=quality)
    print(f'Created resized image: {file_path}')


def create_resized_images(original_image, target_directory, identifier="", quality=90, max_sizes=[(3000,3000)]):

    for max_size in max_sizes:
        create_resized_image(original_image, target_directory, identifier, quality, max_size)
