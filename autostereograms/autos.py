from PIL import Image, ImageDraw
import random
import argparse


def create_tiled_image(tile, dims):
    """Tile a graphics file to create an intermediate image of a set size."""
    img = Image.new('RGB', dims)
    width, height = dims
    tile_width, tile_height = tile.size
    # Calculate the number of tiles needed
    cols = int(width/tile_width) + 1
    rows = int(height/tile_height) + 1
    # Paste the tiles into the image
    for j in range(rows):
        for i in range(cols):
            img.paste(tile, (j*tile_width, i*tile_height))
    return img


def create_random_tile(dims):
    """Create an image tile filled with random circle."""
    img_tile = Image.new('RGB', dims)
    draw = ImageDraw.Draw(img_tile)
    # Set the radius of a random circle to 1% of the smallest of width or height
    radius = int(min(*dims)/100)
    n = 1000  # number of circles
    # Draw random circles
    for i in range(n):
        # minus radius makes sure that circe stays inside tile
        x, y = random.randint(
            0, dims[0]-radius), random.randint(0, dims[1]-radius)
        color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), color)
    return img_tile


def create_autostereogram(depth_map, tile_img):
    """Convert the depth map toa single channel if needed"""
    if depth_map.mode != 'L':
        depth_map = depth_map.convert('L')
    if not tile_img:
        tile_img = create_random_tile((100, 100))
    # Create an image by tiling
    img = create_tiled_image(tile_img, depth_map.size)
    # Create a shifted image using depth map values
    shifted_img = img.copy()
    # Loads image data into memory.
    pix_depth = depth_map.load()
    pix_shifted = shifted_img.load()
    # Shift pixels horizontally based on depth map
    cols, rows = shifted_img.size
    for j in range(rows):
        for i in range(cols):
            xshift = pix_depth[i, j]/10
            xpos = i - tile_img.size[0] + xshift
            if xpos > 0 and xpos < cols:
                pix_shifted[i, j] = pix_shifted[xpos, j]
    return shifted_img


def main():
    """"""
    parser = argparse.ArgumentParser(description="Autosterograms...")
    parser.add_argument('--depth', dest="dm_file", required=True)
    parser.add_argument('--tile', dest="tile_file", required=False)
    parser.add_argument('--out', dest="out_file", required=False)

    args = parser.parse_args()
    # Set the output file
    out_file = 'out.png'
    if args.out_file:
        out_file = args.out_file
    # Set tile
    tile_file = False
    if args.tile_file:
        tile_file = Image.open(args.tile_file)
    # Open depth map
    dm_img = Image.open(args.dm_file)
    # Create stereogram
    as_img = create_autostereogram(dm_img, tile_file)
    # Write output
    as_img.save(out_file)


if __name__ == "__main__":
    main()
