import math

# See https://gist.github.com/Integralist/4ca9ff94ea82b0e407f540540f1d8c6c
def calculate(width, height):

    if width == height:
        return "1:1"

    r = math.gcd(width, height)
    x = int(width / r)
    y = int(height / r)
    return f"{x}:{y}"
    