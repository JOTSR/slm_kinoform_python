import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pygame
import cv2
import threading
from src.helpers.ploting import create_saved_plot
from src.widget.custom import CustomFrame, InputFrame, DoubleInputFrame
import src.helpers.camera as camera

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
        P, Q = self.hg_frame.get_values()
        WX, WY = self.grating_frame.get_values()
        A, B = self.rect_frame.get_values()
        W = self.waist_frame.get_value()

        try:
            p, q, wx, wy, a, b, w = int(P), int(Q), int(WX), int(WY), int(A), int(B), int(W)
            pygame.init()

            display_info = pygame.display.get_desktop_sizes()
            if len(display_info) < 2:
                print("No second screen detected!")
                pygame.quit()
                return

            screen_width, screen_height = display_info[1]
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME | pygame.FULLSCREEN, display=1)

            plot_buffer = create_saved_plot(p, q, w, wx, wy, a, b)
            plot_image = pygame.image.load(plot_buffer)
            
            img_width, img_height = plot_image.get_size()


            
            new_width = int(img_width)
            new_height = int(img_height)

            # Scale the image to fit the screen while preserving the aspect ratio
            plot_image = pygame.transform.scale(plot_image, (new_width, new_height))

            # Calculate the position to center the image
            x_offset = (screen_width - new_width) // 2
            y_offset = (screen_height - new_height) // 2
            
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False

                screen.blit(plot_image, (x_offset, y_offset))
                pygame.display.flip()

            pygame.quit()

        except ValueError:
            print("Please enter valid numerical values for the coefficients and parameters.")

    def capture_frames(self):
        camera.capture_frames(self)
        
    def on_exit(self):
        self.stop_camera()
        pygame.quit()
        self.destroy()
