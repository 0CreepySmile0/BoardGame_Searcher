import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np
import pandas as pd
matplotlib.use("TkAgg")


class SearcherUI(tk.Tk):
    def __init__(self, dataframe: pd.DataFrame, graph1: list=None, graph2: str=None,
                 graph3: list=None, graph4: list=None):
        super().__init__()
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError
        self.__df = dataframe
        col = list(dataframe.columns)
        if graph1 is not None:
            if (len(graph1) != 2) or (graph1[0] not in col) or \
                    (graph1[1] not in col) or (graph1[0] == graph1[1]):
                self.__att1 = None
        if graph2 is not None:
            if graph2 not in col:
                self.__att2 = None
        if graph3 is not None:
            if (len(graph3) != 2) or (graph3[0] not in col) or \
                    (graph3[1] not in col) or (graph3[0] == graph3[1]):
                self.__att3 = None
        if graph4 is not None:
            if (len(graph4) != 2) or (graph4[0] not in col) or \
                    (graph4[1] not in col) or (graph4[0] == graph4[1]):
                self.__att4 = None
        self.__att1 = graph1
        self.__att2 = graph2
        self.__att3 = graph3
        self.__att4 = graph4
        self.title("Board Game Suggester")
        self.__init_component()

    def __init_component(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=11)
        self.rowconfigure(3, weight=5)
        self.__current_mod = {"Sort": [], "Filter": [], "Search": "Name"}
        self.__search_trace = ""
        self.__create_menu()
        self.__bar_frame = self.__create_bar_frame()
        self.__search_frame = self.__create_search_frame()
        tree_frame = self.__create_tree_frame()
        fig_frame = self.__create_figure_frame()
        self.__search_frame.grid(column=0, row=0, sticky="ew", padx=200)
        self.__bar_frame.grid(column=0, row=1, sticky="ew", padx=200, pady=5)
        tree_frame.grid(column=0, row=2, sticky="nsew", padx=50)
        fig_frame.grid(column=0, row=3, sticky="nsew")

    def __create_menu(self):
        menubar = tk.Menu(self)
        search_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Search by", menu=search_menu)
        for i in self.__df.columns.values:
            search_menu.add_command(label=i, command=lambda x=i: self.__config_search(x))
        menubar.add_cascade(label="Exit", command=self.destroy)
        self.config(menu=menubar)

    def __create_search_frame(self):
        frame = tk.LabelFrame(self, text="Search board game by Name")
        self.__search_text = tk.StringVar()
        self.__search_box = tk.Entry(frame, textvariable=self.__search_text)
        self.__search_box.bind("<Return>", lambda x: self.__update_tree("", "Search"))
        self.__sort_box = ttk.Menubutton(frame, text="Sort by")
        sort_menu = tk.Menu(self.__sort_box, tearoff=False)
        for i in self.__df.columns.values:
            temp_bool = tk.BooleanVar()
            sort_menu.add_checkbutton(label=i, variable=temp_bool, command=lambda x=i, y=temp_bool: self.__update_tree(x, "Sort", y.get()))
        self.__sort_box.config(menu=sort_menu)
        self.__search_button = tk.Button(frame, text="Search", command=lambda: self.__update_tree("", "Search"))
        frame.columnconfigure(0, weight=18)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        self.__search_box.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)
        self.__sort_box.grid(column=1, row=0, sticky="nsew", padx=5, pady=5)
        self.__search_button.grid(column=2, row=0, sticky="nsew", padx=5, pady=5)
        self.__disable_search_frame()
        return frame

    def __create_bar_frame(self):
        frame = tk.LabelFrame(self, text="")
        frame.columnconfigure(0, weight=1)
        self.__bar = ttk.Progressbar(frame, length=500, mode="determinate")
        self.__bar.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
        return frame

    def __create_tree_frame(self):
        frame = tk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        head = list(self.__df.columns)
        self.__tree = ttk.Treeview(frame, columns=head, show="headings", selectmode="none")
        scroll_x = tk.Scrollbar(frame, orient="horizontal", command=self.__tree.xview)
        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.__tree.yview)
        self.__tree.config(xscrollcommand=scroll_x.set)
        self.__tree.config(yscrollcommand=scroll_y.set)
        for i in head:
            self.__tree.heading(i, text=i)
        self.__fill_tree(self.__df)
        self.__tree.grid(column=0, row=0, sticky="nsew")
        scroll_x.grid(column=0, row=1, sticky="ew")
        scroll_y.grid(column=1, row=0, sticky="ns")
        return frame

    def __create_figure_frame(self):
        frame = tk.Frame(self)
        self.__fig1 = Figure(figsize=(3, 2))
        self.__fig2 = Figure(figsize=(3, 2))
        self.__fig3 = Figure(figsize=(3, 2))
        self.__fig4 = Figure(figsize=(3, 2))
        self.__ax1 = self.__fig1.add_subplot()
        self.__ax2 = self.__fig2.add_subplot()
        self.__ax3 = self.__fig3.add_subplot()
        self.__ax4 = self.__fig4.add_subplot()
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        frame.rowconfigure(0, weight=1)
        self.__canvas1 = FigureCanvasTkAgg(self.__fig1, master=frame)
        self.__canvas1.get_tk_widget().grid(column=0, row=0)
        self.__canvas2 = FigureCanvasTkAgg(self.__fig2, master=frame)
        self.__canvas2.get_tk_widget().grid(column=1, row=0)
        self.__canvas3 = FigureCanvasTkAgg(self.__fig3, master=frame)
        self.__canvas3.get_tk_widget().grid(column=2, row=0)
        self.__canvas4 = FigureCanvasTkAgg(self.__fig4, master=frame)
        self.__canvas4.get_tk_widget().grid(column=3, row=0)
        return frame

    def __config_search(self, text: str):
        self.__search_frame["text"] = f"Search board game by {text}"
        self.__current_mod["Search"] = text

    def __fill_tree(self, df: pd.DataFrame):

        def fill(index=0):
            if len(df.index) - index >= 543:
                for i in range(index, index+543):
                    temp = [df[col][i] for col in list(df.columns)]
                    self.__tree.insert("", "end", values=temp)
                    self.__bar["value"] = (i/len(df.index))*100
                self.__bar_frame["text"] = f"Filling data: {sum(1 for _ in self.__tree.get_children())} filled"
                self.after(1, lambda: fill(index+543))
            else:
                for i in range(index, len(df.index)):
                    temp = [df[col][i] for col in list(df.columns)]
                    self.__tree.insert("", "end", values=temp)
                    self.__bar["value"] = (i/len(df.index))*100
                self.__bar_frame["text"] = f"Done: {sum(1 for _ in self.__tree.get_children())} filled"
                self.after(1, self.__enable_search_frame)
        self.__disable_search_frame()
        self.__clear_tree()
        fill()

    def __search_tree(self, df: pd.DataFrame, search):
        text = self.__search_text.get()
        if not text:
            return df
        word = text.split(" ")
        mask = eval(" & ".join([f"(df['{search}'].astype(str).str.contains('{i}'))" for i in word]))
        temp_df = df[mask]
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df

    def __sort_tree(self, df: pd.DataFrame):
        if not self.__current_mod["Sort"]:
            return df
        temp_df = df.sort_values(by=self.__current_mod["Sort"], axis=0)
        temp_df.reset_index(drop=True, inplace=True)
        return temp_df

    def __update_tree(self, text: str, mode: str, bool_var: bool=None):
        if bool_var is not None:
            if bool_var:
                self.__current_mod[mode].append(text)
            else:
                self.__current_mod[mode].remove(text)
        if (not self.__current_mod["Sort"]) and (not self.__search_text.get()):
            if self.__search_trace == self.__search_text.get():
                return
            self.__fill_tree(self.__df)
        else:
            temp_search = self.__search_tree(self.__df, self.__current_mod["Search"])
            temp_sort = self.__sort_tree(temp_search)
            if mode == "Search":
                if self.__search_trace == self.__search_text.get():
                    return
            self.__search_trace = self.__search_text.get()
            self.__fill_tree(temp_sort)

    def __disable_search_frame(self):
        self.__search_box.unbind("<Return>")
        self.__search_box.config(state="disabled")
        self.__sort_box.config(state="disabled")
        self.__search_button.config(state="disabled")

    def __enable_search_frame(self):
        self.__bar["value"] = 100
        self.__search_box.bind("<Return>", lambda x: self.__update_tree("", "Search"))
        self.__search_box.config(state="normal")
        self.__sort_box.config(state="normal")
        self.__search_button.config(state="normal")

    def __clear_tree(self):
        for i in self.__tree.get_children():
            self.__tree.delete(i)

    def run(self):
        self.mainloop()
