![](./output/light/bake_icon.png)
![](./output/light/texture_icon.png)
![](./output/light/rename_icon.png)
![](./output/light/object_index_icon.png)
![](./output/light/hemi_icon.png)

# Ucupaint icons

### Setup
1. Get Python
2. Run `pip install -r requirements.txt`

Blender native icons can be explored via the official "Icon Viewer" addon and source files for them can be found in `release/datafile/icons_svg` folder of the Blender repository.

### Build process
1. Export the icon sheets at 4096x4096px as `{light/dark/legacy}.png` into the `source/sheets` folder
2. Run `python build.py`