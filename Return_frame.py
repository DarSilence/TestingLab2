import tkinter as tk
from tkinter import ttk
from for_bd import *

class ReturnFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=450, height=200)
        self.parent = parent
        self.create_widgets()
        self.put_widgets()

    def create_widgets(self):
        self.l_bought = ttk.Label(self, text="Выберите покупку для возрата денежных средств:")
        self.com_boughts = ttk.Combobox(self, width=40)
        self.get_values()
        self.b_delete = ttk.Button(self, text="Удалить запись", command=self.delete)
        self.b_back = ttk.Button(self, text="Назад", command=self.parent.from_return)
        self.l_error = ttk.Label(self, text="Выберите покупку", foreground="red", font="16")

    def put_widgets(self):
        self.l_bought.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        self.com_boughts.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.b_delete.grid(row=3, column=1, padx=10, pady=5)
        self.b_back.grid(row=4, column=1, padx=10, pady=5)


    def clear_widgets(self):
        self.com_boughts.set("")
        self.l_error.grid_forget()

    def get_values(self):
        self.com_boughts.config(values=[str(i + 1) + ". " + " ".join([str(k) for k in j]) for i, j in enumerate(get_boughts(self.parent.u_name))])

    def delete(self):
        if self.com_boughts.get():
            self.l_error.grid_forget()
            all_things = self.com_boughts.get().split()
            sup = 2
            for i in range(1, len(all_things)):
                if all_things[i].isnumeric():
                    sup = i
                    break
            num, good_name, good_price, cat_name, date = all_things[0], " ".join(all_things[1:sup]), all_things[sup], " ".join(all_things[sup+1:-1]), all_things[-1]
            get_pay_back(get_bought_id(good_name, good_price, cat_name, date, self.parent.u_name), self.parent.u_name)
            self.get_values()
            self.clear_widgets()
        else:
            self.l_error.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
