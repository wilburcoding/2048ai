import tkinter as tk
from tkinter import ttk
from matplotlib import rc
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from history import HistoryDialog
import sv_ttk

font = {'family': 'Courier New',
        'weight': 'normal',
        'size': 7}

rc('font', **font)


def e():
    print("e")


class App(tk.Tk):
    def __init__(self, save, step, toggle, reset, history):
        super().__init__()
        sv_ttk.set_theme("dark")
        self.title("2048 AI")
        self.geometry("800x700")
        self.minsize(766, 700)
        self.configure(bg="gray")
        self.grid = [[0 for i in range(4)] for j in range(4)]
        self.plots = [[], []]
        self.move_in = None
        self.moves = [i for i in range(4)]
        self.setup_layout(save, step, toggle, reset, history)

    def setup_layout(self, save, step, toggle, reset, history):
        # Main layout: 3 columns, 2 rows
        self.grid_columnconfigure(0, minsize=100)   # Blue strip
        self.grid_columnconfigure(1, minsize=500)  # Game board
        self.grid_columnconfigure(2, minsize=200)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, minsize=200)
        move_indicator = tk.Frame(self, bg="blue", width=100, height=500)
        move_indicator.grid(row=0, column=0, sticky="nsew")
        move_indicator.grid_rowconfigure(0, minsize=125)
        move_indicator.grid_rowconfigure(1, minsize=125)
        move_indicator.grid_rowconfigure(2, minsize=125)
        move_indicator.grid_rowconfigure(3, minsize=125)
        self.move_in = move_indicator
        movecs = ["lavender", "peach puff", "mint cream", "light cyan"]
        for i in range(4):
            tl = tk.Frame(move_indicator, bg=movecs[i], width=100)
            tl.grid(row=i, column=0, sticky="nsew")
            lf_label = tk.Label(tl, text="~", bg=movecs[i], font=(
                "Courier", 10), fg="gray2")
            lf_label.place(relx=.5, rely=.3, anchor="c")
            self.moves[i] = lf_label

            lf_label = tk.Label(tl, text=["Up", "Down", "Left", "Right"][i], bg=movecs[i],
                                font=("Courier", 10), fg="gray1")
            lf_label.place(relx=.5, rely=.7, anchor="c")

        # Game board
        game_board = tk.Frame(self, bg="white", width=500, height=500)
        game_board.grid(row=0, column=1, sticky="nsew")
        game_board.grid_columnconfigure(0, minsize=125)
        game_board.grid_columnconfigure(1, minsize=125)
        game_board.grid_columnconfigure(2, minsize=125)
        game_board.grid_columnconfigure(3, minsize=125)
        game_board.grid_rowconfigure(0, minsize=125)
        game_board.grid_rowconfigure(1, minsize=125)
        game_board.grid_rowconfigure(2, minsize=125)
        game_board.grid_rowconfigure(3, minsize=125)
        for i in range(4):
            for j in range(4):
                tl = tk.Frame(game_board, bg="white", width=125, height=125)
                tl.grid(row=i, column=j, sticky="nsew")
                lf_label = tk.Label(tl, text="", bg="white",
                                    font=("Courier", 30))
                lf_label.place(relx=.5, rely=.5, anchor="c")
                self.grid[i][j] = [tl, lf_label]

        # Sidebar (thinner now)
        sidebar = tk.Frame(self, bg="lightgray", padx=8, pady=8)
        sidebar.grid(row=0, column=2, sticky="nsew")
        self.sidebar = sidebar

        # Plotting
        fig = Figure(figsize=(1.4, 1.5), dpi=100)
        ax = fig.add_subplot(111)
        x = []
        y = []
        ax.plot(x, y, color='blue')
        ax.set_facecolor("white")
        ax.set_title("Scenarios Searched")

        # Buttons
        self.start = ttk.Button(sidebar, text="Start", command=self.say_hello)
        self.start.pack(
            pady=(0, 3), fill="x")
        self.step = ttk.Button(sidebar, text="Step")
        self.step.pack(pady=(0, 3), fill="x")
        self.save = ttk.Button(sidebar, text="Save")
        self.save.pack(pady=(0, 3), fill="x")
        self.reset = ttk.Button(sidebar, text="Reset")
        self.reset.pack(pady=(0, 3), fill="x")
        self.history = ttk.Button(sidebar, text="History")
        self.history.pack(pady=(0, 3), fill="x")
        self.head = tk.Label(sidebar, text="Debug Stats", bg="lightgray", fg="gray1",
                               font=("Courier", 14, "bold"), anchor="w", justify="left")
        self.head.pack(
            pady=(10, 0), fill="x")
        self.search = tk.Label(sidebar, text="Searched", bg="lightgray", fg="gray1",
                               font=("Courier", 10), anchor="w", justify="left")
        self.search.pack(
            pady=(0, 0), fill="x")
        self.score = tk.Label(sidebar, text="Score", bg="lightgray", fg="gray1",
                              font=("Courier", 10), anchor="w", justify="left")
        self.score.pack(
            pady=(0, 0), fill="x")


        # Bottom bar
        bottom_bar = tk.Frame(self, bg="#ddd", height=200, padx=5, pady=5)
        bottom_bar.grid(row=1, column=0, columnspan=3, sticky="nsew")
        bottom_bar.grid_columnconfigure(0, weight=1)
        canvas = FigureCanvasTkAgg(fig, master=bottom_bar)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", side="left",  expand=True)
        self.plots[0] = [ax, canvas]

        fig = Figure(figsize=(1.4, 1.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter(x, y, color='orange')
        ax.set_facecolor("white")
        ax.set_title("Eval")
        canvas = FigureCanvasTkAgg(fig, master=bottom_bar)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", side="left", expand=True)
        self.plots[1] = [ax, canvas]
        # ttk.Label(bottom_bar, text="Status: Ready", background="#ddd").grid(
        #     row=0, column=0, padx=10, pady=10, sticky="w")
        self.save.configure(text="Save", command=save)
        self.step.configure(text="Step", command=step)
        self.start.configure(text="Start", command=toggle)
        self.reset.configure(text="Reset", command=reset)
        self.history.configure(text="History", command=history)

        print(self.save)
        print('Ready!')

    def say_hello(self):
        print("Button clicked, Hello!")


if __name__ == "__main__":
    app = App(e, e, e,e, e)

    app.mainloop()
    
