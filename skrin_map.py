import tkinter
import tkintermapview
from PIL import ImageGrab

root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{800}")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=800, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

x = 52.6838805
y = 38.6139979

# формируем строку с координатами
coordinates = f"{x}, {y}"

# set current widget position and zoom
map_widget.set_address(coordinates)
map_widget.set_zoom(16)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

def add_marker_event(coords):
    print("Add marker:", coords)
    new_marker = map_widget.set_marker(coords[0], coords[1], text="new marker")

map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=add_marker_event,
                                        pass_coords=True)

def save_map():
    # Сделать скриншот окна tkinter
    x = root_tk.winfo_rootx() + map_widget.winfo_x()
    y = root_tk.winfo_rooty() + map_widget.winfo_y()
    x1 = x + map_widget.winfo_width()
    y1 = y + map_widget.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save("map_image.png")

# Создать кнопку для сохранения карты
save_button = tkinter.Button(root_tk, text="Сохранить карту", command=save_map)
save_button.pack()

root_tk.mainloop()









