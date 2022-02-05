# Remove background from PNG files, Convert PNG files into GIF files, Resize GIF file, Mirror the GIF file
import os
from PIL import Image, ImageOps

dir = "/Users/sachin/Downloads/convert/"
formats = [".jpeg", ".png", ".gif"]
transparency = 0  # 0 for transparent and 1 for not transparent
resize = True
convert = False
flip = False

for file_name in sorted(os.listdir(dir)):
    for format in formats:
        if file_name.endswith(format):
            img = Image.open(dir + file_name)
            if resize:
                img = img.resize((100, 80))
                img.save(dir + file_name)
            if convert:
                img.save(dir + file_name.replace(format, '.gif'), format='GIF', transparency=transparency)
            if flip:
                img_flip = ImageOps.mirror(img)
                img_flip.save(dir + file_name.replace(format, '_flipped'+format), format='GIF', transparency=transparency)
