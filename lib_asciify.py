"""Library that allows you to convert your image into ASCII-art"""

from math import floor

# Converter functions are here
def byte_to_ascii(byte : bytes, spaces = False):

    """Convert brightness byte to according char\n
    byte is a byte you want to convert\n
    spaces is whether you want to allow using spaces in new ASCII-file"""

    asciis = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    if spaces:
        asciis += ' '
    return asciis[floor(byte/255 * len(asciis)-1)]

def ascii_to_byte(char : chr, spaces = False):

    """Convert char to according brightness byte\n
    ascii is a char you want to convert\n
    spaces is whether spaces are in the ASCII picture"""

    asciis = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    if spaces:
        asciis += ' '
    return (floor(asciis.index(char)/len(asciis) * 255)).to_bytes(1, "big")

def asciify(image : bytes, width : int, coefficient = 1, spaces = False):

    """Convert grayscale bytemap to string\n
    image is a bytes variable, where every byte represents brightness of pixel\n
    width is a number of pixels in a vertical line\n
    coefficient is needed to widen your output (because symbols are high and slim)"""

    result = ""
    for i, byte in enumerate(image):
        result += byte_to_ascii(byte, spaces)*coefficient
        if (i+1) % width == 0:
            result += '\n'

    return result

def deasciify(image : str, coefficent = 1, spaces = False):

    """Convert string into grayscale bytemap\n
    image is a string variable you want to convert\n
    width is a number of pixels in a vertical line\n
    coeffeicient is a coefficient that was used when creating the picture"""

    result = bytes()
    image = image.replace('\n', '')
    for i, char in enumerate(image):
        if not i % coefficent:
            result += ascii_to_byte(char, spaces)
    return result
