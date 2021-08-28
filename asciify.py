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
    spaces is whether you want to allow using spaces in new ASCII-file\n"""

    asciis = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    if spaces:
        asciis += ' '
    return asciis[floor(byte/255 * len(asciis))-1]

def asciify(image : bytes, width : int, coefficient = 5, spaces = False):
    """Convert pixel brightness list to string\n
    image is bytes variable, where every byte represents brightness of pixel\n
    width is a number of pixels in a vertical line\n
    coefficient is needed to widen your output (because symbols are high and slim)"""

    result = ""
    for byte in image:
        result += byte_to_ascii(byte, spaces)*coefficient
    return textwrap.wrap(result, width=width*coefficient)

# An implementation for shell
def main(argv : list):
    """Main function"""

    # Setting default parameters (resolution will be set later)
    resolution = None
    coefficient = 5
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
        if arg in ["-h", "--help"]:
            print("Usage: python %s [options] path_to_image" % argv[0].split('/')[-1])
            print("Convert your image to ASCII art")
            print("\nOptions:")
            print("\t-h, --help\t\t\tDisplays this message")
            print("\t-r, --resolution <WIDTHxHEIGHT>\tSets resolution to result")
            print("\t-s, --spaces\t\t\tAllows to use spaces")
            print("\t-c, --coefficient <coefficient>\tSets the propotion coeffecient")
            print("\nArguments:")
            print("\tpath_to_image\t\t\tPath to original image")
            sys.exit()

    # Checking if script is provided with valid path
    if len(argv) < 2:
        raise RuntimeError("You need to provide this script with image. (try python %s -h)"
        % argv[0].split('/')[-1])
    if not os.path.exists(argv[-1]) or not os.path.isfile(argv[-1]):
        raise FileNotFoundError("No such file: %s" % argv[-1])

    # Operations with image
    with Image.open(argv[-1]) as image:

        # If not provided manually, set resolution to original's resolution
        if not resolution:
            resolution = image.size

        image = image.resize(resolution)    # Resize to needed resolution
        image = image.convert("L")          # Convert to grayscale
        image_bytes = image.tobytes()       # Covert PIL.Image.Image to bytes

    result = asciify(image_bytes, resolution[0], coefficient, spaces)
    for line in result:
        print(line)

if __name__ == "__main__":
    main(sys.argv)
