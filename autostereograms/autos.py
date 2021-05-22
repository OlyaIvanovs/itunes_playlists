from PIL import Image


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
