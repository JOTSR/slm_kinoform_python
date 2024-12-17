import pygame
from src.helpers.ploting import create_saved_plot

def full_screen(app):
    P, Q = app.hg_frame.get_values()
    WX, WY = app.grating_frame.get_values()
    A, B = app.rect_frame.get_values()
    W = app.waist_frame.get_value()
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

def close():
    pygame.quit()
