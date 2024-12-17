import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import cv2
import threading
from src.helpers.ploting import create_saved_plot
from src.widget.custom import CustomFrame, InputFrame, DoubleInputFrame
import src.helpers.camera as camera
import src.helpers.slm_screen as slm

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hermite Gauss Generator")
        self.geometry("1000x600")
        self.configure(bg="#2e2e2e")
        self.camera_running = False
        self.camera = None

        self.hg_frame = DoubleInputFrame(self, "Hermite Gauss Coefficients", "P Coefficient", "Q Coefficient")
        self.hg_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.grating_frame = DoubleInputFrame(self, "Grating Parameters", "Wx Parameter", "Wy Parameter")
        self.grating_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.rect_frame = DoubleInputFrame(self, "Rectangle Size", "Dimension a", "Dimension b")
        self.rect_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.waist_frame = InputFrame(self, "Waist Beam", "Beam Waist (w)")
        self.waist_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.plot_button = customtkinter.CTkButton(self, text="Plot Kinoform", command=self.plot_graph)
        self.plot_button.grid(row=4, column=0, padx=10, pady=(20, 0))

        self.full_screen_button = customtkinter.CTkButton(self, text="Full Screen", command=self.full_screen)
        self.full_screen_button.grid(row=5, column=0, padx=10, pady=(20, 0))

        self.start_button = customtkinter.CTkButton(self, text="Start Camera", command=self.start_camera)
        self.start_button.grid(row = 6,column = 0, padx = 5,pady=(20,0))

        self.stop_button = customtkinter.CTkButton(self, text="Stop Camera", command=self.stop_camera, state="disabled")
        self.stop_button.grid(row = 6,column = 1, padx = 5,pady=(20,0))

        self.exit_button = customtkinter.CTkButton(self, text="Exit", command=self.on_exit)
        self.exit_button.grid(row = 6,column = 2, padx = 5,pady=(20,0))

        self.canvas = None

    def plot_graph(self):
        P, Q = self.hg_frame.get_values()
        WX, WY = self.grating_frame.get_values()
        A, B = self.rect_frame.get_values()
        W = self.waist_frame.get_value()

        try:
            p, q, wx, wy, a, b, w = int(P), int(Q), int(WX), int(WY), int(A), int(B), int(W)

            buf = create_saved_plot(p, q, w, wx, wy, a, b)

            fig, ax = plt.subplots()
            ax.imshow(plt.imread(buf), cmap='gray')
            plt.axis('off')

            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=5, padx=10, pady=(10, 0))
            self.canvas.draw()
        except ValueError:
            print("Please enter valid numerical values for the coefficients and parameters.")

    def start_camera(self):
        if not self.camera_running:
            self.camera_running = True
            self.stop_button.configure(state="normal")
            self.start_button.configure(state="disabled")
            self.camera_thread = threading.Thread(target=self.capture_frames)
            self.camera_thread.start()

    def stop_camera(self):
        if self.camera_running:
            self.camera_running = False
            self.stop_button.configure(state="disabled")
            self.start_button.configure(state="normal")

    def full_screen(self):
        slm.full_screen(self)

    def capture_frames(self):
        camera.capture_frames(self)
        
    def on_exit(self):
        self.stop_camera()
        slm.close()
        self.destroy()
