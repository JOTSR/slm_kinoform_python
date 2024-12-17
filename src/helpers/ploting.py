from io import BytesIO
from src.compute.draw import grating, kinoform, rect
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

def plot_graph(app):
    P, Q = app.hg_frame.get_values()
    WX, WY = app.grating_frame.get_values()
    A, B = app.rect_frame.get_values()
    W = app.waist_frame.get_value()
    try:
        p, q, wx, wy, a, b, w = int(P), int(Q), int(WX), int(WY), int(A), int(B), int(W)
        buf = create_saved_plot(p, q, w, wx, wy, a, b)
        fig, ax = plt.subplots()
        ax.imshow(plt.imread(buf), cmap='gray')
        plt.axis('off')
        if app.canvas:
            app.canvas.get_tk_widget().destroy()
        app.canvas = FigureCanvasTkAgg(fig, master=app)
        app.canvas.get_tk_widget().grid(row=0, column=1, rowspan=5, padx=10, pady=(10, 0))
        app.canvas.draw()
    except ValueError:
        print("Please enter valid numerical values for the coefficients and parameters.")
