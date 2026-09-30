import math
import random
import tkinter as tk


BACKGROUND = "#101714"
PANEL = "#18221e"
PANEL_LIGHT = "#202d27"
TEXT = "#edf3ec"
MUTED = "#8d9d91"
ACCENT = "#d6f36a"

PALETTES = {
    "Cítrico": ["#d6f36a", "#f5a66c", "#f4e5a0", "#8ce0bc"],
    "Océano": ["#75d8d0", "#70a6ed", "#b4e8e0", "#f4d58d"],
    "Atardecer": ["#ff8b72", "#ffc36d", "#e9a4c7", "#ffe3a2"],
}

MODES = ("Órbita", "Lluvia", "Pulso")


class AnimationStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("MOTION STUDIO  /  Laboratorio de movimiento")
        self.root.geometry("1180x760")
        self.root.minsize(850, 580)
        self.root.configure(bg=BACKGROUND)

        self.mode = tk.StringVar(value="Órbita")
        self.palette = tk.StringVar(value="Cítrico")
        self.speed = tk.DoubleVar(value=1.0)
        self.running = True
        self.frame = 0
        self.scene_size = (0, 0)
        self.particles = []
        self.ripples = []

        self._build_layout()
        self.canvas.bind("<Configure>", self._resize_scene)
        self.canvas.bind("<Button-1>", self._add_ripple)
        self.root.after(80, self._animate)

    def _build_layout(self):
        sidebar = tk.Frame(self.root, bg=PANEL, width=278)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg=PANEL)
        brand.pack(fill="x", padx=24, pady=(25, 34))
        tk.Label(brand, text="✳", fg=ACCENT, bg=PANEL, font=("Segoe UI", 21)).pack(side="left")
        tk.Label(
            brand,
            text="MOTION\nSTUDIO",
            fg=TEXT,
            bg=PANEL,
            font=("Segoe UI", 10, "bold"),
            justify="left",
        ).pack(side="left", padx=(10, 0))

        self._section_label(sidebar, "ESCENA")
        for mode in MODES:
            button = tk.Radiobutton(
                sidebar,
                text=mode,
                variable=self.mode,
                value=mode,
                indicatoron=False,
                anchor="w",
                padx=13,
                pady=10,
                bg=PANEL,
                fg=MUTED,
                selectcolor=PANEL_LIGHT,
                activebackground=PANEL_LIGHT,
                activeforeground=TEXT,
                font=("Segoe UI", 10),
                relief="flat",
                bd=0,
                cursor="hand2",
            )
            button.pack(fill="x", padx=20, pady=2)

        self._section_label(sidebar, "PALETA", top=27)
        for name, color in (("Cítrico", "#d6f36a"), ("Océano", "#75d8d0"), ("Atardecer", "#ff8b72")):
            row = tk.Frame(sidebar, bg=PANEL)
            row.pack(fill="x", padx=20, pady=3)
            tk.Label(row, text="●", fg=color, bg=PANEL, font=("Segoe UI", 12)).pack(side="left", padx=(8, 9))
            tk.Radiobutton(
                row,
                text=name,
                variable=self.palette,
                value=name,
                indicatoron=False,
                anchor="w",
                padx=5,
                pady=6,
                bg=PANEL,
                fg=MUTED,
                selectcolor=PANEL_LIGHT,
                activebackground=PANEL_LIGHT,
                activeforeground=TEXT,
                font=("Segoe UI", 9),
                relief="flat",
                bd=0,
                cursor="hand2",
            ).pack(side="left", fill="x", expand=True)

        self._section_label(sidebar, "VELOCIDAD", top=28)
        tk.Scale(
            sidebar,
            from_=0.2,
            to=2.4,
            resolution=0.1,
            orient="horizontal",
            variable=self.speed,
            showvalue=False,
            bg=PANEL,
            fg=TEXT,
            troughcolor="#34443b",
            activebackground=ACCENT,
            highlightthickness=0,
            bd=0,
            sliderrelief="flat",
        ).pack(fill="x", padx=24, pady=(2, 0))
        tk.Label(sidebar, text="LENTA                               RÁPIDA", fg=MUTED, bg=PANEL, font=("Segoe UI", 8)).pack(anchor="w", padx=25)

        tk.Frame(sidebar, bg="#2b3931", height=1).pack(fill="x", padx=22, pady=(28, 15))
        self.play_button = tk.Button(
            sidebar,
            text="Ⅱ   Pausar animación",
            command=self._toggle_play,
            bg=ACCENT,
            fg="#172016",
            activebackground="#e3ff91",
            activeforeground="#172016",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            pady=12,
            cursor="hand2",
        )
        self.play_button.pack(fill="x", padx=22)
        tk.Button(
            sidebar,
            text="↺   Reiniciar escena",
            command=self._reset_scene,
            bg=PANEL_LIGHT,
            fg=TEXT,
            activebackground="#2b3931",
            activeforeground=TEXT,
            font=("Segoe UI", 9),
            relief="flat",
            bd=0,
            pady=10,
            cursor="hand2",
        ).pack(fill="x", padx=22, pady=(8, 0))

        tk.Label(
            sidebar,
            text="PYTHON  ·  TKINTER  ·  60 FPS",
            fg="#65756a",
            bg=PANEL,
            font=("Segoe UI", 8),
        ).pack(side="bottom", pady=19)

        content = tk.Frame(self.root, bg=BACKGROUND)
        content.pack(side="left", fill="both", expand=True, padx=30, pady=25)

        topbar = tk.Frame(content, bg=BACKGROUND)
        topbar.pack(fill="x", pady=(0, 20))
        heading = tk.Frame(topbar, bg=BACKGROUND)
        heading.pack(side="left")
        tk.Label(heading, text="LABORATORIO VISUAL", fg=ACCENT, bg=BACKGROUND, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(heading, text="Formas en movimiento", fg=TEXT, bg=BACKGROUND, font=("Segoe UI", 21, "bold")).pack(anchor="w", pady=(4, 0))
        self.status = tk.Label(topbar, text="●  EN DIRECTO", fg=ACCENT, bg=BACKGROUND, font=("Segoe UI", 8, "bold"))
        self.status.pack(side="right", anchor="s", pady=(0, 7))

        stage = tk.Frame(content, bg="#202b25", padx=1, pady=1)
        stage.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(stage, bg="#111a16", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True)

        footer = tk.Frame(content, bg=BACKGROUND)
        footer.pack(fill="x", pady=(13, 0))
        tk.Label(footer, text="PULSA EL LIENZO PARA CREAR ONDAS", fg=MUTED, bg=BACKGROUND, font=("Segoe UI", 8, "bold")).pack(side="left")
        self.frame_label = tk.Label(footer, text="PARTÍCULAS  084", fg=MUTED, bg=BACKGROUND, font=("Segoe UI", 8))
        self.frame_label.pack(side="right")

    def _section_label(self, parent, text, top=0):
        tk.Label(
            parent,
            text=text,
            fg="#91a196",
            bg=PANEL,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=25, pady=(top, 8))

    def _resize_scene(self, _event=None):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width > 2 and height > 2 and self.scene_size != (width, height):
            self._build_scene(width, height)

    def _build_scene(self, width, height):
        self.scene_size = (width, height)
        self.canvas.delete("all")
        center_x, center_y = width / 2, height / 2
        radius = min(width, height) * 0.36
        for scale in (0.42, 0.68, 1.0):
            ring = radius * scale
            self.canvas.create_oval(
                center_x - ring,
                center_y - ring,
                center_x + ring,
                center_y + ring,
                outline="#26342c",
                width=1,
            )
        self.canvas.create_oval(center_x - 42, center_y - 42, center_x + 42, center_y + 42, fill="#18241d", outline="#344b35", width=1)
        self.canvas.create_oval(center_x - 25, center_y - 25, center_x + 25, center_y + 25, fill="#273725", outline="")
        self.canvas.create_text(center_x, center_y, text="✳", fill=ACCENT, font=("Segoe UI", 21))

        random.seed(27)
        self.particles = []
        for index in range(84):
            phase = random.random() * math.tau
            orbit = random.uniform(0.12, 0.98)
            size = random.choice((2, 2, 3, 3, 4))
            trail = self.canvas.create_line(0, 0, 0, 0, fill="#526246", width=1, capstyle="round")
            dot = self.canvas.create_oval(0, 0, 0, 0, fill=ACCENT, outline="")
            self.particles.append({
                "phase": phase,
                "orbit": orbit,
                "size": size,
                "trail": trail,
                "dot": dot,
                "previous": None,
                "fall": random.uniform(0.7, 1.8),
            })
        self.ripples = []

    def _animate(self):
        if self.scene_size != (self.canvas.winfo_width(), self.canvas.winfo_height()):
            self._resize_scene()
        if self.running and self.particles:
            self.frame += 1
            width, height = self.scene_size
            center_x, center_y = width / 2, height / 2
            max_radius = min(width, height) * 0.36
            palette = PALETTES[self.palette.get()]
            speed = self.speed.get()

            for index, particle in enumerate(self.particles):
                phase = particle["phase"]
                if self.mode.get() == "Órbita":
                    angle = phase + self.frame * 0.012 * speed
                    orbit = particle["orbit"] * max_radius
                    x = center_x + math.cos(angle) * orbit
                    y = center_y + math.sin(angle * 0.76 + phase) * orbit * 0.76
                elif self.mode.get() == "Lluvia":
                    x = ((index / len(self.particles)) * width + math.sin(phase + self.frame * 0.018) * 25) % width
                    y = (phase / math.tau * (height + 50) + self.frame * particle["fall"] * speed * 1.5) % (height + 50) - 25
                else:
                    angle = phase + self.frame * 0.006 * speed
                    wave = ((phase / math.tau + self.frame * 0.003 * speed) % 1.0)
                    orbit = (0.12 + wave * 0.88) * max_radius
                    x = center_x + math.cos(angle) * orbit
                    y = center_y + math.sin(angle) * orbit * 0.78

                color = palette[index % len(palette)]
                size = particle["size"]
                previous = particle["previous"]
                if previous is not None:
                    self.canvas.coords(particle["trail"], previous[0], previous[1], x, y)
                    self.canvas.itemconfigure(particle["trail"], fill=color if self.mode.get() == "Lluvia" else "#26342c")
                self.canvas.coords(particle["dot"], x - size, y - size, x + size, y + size)
                self.canvas.itemconfigure(particle["dot"], fill=color)
                particle["previous"] = (x, y)

            self._animate_ripples()

        self.root.after(16, self._animate)

    def _add_ripple(self, event):
        color = PALETTES[self.palette.get()][0]
        item = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=color, width=2)
        self.ripples.append({"x": event.x, "y": event.y, "radius": 0, "item": item})

    def _animate_ripples(self):
        for ripple in self.ripples[:]:
            ripple["radius"] += 2.8 * self.speed.get()
            radius = ripple["radius"]
            self.canvas.coords(
                ripple["item"],
                ripple["x"] - radius,
                ripple["y"] - radius,
                ripple["x"] + radius,
                ripple["y"] + radius,
            )
            if radius > 100:
                self.canvas.delete(ripple["item"])
                self.ripples.remove(ripple)

    def _toggle_play(self):
        self.running = not self.running
        if self.running:
            self.play_button.configure(text="Ⅱ   Pausar animación")
            self.status.configure(text="●  EN DIRECTO", fg=ACCENT)
        else:
            self.play_button.configure(text="▶   Reanudar animación")
            self.status.configure(text="Ⅱ  EN PAUSA", fg="#f5a66c")

    def _reset_scene(self):
        self.frame = 0
        self.ripples.clear()
        self._build_scene(*self.scene_size)


def main():
    root = tk.Tk()
    AnimationStudio(root)
    root.mainloop()


if __name__ == "__main__":
    main()