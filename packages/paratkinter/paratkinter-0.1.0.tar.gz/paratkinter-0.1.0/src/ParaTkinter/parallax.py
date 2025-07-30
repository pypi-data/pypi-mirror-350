import customtkinter as ctk

class ParallaxManager:
    def __init__(self, window, center_rel=(0.5, 0.5), easing=0.1, fps=60):
        self.window = window
        self.center_relx, self.center_rely = center_rel
        self.easing = easing
        self.delay = int(1000 / fps)
        self.layers = []

        self.target_dx = 0
        self.target_dy = 0
        self.window.bind("<Motion>", self._on_mouse_move)
        self._update_center()
        self._animate()

    def _update_center(self):
        self.center_x = self.window.winfo_width() // 2
        self.center_y = self.window.winfo_height() // 2

    def _on_mouse_move(self, event):
        self._update_center()
        self.target_dx = event.x - self.center_x
        self.target_dy = event.y - self.center_y

    def add_layer(self, widget, base_relx, base_rely, depth):
        layer = {
            "widget": widget,
            "base_relx": base_relx,
            "base_rely": base_rely,
            "depth": depth,
            "current_relx": base_relx,
            "current_rely": base_rely
        }
        self.layers.append(layer)
        widget.place(relx=base_relx, rely=base_rely, anchor="center")

    def _animate(self):
        for layer in self.layers:
            offset_x = self.target_dx * layer["depth"] / self.window.winfo_width()
            offset_y = self.target_dy * layer["depth"] / self.window.winfo_height()
            target_relx = layer["base_relx"] + offset_x
            target_rely = layer["base_rely"] + offset_y

            layer["current_relx"] += (target_relx - layer["current_relx"]) * self.easing
            layer["current_rely"] += (target_rely - layer["current_rely"]) * self.easing

            layer["widget"].place(relx=layer["current_relx"], rely=layer["current_rely"], anchor="center")

        self.window.after(self.delay, self._animate)
