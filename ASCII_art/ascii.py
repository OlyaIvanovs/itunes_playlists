from PIL import Image
import numpy as np
import argparse
import random
import math


# 70 levels of gray
# "Standard" character ramp for grey scale pictures, black -> white.
GSCALE1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\" ^`'. "

# A more convincing but shorter sequence for representing 10 levels of grey is
GSCALE2 = " .:-=+*#%@"

cols = 80


def get_average_L(image):
    """Compute the average brightness"""
    im = np.array(image)  # Image as PIL image object
    # Get the dimensions
    width, height = im.shape
    # Get the average
    return np.average(im.reshape(width*height))


def convert_image_to_ASCII(filename, cols, scale, more_levels):
    """Given Image, returns an m*n list of Images."""

    # Open the image and convert to grayscale
    # L- luminance, a measure of the brightness
    image = Image.open(filename).convert('L')
    # Store image dimensions
    width, height = image.size[0], image.size[1]
    print(f"Input image dims: {width} * {height}")
    # Compute the tile width
    tile_width = width/cols
    # Compute the tile height based on the aspect ratio and scale of the front
    tile_height = tile_width/scale
    # Compute the number of rows to use in the final grid
    rows = int(height/tile_height)

    print(f"cols: {cols}, rows: {rows}")
    print(f"tile dims: {width} * {height}")

    # Check if image size is too small
    #!!!!!!!!!!!if cols > width or rows

    # ASCII image is a list of character strings
    # An ASCII image is a list of character strings
    aimg = []
    # Generate the list of tile dimensions
    for j in range(rows):
        y1 = int(j*tile_height)
        y2 = int((j+1)*tile_height)
        # Correct the last tile
        if j == rows - 1:
            y2 = height
        # Append an empty string
        aimg.append("")
        for i in range(cols):
            # Crop the image to fit the tile
            x1 = int(i*tile_width)
            x2 = int((i+1)*tile_width)
            # Correct the last tile
            if i == cols-1:
                x2 = width
            # Crop the image to extract the tile into another Image object
            img = image.crop((x1, y1, x2, y2))
            # Get the average luminance
            avg = int(get_average_L(img))
            # Look up the ASCII character for grayscale vaue(avg)
            if more_levels:
                gsval = GSCALE1[int((avg*69)/255)]
            else:
                gsval = GSCALE2[int((avg*9)/255)]
            # Append the ASCII character to the string
            aimg[j] += gsval

    return aimg


def main():
    """Generates ASCII art from image."""
    parser = argparse.ArgumentParser(description="descStr")
    # Add expected arguments
    parser.add_argument('--file', dest='img_file', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='out_file', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--more-levels', dest='more_levels',
                        action='store_true')

    args = parser.parse_args()

    img_file = args.img_file
    # Set output file
    out_file = 'out.txt'
    if args.out_file:
        out_file = args.out_file
    # Set scale default as 0.43(as a Courier font)
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
    # Set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)
    print("generating ASCII art....")
    # Convert image to ASCII text
    aimg = convert_image_to_ASCII(img_file, cols, scale, args.more_levels)

    # Open a new text file
    with open(out_file, 'w') as f:
        # Write each string in the list to the new file
        for row in aimg:
            f.write(row + '\n')
    print(f"ASCII art written to {out_file}")


if __name__ == '__main__':
    main()
