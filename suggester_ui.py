import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np
import pandas as pd


class SearcherUI(tk.Tk):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__()
        self.__df = dataframe
        self.title("Board Game Suggester")
        self.geometry("1500x700")
        self.resizable(False, False)
        self.init_component()

    def init_component(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=9)
        self.rowconfigure(2, weight=9)
        self.create_menu()
        self.__search_frame = self.create_search_frame()
        tree_frame = self.create_tree_frame()
        fig_frame = self.create_figure_frame()
        self.__search_frame.grid(column=0, row=0, sticky="ew", padx=200)
        tree_frame.grid(column=0, row=1, sticky="ew", padx=80)
        fig_frame.grid(column=0, row=2, sticky="ew", padx=30)

    def create_menu(self):
        menubar = tk.Menu(self)
        search_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Search by", menu=search_menu)
        for i in list(self.__df.columns):
            search_menu.add_command(label=i)
        self.config(menu=menubar)

    def create_search_frame(self):
        frame = tk.LabelFrame(self, text="Search board game by ID")
        self.__search_text = tk.StringVar()
        self.__search_box = tk.Entry(frame, textvariable=self.__search_text)
        self.__sort_box = ttk.Menubutton(frame, text="Sort by")
        sort_menu = tk.Menu(self.__sort_box, tearoff=False)
        for i in list(self.__df.columns):
            sort_menu.add_checkbutton(label=i)
        self.__sort_box.config(menu=sort_menu)
        self.__search_button = tk.Button(frame, text="Search")
        frame.columnconfigure(0, weight=18)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        self.__search_box.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
        self.__sort_box.grid(column=1, row=0, sticky="ew", padx=5, pady=5)
        self.__search_button.grid(column=2, row=0, sticky="ew", padx=5, pady=5)
        return frame

    def create_tree_frame(self):
        frame = tk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        head = list(self.__df.columns)
        self.__tree = ttk.Treeview(frame, columns=head, show="headings", height=15)
        scroll_x = tk.Scrollbar(frame, orient="horizontal", command=self.__tree.xview)
        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.__tree.yview)
        self.__tree.config(xscrollcommand=scroll_x.set)
        self.__tree.config(yscrollcommand=scroll_y.set)
        for i in head:
            self.__tree.heading(i, text=i)
        scroll_x.grid(column=0, row=1, sticky="ew")
        scroll_y.grid(column=1, row=0, sticky="ns")
        self.__tree.grid(column=0, row=0, sticky="nsew")
        return frame

    def create_figure_frame(self):
        frame = tk.Frame(self)
        self.__fig1 = Figure(figsize=(3, 2.5))
        self.__fig2 = Figure(figsize=(3, 2.5))
        self.__fig3 = Figure(figsize=(3, 2.5))
        self.__fig4 = Figure(figsize=(3, 2.5))
        self.__ax1 = self.__fig1.add_subplot()
        self.__ax2 = self.__fig2.add_subplot()
        self.__ax3 = self.__fig3.add_subplot()
        self.__ax4 = self.__fig4.add_subplot()
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        frame.rowconfigure(0, weight=1)
        self.__canvas1 = FigureCanvasTkAgg(self.__fig1, master=frame)
        self.__canvas1.get_tk_widget().grid(column=0, row=0, padx=8, sticky="ew")
        self.__canvas2 = FigureCanvasTkAgg(self.__fig2, master=frame)
        self.__canvas2.get_tk_widget().grid(column=1, row=0, padx=8, sticky="ew")
        self.__canvas3 = FigureCanvasTkAgg(self.__fig3, master=frame)
        self.__canvas3.get_tk_widget().grid(column=2, row=0, padx=8, sticky="ew")
        self.__canvas4 = FigureCanvasTkAgg(self.__fig4, master=frame)
        self.__canvas4.get_tk_widget().grid(column=3, row=0, padx=8, sticky="ew")
        return frame

    def run(self):
        self.mainloop()
