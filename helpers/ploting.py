from io import BytesIO
from compute.draw import grating, kinoform, rect
import numpy as np
from PIL import Image

def create_plot(p, q, w, wx, wy, a, b):
    pixels = []
    kpe = kinoform(p, q, w)
    blaze = grating(wx, wy)
    crop = rect(a, b)
    ngridx = 1920
    ngridy = 1080

    for x in range(-ngridx // 2, ngridx // 2):
        row = []
        for y in range(-ngridy // 2, ngridy // 2):
            croping = crop(x, y)
            croped_kpe = croping and kpe(x, y)
            blazed = (croped_kpe + blaze(x, y)) % 256
            row.append(croping and blazed)
        pixels.append(row)

    return np.array(pixels)

def create_saved_plot(p, q, w, wx, wy, a, b):
    image_2d = create_plot(p, q, w, wx, wy, a, b)
    
    img = Image.fromarray(image_2d.astype(np.uint8), 'L')

    img = img.convert("RGBA")

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    
    return buf
