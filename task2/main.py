"""
tk_image_app.py — Tkinter + ООП + работа с изображениями.
Загрузка изображений из папки images/.
"""

import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os


class ImageApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tkinter OOP Image Template")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="#222")
        self.canvas.pack(fill="both", expand=True)

        self.btn_load = tk.Button(root, text="Загрузить изображение из папки images", command=self.load_image)
        self.btn_load.pack(pady=5)

        self.image_obj = None

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self._drag_start_x = 0
        self._drag_start_y = 0

    def load_image(self):
        filename = simpledialog.askstring(
            "Имя файла",
            "Введите имя файла из папки images (например: cat.png):"
        )
        if not filename:
            return

        full_path = os.path.join("images", filename)

        if not os.path.exists(full_path):
            print(f"Файл не найден: {full_path}")
            return

        if self.image_obj:
            self.image_obj.delete()

        self.image_obj = ImageObject(self.canvas, full_path)

    def on_mouse_down(self, event):
        if self.image_obj:
            self._drag_start_x = event.x
            self._drag_start_y = event.y

    def on_mouse_drag(self, event):
        if self.image_obj:
            dx = event.x - self._drag_start_x
            dy = event.y - self._drag_start_y
            self.image_obj.move(dx, dy)
            self._drag_start_x = event.x
            self._drag_start_y = event.y

    def on_mouse_wheel(self, event):
        if self.image_obj:
            scale = 1.1 if event.delta > 0 else 0.9
            self.image_obj.scale_at(event.x, event.y, scale)


class ImageObject:
    def __init__(self, canvas: tk.Canvas, filepath: str):
        self.canvas = canvas
        self.filepath = filepath

        self.original_image = Image.open(filepath)

        self.scale_factor = 1.0

        self.tk_image = ImageTk.PhotoImage(self.original_image)

        self.x = canvas.winfo_width() // 2
        self.y = canvas.winfo_height() // 2

        self.canvas_id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.canvas_id, dx, dy)

    def scale_at(self, center_x, center_y, factor):
        self.scale_factor *= factor

        # TODO Задание 1:
        # 1. new_w = int(self.original_image.width * self.scale_factor)
        #    new_h = int(self.original_image.height * self.scale_factor)
        # 2. resized = self.original_image.resize((new_w, new_h))
        # 3. self.tk_image = ImageTk.PhotoImage(resized)
        # 4. self.canvas.itemconfig(self.canvas_id, image=self.tk_image)

        new_w = int(self.original_image.width * self.scale_factor)
        new_h = int(self.original_image.height * self.scale_factor)

        resized = self.original_image.resize((new_w, new_h))
        self.tk_image = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.canvas_id, image=self.tk_image)

    def delete(self):
        self.canvas.delete(self.canvas_id)


# TODO Задание 2:
# Создать класс ImageWithBorder(ImageObject)
# Добавить рамку rectangle.
# Добавить движение рамки вместе с изображением.
# Добавить масштабирование рамки.


# TODO Задание 3:
# Создать класс ImageRotatable(ImageObject)
# Добавить self.angle = 0
# Сделать метод rotate(...)
# Поворачивать через original.rotate(angle, expand=True)
# Обновлять tk_image + itemconfig().


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
