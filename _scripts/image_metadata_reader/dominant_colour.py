from PIL import Image


def calculate(image: Image, palette_size: int = 16) -> str:
    # See https://stackoverflow.com/a/61730849/1426227

    # Resize image to speed up processing
    img = image.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert(
        'P', palette=Image.Palette.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    return rgb_to_hex(dominant_color[0], dominant_color[1], dominant_color[2])


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
