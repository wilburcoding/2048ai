import tkinter as tk
from RangeSlider.RangeSlider import RangeSliderH
from tkinter import ttk


class HistoryDialog(tk.Toplevel):


    def __init__(self, master, history_data):
        super().__init__(master)
        def hex(rgb):
            rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
            return "#%02x%02x%02x" % rgb

        self.title("Board History")
        self.geometry("400x460")
        self.configure(bg="white")
        self.transient(master)
        self.board = [[0 for i in range(4)] for j in range(4)]
        self.grab_set()
        bgcolors = {
            "0": [255, 255, 255],
            "2": [255, 239, 214],
            "4": [255, 209, 138],
            "8": [255, 165, 97],
            "16": [255, 131, 82],
            "32": [255, 99, 87],
            "64": [255, 84, 71],
            "128": [255, 251, 140],
            "256": [255, 250, 97],
            "512": [242, 236, 53],
            "1024": [255, 248, 28],
            "2048": [255, 255, 0],
            "4096": [173, 173, 173]
        }
        # Scrollable canvas frame
        board = tk.Frame(self, bg="black", height=400,width=400)
        board.pack(side="top", fill="y")
        for i in range(4):
            for j in range(4):
                sq = tk.Frame(board, bg="blue", height=100, width=100)
                labe = tk.Label(sq, text="hello", bg="white", font=("Courier", 20), fg="gray1")
                labe.place(relx=0.5, rely=0.5, anchor="center")
                self.board[i][j] = [sq, labe]
                self.board[i][j][0].grid(row=i, column=j)
        slide = tk.Frame(self, bg="white", height=60, width=400)

        def change(value):
            binfo = str(history_data[int(value)-1]).split(",")
            for i in range(16):
                x = i % 4
                y = i // 4
                self.board[y][x][0].configure(bg=hex([int(x) for x in bgcolors[str(binfo[i])]]))
                self.board[y][x][1].configure(text=str(binfo[i]) if binfo[i] != 0 else "", bg=hex([int(x) for x in bgcolors[str(binfo[i])]]), fg="gray1")
        change(1)
        slide.pack(side="bottom", fill="both", expand=True)
        # horizontal slider, [padX] value might be needed to be different depending on system, font and handle size. Usually [padX] = 12 serves,
        hSlider = tk.Scale(
            slide, from_=1, to=len(history_data), orient=tk.HORIZONTAL, label="Move", command=change, background="white", fg="gray1")
        hSlider.pack(fill="both")
