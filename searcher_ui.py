import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
from searcher_controller import SearcherController
matplotlib.use("TkAgg")


class SearcherUI(tk.Tk):
    def __init__(self, controller: SearcherController, graph1: list=None, graph2: str=None,
                 graph3: list=None, graph4: list=None):
        super().__init__()
        if not isinstance(controller, SearcherController):
            raise TypeError
        self._controller = controller

        self.title("Board Game Suggester")
        self._init_component()

    def _init_component(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=11)
        self._current_mod = {"Sort": [], "Filter": [], "Search": "Name"}
        self._search_trace = ""
        self._create_menu()
        self._bar_frame = self._create_bar_frame()
        self._search_frame = self._create_search_frame()
        tree_frame = self._create_tree_frame()
        fig_frame = self._create_figure_frame()
        self._search_frame.grid(column=0, row=0, sticky="ew", padx=200)
        self._bar_frame.grid(column=0, row=1, sticky="ew", padx=200, pady=5)
        tree_frame.grid(column=0, row=2, sticky="nsew", padx=50)
        fig_frame.grid(column=0, row=3, sticky="nsew")

    def _create_menu(self):
        menubar = tk.Menu(self)
        search_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Search by", menu=search_menu)
        for i in self._controller.original_data.columns.values:
            search_menu.add_command(label=i, command=lambda x=i: self._config_search(x))
        menubar.add_cascade(label="Exit", command=self.destroy)
        self.config(menu=menubar)

    def _create_search_frame(self):
        frame = tk.LabelFrame(self, text="Search board game by Name")
        self._search_text = tk.StringVar()
        self._search_box = tk.Entry(frame, textvariable=self._search_text)
        self._search_box.bind("<Return>", lambda x: self._update_display("", "Search"))
        self._sort_box = ttk.Menubutton(frame, text="Sort by")
        sort_menu = tk.Menu(self._sort_box, tearoff=False)
        bool_var = {}
        for i in self._controller.original_data.columns.values:
            temp_bool = tk.BooleanVar()
            bool_var[i] = temp_bool
            sort_menu.add_checkbutton(label=i, variable=temp_bool, command=lambda x=i, y=temp_bool: self._update_display(x, "Sort", y.get()))
        sort_menu.add_command(label="Clear", command=lambda: self._clear_sort(bool_var))
        self._sort_box.config(menu=sort_menu)
        self._search_button = tk.Button(frame, text="Search", command=lambda: self._update_display("", "Search"))
        frame.columnconfigure(0, weight=18)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        self._search_box.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)
        self._sort_box.grid(column=1, row=0, sticky="nsew", padx=5, pady=5)
        self._search_button.grid(column=2, row=0, sticky="nsew", padx=5, pady=5)
        self._disable_search_frame()
        return frame

    def _create_bar_frame(self):
        frame = tk.LabelFrame(self, text="")
        frame.columnconfigure(0, weight=1)
        self._bar = ttk.Progressbar(frame, length=500, mode="determinate")
        self._bar.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
        return frame

    def _create_tree_frame(self):
        frame = tk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        head = list(self._controller.original_data.columns)
        self._tree = ttk.Treeview(frame, columns=head, show="headings", selectmode="none")
        scroll_x = tk.Scrollbar(frame, orient="horizontal", command=self._tree.xview)
        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self._tree.yview)
        self._tree.config(xscrollcommand=scroll_x.set)
        self._tree.config(yscrollcommand=scroll_y.set)
        for i in head:
            self._tree.heading(i, text=i)
        self._fill_tree(self._controller.original_data)
        self._tree.grid(column=0, row=0, sticky="nsew")
        scroll_x.grid(column=0, row=1, sticky="ew")
        scroll_y.grid(column=1, row=0, sticky="ns")
        return frame

    def _create_figure_frame(self):
        frame = tk.Frame(self)
        fig1 = Figure(figsize=(5, 4.5), dpi=60)
        fig2 = Figure(figsize=(5, 4.5), dpi=60)
        fig3 = Figure(figsize=(5, 4.5), dpi=60)
        fig4 = Figure(figsize=(5, 4.5), dpi=60)
        self._ax1 = fig1.add_subplot()
        self._ax2 = fig2.add_subplot()
        self._ax3 = fig3.add_subplot()
        self._ax4 = fig4.add_subplot()
        frame.rowconfigure(0, weight=1)
        self._fig_frame1 = tk.LabelFrame(frame, text="")
        self._fig_frame2 = tk.LabelFrame(frame, text="")
        self._fig_frame3 = tk.LabelFrame(frame, text="")
        self._fig_frame4 = tk.LabelFrame(frame, text="")
        self._canvas1 = FigureCanvasTkAgg(fig1, master=self._fig_frame1)
        self._canvas2 = FigureCanvasTkAgg(fig2, master=self._fig_frame2)
        self._canvas3 = FigureCanvasTkAgg(fig3, master=self._fig_frame3)
        self._canvas4 = FigureCanvasTkAgg(fig4, master=self._fig_frame4)
        for i in range(4):
            frame.columnconfigure(i, weight=1)
            eval(f"self._canvas{i+1}.get_tk_widget().grid(column=0, row=0, padx=10, pady=10)")
            eval(f"self._fig_frame{i+1}.columnconfigure(0, weight=1)")
            eval(f"self._fig_frame{i+1}.rowconfigure(0, weight=1)")
            eval(f"self._fig_frame{i+1}.grid(column={i}, row=0)")
        frame.rowconfigure(0, weight=1)
        self._plot_graph(1, self._controller.original_data)
        self._plot_graph(2, self._controller.original_data)
        return frame

    def _config_search(self, text: str):
        self._search_frame["text"] = f"Search board game by {text}"
        self._current_mod["Search"] = text

    def _fill_tree(self, df: pd.DataFrame):
        def fill(index=0):
            if len(df.index) - index >= 543:
                for i in range(index, index+543):
                    temp = [df[col][i] for col in list(df.columns)]
                    self._tree.insert("", "end", values=temp)
                    self._bar["value"] = (i/len(df.index))*100
                self._bar_frame["text"] = f"Filling data: {sum(1 for _ in self._tree.get_children())} filled"
                self.after(1, lambda: fill(index+543))
            else:
                for i in range(index, len(df.index)):
                    temp = [df[col][i] for col in list(df.columns)]
                    self._tree.insert("", "end", values=temp)
                    self._bar["value"] = (i/len(df.index))*100
                self._bar_frame["text"] = f"Done: {sum(1 for _ in self._tree.get_children())} filled"
                self.after(1, self._enable_search_frame)
        self._disable_search_frame()
        self._clear_tree()
        fill()

    def _update_tree(self, df: pd.DataFrame):
        if (not self._current_mod["Sort"]) and (not self._search_text.get()):
            self._fill_tree(self._controller.original_data)
        else:
            self._fill_tree(df)

    def _plot_graph(self, which: int, data: pd.DataFrame):
        att, text = self._controller.get_attribute(which, data)
        eval(f"self._ax{which}.clear()")
        if which == 1:
            sns.scatterplot(data, x=att[0], y=att[1], ax=self._ax1)
        elif which == 2:
            sns.histplot(data, x=att[0], ax=self._ax2)
        eval(f"self._fig_frame{which}.config(text=text)")
        eval(f"self._canvas{which}.draw()")

    def _update_display(self, text: str, mode: str, bool_var: bool=None):
        if bool_var is not None:
            if bool_var:
                self._current_mod[mode].append(text)
            else:
                self._current_mod[mode].remove(text)
        temp_df = self._controller.modified_data(self._search_text.get(),
                                                  self._current_mod["Search"],
                                                  self._current_mod["Sort"])
        self._update_tree(temp_df)
        self._plot_graph(2, temp_df)

    def _disable_search_frame(self):
        self._search_box.unbind("<Return>")
        self._search_box.config(state="disabled")
        self._sort_box.config(state="disabled")
        self._search_button.config(state="disabled")

    def _enable_search_frame(self):
        self._bar["value"] = 100
        self._search_box.bind("<Return>", lambda x: self._update_display("", "Search"))
        self._search_box.config(state="normal")
        self._sort_box.config(state="normal")
        self._search_button.config(state="normal")

    def _clear_tree(self):
        for i in self._tree.get_children():
            self._tree.delete(i)

    def _clear_sort(self, bool_var_dict: dict):
        for i in bool_var_dict:
            bool_var_dict[i].set(False)
        self._current_mod["Sort"].clear()
        self._update_display("", "Clear Sort")

    def run(self):
        self.mainloop()
