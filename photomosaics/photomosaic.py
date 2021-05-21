import os
from PIL import Image
import numpy as np


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


images = get_images('imgs')
for img in images:
    a = get_average_RGB(img)
    print(a)
