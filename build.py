import json
from PIL import Image

# Data
icons = json.load(open('./data/icons.json'))
overlays = json.load(open('./data/overlays.json'))
disabled = json.load(open('./data/disabled.json'))

# Icon sheet
sheet = Image.open('./svg/sheet.png')
padding = 0.115
vertical_correction = -10
tile_size = sheet.width / 10

# Tile extractor
def crop_tile(index):
    col = index % 10
    row = index // 10

    top = row * tile_size + tile_size * padding + vertical_correction
    left = col * tile_size + tile_size * padding
    bottom = row * tile_size + tile_size - tile_size * padding + vertical_correction
    right = col * tile_size + tile_size - tile_size * padding

    coords = (left, top, right, bottom)
    return sheet.crop(coords)

# Tile downscale and save
def save(tile, name):
    tile = tile.resize((32, 32), Image.Resampling.LANCZOS)
    tile.save(f"./png/{name}.png")

# Regular
def process_regular():
    saveds = []
    for i in range(len(icons)):
        if icons[i] not in saveds:
            tile = crop_tile(i)
            save(tile, icons[i])
            saveds.append(icons[i])

# Overlays
def process_overlays():
    for o, (overlay_name, overlay_tiles) in enumerate(overlays.items()):
        # Read overlays from last row of the icon sheet
        overlay = crop_tile(90 + o)

        for i in overlay_tiles:
            if i >= len(icons):
                print(f"Warning: Overlay \"{overlay_name}\" is defined for an image index that's out of icon name range ({i}). Skipping.")
                continue

            tile = crop_tile(i)
            tile.paste(overlay, (0, 0), overlay)
            save(tile, f"{overlay_name}_{icons[i]}")

# Disabled
def process_disabled():
    for d in range(len(disabled)):
        i = disabled[d]
        if i >= len(icons):
            print(f"Warning: Disabled icon definition is out of icon name range ({i}). Skipping.")
            continue

        tile = crop_tile(i)
        alpha = tile.split()[-1]
        alpha = alpha.point(lambda x: int(x * 0.5))
        tile.putalpha(alpha)
        save(tile, f"disabled_{icons[i]}")

process_regular()
process_overlays()
process_disabled()
