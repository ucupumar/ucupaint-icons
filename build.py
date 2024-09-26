import os
import json
from PIL import Image

# Data
icons = json.load(open('./data/icons.json'))
overlays = json.load(open('./data/overlays.json'))
disabled = json.load(open('./data/disabled.json'))

# Icon sheets
sheet_files = ['light.png', 'dark.png', 'legacy.png']
sheets = [(path, Image.open(f'./source/sheets/{path}')) for path in sheet_files]

padding = 0.115

# Tile extractor
def crop_tile(sheet, index):
    tile_size = sheet[1].width / 10
    col = index % 10
    row = index // 10

    top = row * tile_size + tile_size * padding
    left = col * tile_size + tile_size * padding
    bottom = row * tile_size + tile_size - tile_size * padding
    right = col * tile_size + tile_size - tile_size * padding

    coords = (left, top, right, bottom)
    return sheet[1].crop(coords)

# Tile downscale and save
def save(tile, sheet, name):
    tile = tile.resize((32, 32), Image.Resampling.LANCZOS)

    sheet_base_name = sheet[0].replace('.png', '')

    # Create directory in png folder if it doesn't exist
    directory = f"./output/{sheet_base_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    tile.save(f"./output/{sheet_base_name}/{name}.png")

# Regular
def process_regular(sheet):
    saved = []
    for i in range(len(icons)):
        if icons[i] != '' and icons[i] not in saved:
            tile = crop_tile(sheet, i)
            save(tile, sheet, icons[i])
            saved.append(icons[i])

# Overlays
def process_overlays(sheet):
    for o, (overlay_name, overlay_tiles) in enumerate(overlays.items()):
        # Read overlays from last row of the icon sheet
        overlay = crop_tile(sheet, 90 + o)

        for i in overlay_tiles:
            if i >= len(icons):
                print(f"Warning: Overlay \"{overlay_name}\" is defined for an image index that's out of icon name range ({i}). Skipping.")
                continue

            tile = crop_tile(sheet, i)
            tile.paste(overlay, (0, 0), overlay)
            save(tile, sheet, f"{overlay_name}_{icons[i]}")

# Disabled
def process_disabled(sheet):
    for d in range(len(disabled)):
        i = disabled[d]
        if i >= len(icons):
            print(f"Warning: Disabled icon definition is out of icon name range ({i}). Skipping.")
            continue

        tile = crop_tile(sheet, i)
        alpha = tile.split()[-1]
        alpha = alpha.point(lambda x: int(x * 0.5))
        tile.putalpha(alpha)
        save(tile, sheet, f"disabled_{icons[i]}")

for sheet in sheets:
    print(f"Processing {sheet[0]}")
    process_regular(sheet)
    process_overlays(sheet)
    process_disabled(sheet)