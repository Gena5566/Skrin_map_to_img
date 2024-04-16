import tkinter
import tkintermapview
from PIL import ImageGrab
import os
import logging
import concurrent.futures

# Настройка логирования
logging.basicConfig(filename='map_processing.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для вывода сообщений в терминал
def print_message(message):
    print("[INFO] " + message)

# Определение пути каталога
directory = '/Users/n.a./Downloads/Map_scrin'

# Создание каталога, если его не существует
if not os.path.exists(directory):
    os.makedirs(directory)

# Функция для обработки координат, создания карты и сохранения скриншота
def process_and_save_map(x, y):
    coordinates = f"{x}, {y}"
    print_message(f"Обработка карты для координат: {coordinates}")

    # Создание корневого окна
    root_tk = tkinter.Tk()

    # Получение ширины и высоты экрана
    screen_width = root_tk.winfo_screenwidth()
    screen_height = root_tk.winfo_screenheight()

    print_message("Получение ширины и высоты экрана")

    # Рассчет максимально допустимой ширины и высоты окна для карты
    max_width = min(800, screen_width)  # Максимальная ширина - 800 пикселей или ширина экрана, в зависимости от того, что меньше
    max_height = min(800, screen_height)  # Максимальная высота - 800 пикселей или высота экрана, в зависимости от того, что меньше

    print_message("Рассчет максимально допустимой ширины и высоты")

    # Рассчет позиции окна, чтобы оно оставалось по центру экрана
    window_x = max(0, (screen_width - max_width) // 2)
    window_y = max(0, (screen_height - max_height) // 2)

    print_message("Рассчет позиции окна")

    # Установка геометрии корневого окна
    root_tk.geometry(f"{max_width}x{max_height}+{window_x}+{window_y}")

    print_message("Установка геометрии корневого окна")

    # Создание виджета карты
    map_widget = tkintermapview.TkinterMapView(root_tk, width=max_width, height=max_height, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    print_message("Создание виджета карты")

    # Установка текущей позиции и масштаба
    map_widget.set_position(x, y, 20)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    print_message("Установка текущей позиции и масштаба")

    # Функция для сохранения карты
    def save_map_internal():
        try:
            # Рассчет позиции центра карты
            center_x = max(0, root_tk.winfo_screenwidth() // 2 - 400)
            center_y = max(0, root_tk.winfo_screenheight() // 2 - 400)

            # Создание скриншота области вокруг центра карты
            with ImageGrab.grab(bbox=(center_x, center_y, center_x + 800, center_y + 800)) as image:
                image.save(os.path.join(directory, f"map_image_{x}_{y}.png"))

            # Проверка на существование виджета карты
            if map_widget is not None and map_widget.winfo_exists():
                # Удаление виджета карты
                map_widget.destroy()

            # Закрытие главного окна после 2 секунд
            root_tk.after(2000, root_tk.destroy)

        except Exception as e:
            # Логирование ошибок
            logging.exception(f"Ошибка при сохранении карты для координат {x}, {y}: {e}")

    # Запланировать сохранение карты через 2 секунды
    root_tk.after(5000, save_map_internal)

    # Запуск цикла обработки событий
    root_tk.mainloop()

def main():
    # Определение координат
    x_center = 52.00
    y_center = 38.00
    x_min = x_center - 0.5
    x_max = x_center + 0.5
    y_min = y_center - 0.5
    y_max = y_center + 0.5

    # Запуск обработки координат в пуле процессов
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for x in range(int(x_min * 100), int(x_max * 100) + 1):
            for y in range(int(y_min * 100), int(y_max * 100) + 1):
                executor.submit(process_and_save_map, x / 100, y / 100)

if __name__ == "__main__":
    main()







