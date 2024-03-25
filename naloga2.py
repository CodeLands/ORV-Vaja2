import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import filedialog

# Main funkcije
def konvolucija(slika, jedro):
    if slika.ndim == 2:
        slika = slika[:, :, np.newaxis]
    
    kernel_height, kernel_width = jedro.shape
    image_height, image_width, num_channels = slika.shape
    pad_height, pad_width = kernel_height // 2, kernel_width // 2
    
    padded_image = np.pad(slika, ((pad_height, pad_height), (pad_width, pad_width), (0, 0)), mode='constant', constant_values=0)
    
    new_image = np.zeros_like(slika)
    
    for i in range(image_height):
        for j in range(image_width):
            for k in range(num_channels):
                new_image[i, j, k] = (jedro * padded_image[i:i+kernel_height, j:j+kernel_width, k]).sum()
    
    if num_channels == 1:
        return new_image[:, :, 0]
    return new_image

def filtriraj_z_gaussovim_jedrom(slika, sigma):
    velikost_jedra = int((2 * sigma) * 2 + 1)
    k = (velikost_jedra - 1) // 2
    gaussovo_jedro = np.fromfunction(lambda x, y: (1 / (2 * np.pi * sigma ** 2)) * np.exp(-((x - k) ** 2 + (y - k) ** 2) / (2 * sigma ** 2)), (velikost_jedra, velikost_jedra), dtype=np.float32)
    #gaussovo_jedro /= gaussovo_jedro.sum()
    
    return konvolucija(slika, gaussovo_jedro)

class ImageApp:
    def __init__(self):
        self.running = True

        self.frame_processed = None
        self.frame_original = None
        self.image_original = None
        self.image_processed = None

        self.frame_overlay = None
        self.image_overlay = None

        self.filter_mode = 1

        self.window_name = "ImageApp"
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        self.window_size = (800, 600)

        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window of tkinter

        self.image_mode_commands = {}
        self.filter_commands = {}
        self.__setup_commands()

        # Initial black screen with "No image" text
        self.__set_image(np.zeros(self.window_size, dtype=np.uint8))  # Start with a black screen
        cv.putText(self.image_processed, "No image", (325, 300), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        self.__show_image()

    def __redraw_window(self, window_name, image):
        cv.destroyWindow(window_name)
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.imshow(window_name, image)
        cv.waitKey(1)
    
    # 1. Commands
    def __setup_commands(self):
        self.image_mode_commands = {
            'l': self.__load_image,
            'o': self.__show_commands,
            'q': self.__stop
        }

        # Shared filter commands
        filter_commands = {
            '1': lambda: self.__apply_filter(1),
            '2': lambda: self.__apply_filter(2),
        }

        self.filter_commands.update(filter_commands)

    def __show_commands(self):
        print("Available commands:")
        commands = self.image_mode_commands
        for command, action in commands.items():
            print(f" - Press '{command}' to {action.__name__}")

    # 2. Utility functions
    # 2.1 Image functions
    def __set_image(self, image):
        self.image_original = cv.resize(image, self.window_size)
        self.image_processed = self.image_original.copy()

    def __load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            image = cv.imread(file_path, cv.IMREAD_COLOR)
            if image is not None:
                self.__set_image(image)
            else:
                print("Error loading image from file.")
        self.__redraw_window(self.window_name, self.image_processed)

    # Filter functions
    def __apply_filter(self, mode):
        self.filter_mode = mode
        if mode == 1:
            # Display original image/frame
            if self.image_original is not None:
                self.image_processed = self.image_original.copy()
        elif mode == 2:
            # Apply Gaussian filter
            if self.image_original is not None:
                self.image_processed = filtriraj_z_gaussovim_jedrom(self.image_processed, sigma=2)

    def __show_image(self):
        if self.image_processed is not None and self.image_processed.size > 0:
            cv.imshow(self.window_name, self.image_processed)
        else:
            print("Napaka: Slika nima veljavnih dimenzij.")


    # Process functions
    def __run(self):
        while self.running:

            self.__show_image()
            cv.waitKey(1)

            key = cv.waitKey(1) & 0xFF
            commands = self.image_mode_commands
            if chr(key) in commands:
                commands[chr(key)]()
            if chr(key) in self.filter_commands:
                self.filter_commands[chr(key)]()

    def __stop(self):
        self.running = False
        cv.destroyAllWindows()

    def start(self):
        self.__run()

if __name__ == "__main__":
    app = ImageApp()
    app.start()