"""A script to convert your image into ASCII art"""

# Imports for shell implementation
import sys
import os

# Imports for the converter itself
import textwrap
from math import floor
from PIL import Image

# Converter functions are here
def byte_to_ascii(byte : int, spaces = False):

    """Convert brightness byte to according char\n
    byte is a byte you want to convert\n
    spaces is whether you want to allow using spaces in new ASCII-file"""

    asciis = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    if spaces:
        asciis += ' '
    return asciis[floor(byte/255 * len(asciis))-1]

def ascii_to_byte(ascii : chr, spaces = False):

    """Convert char to according brightness byte\n
    ascii is a char you want to convert\n
    spaces is whether spaces are in the ASCII picture"""

    asciis = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    if spaces:
        asciis += ' '
    return (floor(asciis.index(ascii)/len(asciis) * 255)).to_bytes(1, "big")

def asciify(image : bytes, width : int, coefficient = 1, spaces = False):

    """Convert grayscale bytemap to string\n
    image is a bytes variable, where every byte represents brightness of pixel\n
    width is a number of pixels in a vertical line\n
    coefficient is needed to widen your output (because symbols are high and slim)"""

    result = ""
    for byte in image:
        result += byte_to_ascii(byte, spaces)*coefficient
    return '\n'.join(textwrap.wrap(result, width=width*coefficient))

def deasciify(image : str, coefficent = 1, spaces = False):

    """Convert string into grayscale bytemap\n
    image is a string variable you want to convert\n
    width is a number of pixels in a vertical line\n
    coeffeicient is a coefficient that was used when creating the picture"""

    result = bytes()
    image = image.replace('\n', '')
    for i, char in enumerate(image):
        if not (i % coefficent):
            result += ascii_to_byte(char, spaces)
    return result


# An implementation for shell
def print_help(filename):

    """Prints help message"""

    print("\nUsage: python %s [options] path_to_image" % filename)
    print("Convert your image to ASCII art")
    print("\nOptions:")
    print("\t-h, --help\t\t\tDisplays this message")
    print("\t-d, --deasciify <path>\t\tTakes text file with ASCII art from path_to_image and turns it into png")
    print("\t-r, --resolution <WIDTHxHEIGHT>\tSets resolution to result")
    print("\t-s, --spaces\t\t\tAllows to use spaces")
    print("\t-c, --coefficient <coefficient>\tSets the propotion coefficient")
    print("\nArguments:")
    print("\tpath_to_image\t\t\tPath to original image\n")

def main(argv : list):

    """Main function"""

    # Setting default parameters (resolution will be set later)
    resolution = None
    path_to_ascii = None
    coefficient = 1
    spaces = False

    # Parsing args
    for i, arg in enumerate(argv):
        if arg in ["-r", "--resolution"]:
            temp = argv[i+1].split('x')
            resolution = int(temp[0]), int(temp[1])
        if arg in ["-c", "--coefficient"]:
            coefficient = int(argv[i+1])
        if arg in ["-s", "--spaces"]:
            spaces = True
        if arg in ["-d", "--deasciify"]:
            path_to_ascii = argv[i+1]
        if arg in ["-h", "--help"]:
            print_help(argv[0].split('/')[-1])
            sys.exit()

    # Checking if script is provided with valid path
    if len(argv) < 2:
        print_help(argv[0].split('/')[-1])
        raise RuntimeError("You need to provide this script with image.")
    if not os.path.exists(argv[-1]):
        raise FileNotFoundError("No such file: %s" % argv[-1])
    if not os.path.isfile(argv[-1]):
        raise IsADirectoryError("%s is a directory." % argv[-1])

    # Asciify
    if not path_to_ascii:
        with Image.open(argv[-1]) as image:

            # If not provided manually, set resolution to original's resolution
            if not resolution:
                resolution = image.size

            image = image.resize(resolution)    # Resize to needed resolution
            image = image.convert("L")          # Convert to grayscale
            image_bytes = image.tobytes()       # Covert PIL.Image.Image to bytes

        result = asciify(image_bytes, resolution[0], coefficient, spaces)
        print(result)

    # Deasciify
    else:
        with open(argv[-1], 'r', encoding="utf-8") as ascii_art:
            ascii_content = ascii_art.read()
            
        # If not provided manually, set resolution to original's resolution
        if not resolution:
            resolution = (
                floor(len(ascii_content.split('\n')[0]) / coefficient),
                len(ascii_content.split('\n'))-1)

        deasciified_bytes = deasciify(ascii_content, coefficient, spaces)
        Image.frombytes("L", resolution, deasciified_bytes).save(path_to_ascii)

if __name__ == "__main__":
    main(sys.argv)
