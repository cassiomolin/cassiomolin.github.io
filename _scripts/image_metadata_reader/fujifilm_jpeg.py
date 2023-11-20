def extract_metadata(maker_note):
    
    film_simulation = get_film_simulation(maker_note)
    grain_effect = get_grain_effect(maker_note)
    grain_size = parse_grain_size(maker_note)
    colour_chrome_effect = parse_colour_chrome_effect(maker_note)
    colour_chrome_effect_blue = parse_colour_chrome_effect_blue(maker_note)
    white_balance = parse_white_balance(maker_note)
    white_balance_shift = parse_white_balance_shift(maker_note)
    dynamic_range = parse_dynamic_range(maker_note)
    highlights = parse_hightlights(maker_note)
    shadows = parse_shadows(maker_note)
    colour = parse_colour(maker_note)
    sharpness = parse_sharpness(maker_note)
    noise_reduction = parse_noise_reduction(maker_note)
    clarity = parse_clarity(maker_note)

    # Acros, Monochrome, and Sepia are not film simulations (at least, not in the EXIF)
    has_colours = is_photographed_with_colours(colour)

    jpeg_settings = {}

    jpeg_settings['film_simulation'] = film_simulation if has_colours else colour
    jpeg_settings['grain_effect'] = grain_effect
    jpeg_settings['grain_size'] = grain_size
    jpeg_settings['colour_chrome_effect'] = colour_chrome_effect
    jpeg_settings['colour_chrome_effect_blue'] = colour_chrome_effect_blue
    jpeg_settings['white_balance'] = white_balance
    jpeg_settings['white_balance_shift'] = white_balance_shift
    jpeg_settings['dynamic_range'] = dynamic_range
    jpeg_settings['highlights'] = highlights
    jpeg_settings['shadows'] = shadows
    if has_colours:
        jpeg_settings['colour'] = colour
    jpeg_settings['sharpness'] = sharpness
    jpeg_settings['noise_reduction'] = noise_reduction
    jpeg_settings['clarity'] = clarity

    return jpeg_settings


def get_film_simulation(maker_note):

    value = maker_note.get(0x1401)
    if value is None:
        return None

    film_simulations = {
        0x0: 'Provia',
        0x200: 'Velvia',
        0x400: 'Velvia',
        0x500: 'Pro Neg. Std',
        0x501: 'Pro Neg. Hi',
        0x600: 'Classic Chrome',
        0x700: 'Eterna',
        0x800: 'Classic Negative',
        0x900: 'Bleach Bypass',
        0xa00: 'Nostalgic Neg'
    }

    return film_simulations.get(value)


def get_grain_effect(maker_note):

    value = maker_note.get(0x1047)
    if value is None:
        return None

    grain_effects = {
        0: 'Off',
        32: 'Weak',
        64: 'Strong'
    }
    
    return grain_effects.get(value)


def parse_grain_size(maker_note):

    value = maker_note.get(0x104c)
    if value is None:
        return None

    grain_sizes = {
        0: 'Off',
        32: 'Small',
        64: 'Large'
    }
    
    return grain_sizes.get(value)


def parse_colour_chrome_effect(maker_note):

    value = maker_note.get(0x1048)
    if value is None:
        return None

    colour_chrome_effects = {
        0: 'Off',
        32: 'Weak',
        64: 'Strong'
    }

    return colour_chrome_effects.get(value)


def parse_colour_chrome_effect_blue(maker_note):
    
    value = maker_note.get(0x104e)
    if value is None:
        return None
    
    colour_chrome_effects = {
        0: 'Off',
        32: 'Weak',
        64: 'Strong'
    }

    return colour_chrome_effects.get(value)


