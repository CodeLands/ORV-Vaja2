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

def filtriraj_sobel_horizontalno(slika):
    slika = slika.astype(np.float32)
    sobel_horizontalno_jedro = np.array([[-1, 0, 1],
                                         [-2, 0, 2],
                                         [-1, 0, 1]], dtype=np.float32)
    if slika.ndim == 3:
        slika_gray = cv.cvtColor(slika, cv.COLOR_BGR2GRAY)
    else:
        slika_gray = slika
    filtrirana_slika = konvolucija(slika_gray, sobel_horizontalno_jedro)
    filtrirana_slika = cv.convertScaleAbs(filtrirana_slika)  # Pretvorba v 8-bitno sliko
    filtrirana_slika = cv.normalize(filtrirana_slika, None, 0, 255, cv.NORM_MINMAX)

    return filtrirana_slika

def filtriraj_sobel_vertikalno(slika):
    slika = slika.astype(np.float32)
    sobel_vertikalno_jedro = np.array([[-1, -2, -1],
                                       [ 0,  0,  0],
                                       [ 1,  2,  1]], dtype=np.float32)
    if slika.ndim == 3:
        slika_gray = cv.cvtColor(slika, cv.COLOR_BGR2GRAY)
    else:
        slika_gray = slika
    filtrirana_slika = konvolucija(slika_gray, sobel_vertikalno_jedro)
    filtrirana_slika = cv.convertScaleAbs(filtrirana_slika)  # Pretvorba v 8-bitno sliko
    filtrirana_slika = cv.normalize(filtrirana_slika, None, 0, 255, cv.NORM_MINMAX)
    return filtrirana_slika

def filtriraj_sobel_oboje(slika):
    return cv.bitwise_or(filtriraj_sobel_horizontalno(slika), filtriraj_sobel_vertikalno(slika))



class ImageApp:
    def __init__(self):
        self.running = True # Flag to keep the app running

        self.frame_processed = None # Store the current frame
        self.frame_original = None # Store the original frame before any modifications
        self.image_original = None  # Store the last image shown in image mode
        self.image_processed = None  # Store the last image processed in image mode

        self.frame_overlay = None  # Store the overlay frame
        self.image_overlay = None  # Store the overlay image

        self.camera = None

        self.mode = "image"  # Start in image mode
        self.filter_mode = 1

        self.window_name = "ImageApp"
        cv.namedWindow(self.window_name, cv.WINDOW_NORMAL)
        self.window_size = (800, 600)

        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window of tkinter

        self.image_mode_commands = {}
        self.camera_mode_commands = {}
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

    def __show_overlay(self):
        self.image_overlay = self.image_processed.copy()

        cv.putText(self.image_processed, "Loading...", (350, 300), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
        
        self.__show_image()

        self.image_processed = self.image_overlay

        cv.waitKey(1)

    def __camera_initialize(self):
        if self.camera is None:
            self.camera = cv.VideoCapture(0)
            if not self.camera.isOpened():
                print("Error: Camera could not be accessed.")

    def __camera_release(self):
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def __capture_frame(self):
        if self.mode == "camera":
            self.__set_image(self.frame_original)
            self.__toggle_mode()  # Switch to image mode after capturing

    def __toggle_mode(self):
        if self.mode == "camera":
            self.__camera_release()
            self.mode = "image"
            print("Image mode enabled.")
            # self.__show_image()
        else:
            self.mode = "camera"
            print("Camera mode enabled.")
    
    # 1. Commands
    def __setup_commands(self):
        # Setup commands based on mode
        self.image_mode_commands = {
            'l': self.__load_image,
            's': self.__save_image,
            't': self.__toggle_mode,
            'o': self.__show_commands,
            'f': self.__flip_image,
            'n': self.__negate_image,
            'q': self.__stop
        }

        self.camera_mode_commands = {
            'c': self.__capture_frame,
            't': self.__toggle_mode,
            'o': self.__show_commands,
            'q': self.__stop
        }

        # Shared filter commands
        filter_commands = {
            '1': lambda: self.__apply_filter(1),
            '2': lambda: self.__apply_filter(2),
            '3': lambda: self.__apply_filter(3),
            '4': lambda: self.__apply_filter(4),
            '5': lambda: self.__apply_filter(5),
        }

        self.filter_commands.update(filter_commands)

    def __show_commands(self):
        print("Available commands:")
        commands = self.image_mode_commands if self.mode == "image" else self.camera_mode_commands
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

    def __save_image(self):
        cv.imwrite("saved_image.png", self.image_processed)
        print("Image saved as saved_image.png.")

    def __flip_image(self):
        if self.image_processed is not None:
            self.image_processed = cv.flip(self.image_processed, 1)
            self.image_original = cv.flip(self.image_original, 1)

    def __negate_image(self):
        if self.image_processed is not None:
            self.image_processed = cv.bitwise_not(self.image_processed)

    # Filter functions
    def __apply_filter(self, mode):
        self.filter_mode = mode
        self.__show_overlay()
        if mode == 1:
            # Display original image/frame
            if self.mode == "image" and self.image_original is not None:
                self.image_processed = self.image_original.copy()
        elif mode == 2:
            # Apply Gaussian filter
            if self.mode == "image" and self.image_original is not None:
                self.image_processed = filtriraj_z_gaussovim_jedrom(self.image_processed, sigma=2)
        elif mode == 3:
            # Apply Sobel horizontal filter
            if self.mode == "image" and self.image_original is not None:
                self.image_processed = filtriraj_sobel_horizontalno(self.image_processed)
        elif mode == 4:
            # Apply Sobel vertical filter
            if self.mode == "image" and self.image_original is not None:
                self.image_processed = filtriraj_sobel_vertikalno(self.image_processed)
        elif mode == 5:
            # Apply Sobel both filters
            if self.mode == "image" and self.image_original is not None:
                self.image_processed = filtriraj_sobel_oboje(self.image_processed)

    # Image processing functions
    def __load_camera(self):
        if self.camera is None:
            self.__camera_initialize()

        success, frame = self.camera.read()
        if success:
            self.__show_camera_image(frame)
        else:
            print("Error capturing image from camera.")

    def __show_camera_image(self, frame):
        self.frame_original = frame
        self.frame_processed = frame.copy()
        cv.imshow(self.window_name, self.frame_processed)

    def __show_image(self):
        if self.image_processed is not None and self.image_processed.size > 0:
            cv.imshow(self.window_name, self.image_processed)
        else:
            print("Napaka: Slika nima veljavnih dimenzij.")


    # Process functions
    def __run(self):
        while self.running:

            if self.mode == "image":
                self.__show_image()
                cv.waitKey(1)
            elif self.mode == "camera":
                self.__load_camera()

            
            key = cv.waitKey(1) & 0xFF
            commands = self.image_mode_commands if self.mode == "image" else self.camera_mode_commands
            if chr(key) in commands:
                commands[chr(key)]()
            if chr(key) in self.filter_commands:
                self.filter_commands[chr(key)]()

    def __stop(self):
        self.running = False
        self.__camera_release()
        cv.destroyAllWindows()

    def start(self):
        self.__run()

if __name__ == "__main__":
    app = ImageApp()
    app.start()