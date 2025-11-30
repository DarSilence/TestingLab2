import tkinter as tk
from tkinter import ttk
from for_bd import *


class MainFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=650, height=500)
        self.parent = parent
        self.create_widgets()
        self.put_widgets()

    def create_widgets(self):
        self.l_to_balance = ttk.Label(self, text="Ваш баланс:")
        self.l_balance = ttk.Label(self, text=get_fund(self.parent.u_name))
        self.l_bougths = ttk.Label(self, text="Ваши покупки:")
        self.b_buy = ttk.Button(self, text="Совершить покупку", command=self.parent.to_bougth)
        self.b_return = ttk.Button(self, text="Отменить покупку", command=self.parent.to_return)
        self.l_sort = ttk.Label(self, text="Вывести по дате/категории")
        self.com_cat = ttk.Combobox(self, values=(["Все"] + get_cats(self.parent.u_name)), width=30)
        self.com_date = ttk.Combobox(self, values=(["Все"] + get_dates(self.parent.u_name)), width=30)
        self.get_values()
        self.com_cat.bind('<<ComboboxSelected>>', self.insert)
        self.com_date.bind('<<ComboboxSelected>>', self.insert)
        self.com_cat.current(0)
        self.com_date.current(0)

        self.heads = ["Товар", "Стоимость", "Категория", "Дата покупки"]
        self.heads_reverse = [False, False, False, False]
        self.t_boughts = ttk.Treeview(self, show="headings")
        self.t_boughts['columns'] = self.heads

        self.scr_boughts = ttk.Scrollbar(self, command=self.t_boughts.yview)
        self.t_boughts.configure(yscrollcommand=self.scr_boughts.set)

        self.re_table()

    def get_values(self):
        self.com_cat.config(values=(["Все"] + sorted(get_cats(self.parent.u_name))))
        self.com_date.config(values=(["Все"] + sorted(get_dates(self.parent.u_name))))
        self.l_balance.config(text=get_fund(self.parent.u_name))

    def clear_widgets(self):
        self.com_cat.current(0)
        self.com_date.current(0)

    def insert(self, *args):
        category = self.com_cat.get()
        date = self.com_date.get()

        self.re_table(category, date)

    def re_table(self, cat="Все", date="Все"):
        for i in self.t_boughts.get_children():
            self.t_boughts.delete(i)

        if self.com_cat.get():
            cat = self.com_cat.get()
        if self.com_date.get():
            date = self.com_date.get()

        self.t_boughts.heading(self.heads[0], text=self.heads[0], anchor="center", command=lambda: self.ch_rows(0))
        self.t_boughts.column(self.heads[0], anchor="center", width=610//4)
        self.t_boughts.heading(self.heads[1], text=self.heads[1], anchor="center", command=lambda: self.ch_rows(1))
        self.t_boughts.column(self.heads[1], anchor="center", width=610//4)
        self.t_boughts.heading(self.heads[2], text=self.heads[2], anchor="center", command=lambda: self.ch_rows(2))
        self.t_boughts.column(self.heads[2], anchor="center", width=610//4)
        self.t_boughts.heading(self.heads[3], text=self.heads[3], anchor="center", command=lambda: self.ch_rows(3))
        self.t_boughts.column(self.heads[3], anchor="center", width=610//4)

        for i in get_boughts(self.parent.u_name, cat, date):
            self.t_boughts.insert('', tk.END, values=i)

    def ch_rows(self, column):
        try:
            array = [(int(self.t_boughts.set(k, column)), k) for k in self.t_boughts.get_children("")]
        except:
            array = [(self.t_boughts.set(k, column), k) for k in self.t_boughts.get_children("")]

        array.sort(reverse=self.heads_reverse[column])

        for i in range(4):
            if i != column:
                self.heads_reverse[i] = False
            else:
                self.heads_reverse[column] ^= True

        for index, (_, k) in enumerate(array):
            self.t_boughts.move(k, "", index)


    def put_widgets(self):
        self.l_to_balance.grid(row=0, column=0, padx=10, pady=5)
        self.l_balance.grid(row=0, column=1, padx=10, pady=5)
        self.l_bougths.grid(row=2, column=0, padx=10, pady=5)
        self.b_buy.grid(row=2, column=1, padx=10, pady=5)
        self.b_return.grid(row=2, column=2, padx=10, pady=5)
        self.l_sort.grid(row=1, column=0, padx=10, pady=5)
        self.com_cat.grid(row=1, column=1, padx=10, pady=5)
        self.com_date.grid(row=1, column=2, padx=10, pady=5)
        self.t_boughts.grid(row=3, column=0, padx=10, pady=5, columnspan=3, sticky="nsew")
        self.scr_boughts.grid(row=3, column=3)