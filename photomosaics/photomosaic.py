import os
import random
from PIL import Image
import numpy as np
import argparse


def get_images(image_dir):
    """Given a directory of images, return a list of Images."""
    files = os.listdir(image_dir)  # gathet files in the image_dir directory
    images = []
    for file in files:
        # Get complete filename of the image
        file_path = os.path.abspath(os.path.join(image_dir, file))
        try:
            with open(file_path, 'rb') as f:
                im = Image.open(f)
                images.append(im)
                # Force loading the image data from file
                im.load()
        except:
            print(f"Invalid image: {file_path}")
    return images


def get_average_RGB(image):
    """Calculates the average color value as (r, g, b) for each input image."""
    # Get each tile image as a numpy array
    im = np.array(image)
    # Get the shape of each input image
    w, h, d = im.shape
    # Get the average RGB value
    return tuple(np.average(im.reshape(w*h, d), axis=0))


def split_image(image, size):
    """Split the target image into a grid m*n of smaller images."""
    width, height = image.size[0], image.size[1]
    m, n = size
    tile_width, tile_height = int(width/m), int(height/n)
    # Image list
    imgs = []
    for j in range(m):
        for i in range(n):
            # Append cropped image
            imgs.append(image.crop((i*tile_width, j*tile_height,
                        (i+1)*tile_width, (j+1)*tile_height)))
    return imgs


def get_best_match_index(input_avg, avgs):
    """Find the bast match for a tile from the folder of input images."""
    # Input innage average
    avg = input_avg

    # Get the closest RGB value to input, based on RGB distance
    index = 0
    min_index = 0
    min_dist = float("inf")  # minim distance to infinity
    for val in avgs:
        dist = ((val[0] - avg[0])*(val[0] - avg[0]) + (val[1] - avg[1])
                * (val[1] - avg[1]) + (val[2] - avg[2])*(val[2] - avg[2]))
        if dist < min_dist:
            min_dist = dist
            min_index = index
        index += 1
    return min_index


def create_image_grid(images, dims):
    """Create a grid of images of size m*n"""
    m, n = dims  # grid size

    # Sanity check
    # check if number of supplied images matches the grid size
    assert m*n == len(images)

    # Get the maximun height and width of the images. Don't assume thay are equal
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])

    # Create the target image
    grid_img = Image.new('RGB', (n*width, m*height))

    # Paste the tile images into the image grid
    for index in range(len(images)):
        row = int(index/n)
        col = index - n*row
        grid_img.paste(images[index], (col*width, row*height))

    return grid_img


def create_photomosaic(target_image, input_images, grid_size, reuse_images=True):
    """Create a photomosaic given target and input images."""
    print("splitting input images...")
    target_images = split_image(target_image, grid_size)

    print("finding image matches...")
    # For each tile, pick one matching input files
    output_images = []
    # For user feedback
    count = 0

    # Calculate the average of the input images
    avgs = []
    for img in input_images:
        avgs.append(get_average_RGB(img))

    for img in target_images:
        avg = get_average_RGB(img)
        # Find the matching index of closest RGB value
        match_index = get_best_match_index(avg, avgs)
        match = input_images[match_index]
        output_images.append(match)
        count += 1

        # Remove the selected image from input if flag set
        if not reuse_images:
            input_images.remove(match)

    print("creating mosaic...")
    # Create photomosaic image from files
    mosaic_image = create_image_grid(output_images, grid_size)

    # display the mosaic
    return mosaic_image


def main():
    """Create photomosaic for the image from input images."""
    parser = argparse.ArgumentParser(
        description="Creates a photomosaic from input images.")
    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--grid-size', nargs=2,
                        dest='grid_size', required=True)
    parser.add_argument('--output-file', dest='outfile', required=False)

    args = parser.parse_args()

    target_image = Image.open(args.target_image)

    # input images
    print('reading input folder...')
    input_images = get_images(args.input_folder)
    # Check if any valid input images found
    if input_images == []:
        print(f"No input images found in {args.input_folder}")
        exit()

    # Shuffle list to get more varied output
    random.shuffle(input_images)

    # Size of the grid
    grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

    # Output
    output_filename = 'mosaic.png'
    if args.outfile:
        output_filename = args.outfile

    # Reuse any image in input
    reuse_images = True
    # Resize the input to fit the original image size
    resize_input = True

    print('starting photomosaic creation...')
    # If images can't be reused, ensure m*n <= num_of_images
    if not reuse_images:
        if grid_size[0]*grid_size[1] > len(input_images):
            print("Grid size less than number of images.")
            exit()

    # Resizing input
    if resize_input:
        print("resizing images...")
        # For given grid size,  compute the max width and height of tiles
        tile_dims = (
            int(target_image.size[0]/grid_size[1]), int(target_image.size[1]/grid_size[1]))
        print(f"max tile dims: {tile_dims}")
        # resize
        for img in input_images:
            img.thumbnail(tile_dims)

    # Create photomosaic
    mosaic_image = create_photomosaic(
        target_image, input_images, grid_size, reuse_images)

    # Write out mosaic
    mosaic_image.save(output_filename, 'PNG')
    print(f"saved output to {output_filename}")


if __name__ == "__main__":
    main()


images = get_images('imgs')
for img in images:
    a = get_average_RGB(img)
    print(a)
