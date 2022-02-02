# Remove background from PNG files, Convert PNG files into GIF files, Mirror the GIF file
import os
from PIL import Image, ImageOps

dir = "/Users/sachin/Downloads/convert/"  # e.g. "/Users/sachin/Downloads/convert/"
format = ".png"  # eg. ".png"
transparent = 0  # 0 or 1 for true or false respectively
flip = True  # True or False

for file_name in sorted(os.listdir(dir)):
    if file_name.endswith(format):
        img = Image.open(dir + file_name)
        img.save(dir + file_name.replace(format, '.gif'), format='GIF', transparency=transparent)
        if flip:
            img_flip = ImageOps.mirror(img)
            img_flip.save(dir + file_name.replace('.png', '_flipped.gif'), format='GIF', transparency=0)
