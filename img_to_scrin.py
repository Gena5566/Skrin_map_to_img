import tkinter
import tkintermapview
from PIL import Image, ImageDraw
import os
import io
import logging

# Настройка логирования
logging.basicConfig(filename='map_processing.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для вывода сообщений в терминал
def print_message(message):
    print("[INFO] " + message)

# Define the directory path
directory = '/Users/n.a./Downloads/Map_scrin'

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Функция для создания изображения из данных карты


# Функция для сохранения изображения карты
def save_map_image(image, filename):
    image.save(filename)

# Function to process coordinates, create a map, and save a screenshot
def process_and_save_map(x, y):
    coordinates = f"{x}, {y}"
    print_message(f"Processing map for coordinates: {coordinates}")

    # Create the root window
    root_tk = tkinter.Tk()

    # Get the screen width and height
    screen_width = root_tk.winfo_screenwidth()
    screen_height = root_tk.winfo_screenheight()

    print_message("Getting screen width and height")

    # Calculate the maximum allowed width and height for the map window
    max_width = min(800, screen_width)  # Set the maximum width to 800 pixels or the screen width, whichever is smaller
    max_height = min(800, screen_height)  # Set the maximum height to 800 pixels or the screen height, whichever is smaller

    print_message("Calculating maximum allowed width and height")

    # Calculate the position of the window to keep it centered on the screen
    window_x = max(0, (screen_width - max_width) // 2)
    window_y = max(0, (screen_height - max_height) // 2)

    print_message("Calculating window position")

    # Set the geometry of the root window
    root_tk.geometry(f"{max_width}x{max_height}+{window_x}+{window_y}")

    print_message("Setting root window geometry")

    # Create the map widget
    map_widget = tkintermapview.TkinterMapView(root_tk, width=max_width, height=max_height, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    print_message("Creating map widget")

    # Set current widget position and zoom
    map_widget.set_address(coordinates)
    map_widget.set_zoom(20)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

    print_message("Setting widget position and zoom")

    # Function to save the map
    def save_map():
        try:
            # Create map image from map widget data
            map_image = create_map_image(map_widget, max_width, max_height)

            # Save map image
            save_map_image(map_image, os.path.join(directory, f"map_image_{x}_{y}.png"))

            root_tk.destroy()

        except Exception as e:
            # Log any exceptions that occur during map saving
            logging.error(f"Error occurred while saving map for coordinates {coordinates}: {e}")
            raise  # Re-raise the exception so it's not silently ignored

    # Schedule saving the map after 2 seconds
    root_tk.after(1000, save_map)
    root_tk.mainloop()

    print_message("Main loop exited")

# Изменим начальные координаты
start_x = 52.00 - 0.05
start_y = 38.00 - 0.05

# Шаг в градусах для движения по квадратам
step_size = 0.01

print_message("Starting map processing")

# Первый цикл для движения по вертикали
for i in range(10):
    # Первая координата Y текущего квадрата
    current_y = start_y + i * step_size

    # Второй цикл для движения по горизонтали
    for j in range(10):
        # Первая координата X текущего квадрата
        current_x = start_x + j * step_size

        # Обработка и сохранение карты для текущего квадрата
        try:
            process_and_save_map(current_x, current_y)
        except Exception as e:
            # Log any exceptions that occur during map processing
            logging.error(f"Error occurred while processing map for coordinates {current_x}, {current_y}: {e}")

print_message("Map processing completed")