def parse_white_balance(maker_note):

    value = maker_note.get(0x1002)
    if value is None:
        return None

    white_balances = {
        0x0: 'Auto',
        0x1: 'Auto (white priority)',
        0x2: 'Auto (ambiance priority)',
        0x100: 'Daylight',
        0x200: 'Cloudy',
        0x300: 'Daylight Fluorescent',
        0x301: 'Day White Fluorescent',
        0x302: 'White Fluorescent',
        0x303: 'Warm White Fluorescent',
        0x304: 'Living Room Warm White Fluorescent',
        0x400: 'Incandescent',
        0x500: 'Flash',
        0x600: 'Underwater',
        0xf00: 'Custom 1',
        0xf01: 'Custom 2',
        0xf02: 'Custom 3',
        0xf03: 'Custom 4',
        0xf04: 'Custom 5',
        0xff0: 'Kelvin'  # TODO See 0x1005 (Color Temperature)?
    }

    return white_balances.get(value)


def parse_white_balance_shift(maker_note):

    value = maker_note.get(0x100a)
    if value is None:
        return None

    # Must be divided by 20
    red = value[0] // 20 
    blue = value[1] // 20

    # See https://stackoverflow.com/a/2763589/1426227
    return {
        'red': '{0:{1}}'.format(red, '+' if red else ''),
        'blue': '{0:{1}}'.format(blue, '+' if blue else '')
    }

def parse_dynamic_range(maker_note):

    value = maker_note.get(0x1403)
    if value is None:
        return None

    return f"{value}%"


def parse_hightlights(maker_note):

    value = maker_note.get(0x1041)
    if value is None:
        return None

    highlights = {
        -64: '+4',
        -48: '+3',
        -32: '+2',
        -16: '+1',
        0: '0',
        16: '-1',
        32: '-2'
    }

    return highlights.get(value)


def parse_shadows(maker_note):

    value = maker_note.get(0x1040)
    if value is None:
        return None

    shadows = {
        -64: '+4',
        -48: '+3',
        -32: '+2',
        -16: '+1',
        0: '0',
        16: '-1',
        32: '-2'
    }

    return shadows.get(value)


def parse_colour(maker_note):

    value = maker_note.get(0x1003)
    if value is None:
        return None

    colours = {
        0x4e0: '-4',
        0x4c0: '-3',
        0x400: '-2',
        0x180: '-1',
        0x0: '0',
        0x80: '+1',
        0x100: '+2',
        0xc0: '+3',
        0xe0: '+4',
        0x200: 'Low',
        0x300: 'Monochrome',
        0x301: 'Monochrome+R',
        0x302: 'Monochrome+Ye',
        0x303: 'Monochrome+G',
        0x310: 'Sepia',
        0x500: 'Acros',
        0x501: 'Acros+R',
        0x502: 'Acros+Ye',
        0x503: 'Acros+G',
        0x8000: 'Film Simulation'
    }

    return colours.get(value)


def parse_sharpness(maker_note):

    value = maker_note.get(0x1001)
    if value is None:
        return None

    sharpnesses = {
        0x0: '-4',
        0x1: '-3',
        0x2: '-2',
        0x82: '-1',
        0x3: '0',
        0x84: '+1',
        0x4: '+2',
        0x5: '+3',
        0x6: '+4',
    }

    return sharpnesses.get(value)


def parse_noise_reduction(maker_note):

    value = maker_note.get(0x100e)
    if value is None:
        return None

    noise_reductions = {
        0x2e0: '-4',
        0x2c0: '-3',
        0x200: '-2',
        0x280: '-1',
        0x0: '0',
        0x100: '+2',
        0x180: '+1',
        0x1c0: '+3',
        0x1e0: '+4'
    }

    return noise_reductions.get(value)


def parse_clarity(maker_note):

    value = maker_note.get(0x100f)
    if value is None:
        return None

    clarities = {
        -5000: '-5',
        -4000: '-4',
        -3000: '-3',
        -2000: '-2',
        -1000: '-1',
        0: '0',
        1000: '1',
        2000: '2',
        3000: '3',
        4000: '4',
        5000: '5'
    }

    return clarities.get(value)


def parse_colour_temperature(maker_note):
    # TODO: Review this
    return None


def is_photographed_with_colours(parsed_colour):

    if parsed_colour is None:
        return None

    return not (
        "monochrome" in parsed_colour.lower() or
        "acros" in parsed_colour.lower() or
        "sepia" in parsed_colour.lower()
    )
