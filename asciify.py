"""Asciify implementation for shell. If you need just the library - check out lib_asciify.py"""

import os
import sys
from math import floor
from PIL import Image
from lib_asciify import asciify, deasciify

# An implementation for shell
def print_help(filename):

    """Prints help message"""

    print("\nUsage: python %s [options] path_to_image" % filename)
    print("Convert your image to ASCII art")
    print("\nOptions:")
    print("\t-h, --help\t\t\tDisplays this message")
    print("\t-d, --deasciify <path>\t\tConvert ASCII art from path_to_image into regular image")
    print("\t-r, --resolution <WIDTHxHEIGHT>\tSets resolution to result")
    print("\t-s, --spaces\t\t\tAllows to use spaces")
    print("\t-c, --coefficient <coefficient>\tSets the propotion coefficient")
    print("\nArguments:")
    print("\tpath_to_image\t\t\tPath to original image\n")

def check_usage(argv):

    """Checking if script is provided with valid path"""

    if len(argv) < 2:
        print_help(argv[0].split('/')[-1])
        raise RuntimeError("You need to provide this script with image.")
    if not os.path.exists(argv[-1]):
        raise FileNotFoundError("No such file: %s" % argv[-1])
    if not os.path.isfile(argv[-1]):
        raise IsADirectoryError("%s is a directory." % argv[-1])

def main(argv : list):

    """Main function"""

    # Setting default parameters (resolution will be set later, path_to_ascii is optional)
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

    # Checking usage
    check_usage(argv)

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
