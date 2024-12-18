import customtkinter
import numpy as np
import cv2
import threading
from src.widget.custom import CustomFrame, InputFrame, DoubleInputFrame
import src.helpers.camera as camera
import src.helpers.slm_screen as slm
from src.helpers.ploting import plot_graph
from src.helpers.efficiency import efficiency_calcul
import time
from queue import Queue

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
        
        self.effiency_result = 
        
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
       
        self.eff_button = customtkinter.CTkButton(self, text = "Efficiency", command = self.efficiency_calcul)
        self.eff_button.grid(row=7, column = 0, padx = 5, pady = (20,0))
                             
        self.label_RMS =  customtkinter.CTkLabel(self)
        self.label_RMS.grid(row=8, column=0, padx=10, pady=(5, 0), sticky="w")
        
        self.label_Eff = customtkinter.CTkLabel(self)
        self.label_Eff.grid(row=8, column=0, padx=10, pady=(5, 0), sticky="w")

        self.plot_canvas = customtkinter.CTkCanvas(self,width=350,height=350) 
        self.plot_canvas.grid(row = 0,column = 2,rowspan=3)
        self.plot_canvas.configure(bg= "black")
        
        self.camera_canvas = customtkinter.CTkCanvas(self,width=350,height=350)
        self.camera_canvas.grid(row = 0, column = 5, rowspan = 3 )
        self.camera_canvas.configure(bg= "black")

    def plot_graph(self):
        plot_graph(self)
        
    def start_camera(self):
        if not self.camera_running:
            self.camera_running = True
            self.stop_button.configure(state="normal")
            self.start_button.configure(state="disabled")
            self.camera_thread = threading.Thread(target=self.capture_frames)
            self.timestamp = time.perf_counter_ns()
            self.fps = 10
            self.photo = Queue()
            self.camera_thread.start()
            self.image_update()

    def image_update(self):
        camera.image_update(self)

    def stop_camera(self):
        if self.camera_running:
            self.camera_running = False
            self.stop_button.configure(state="disabled")
            self.start_button.configure(state="normal")

    def full_screen(self):
        slm.full_screen(self)

    def capture_frames(self):
        camera.capture_frames(self)

    def efficiency_calcul(self):
        efficiency_calcul(self)
        
    def on_exit(self):
        self.stop_camera()
        slm.close()
        self.destroy()
