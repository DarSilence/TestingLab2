import tkinter as tk
from tkinter import ttk
from for_bd import *

class BoughtFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=450, height=200)
        self.parent = parent
        self.create_widgets()
        self.put_widgets()

    def create_widgets(self):
        self.l_to_balance = ttk.Label(self, text="Ваш баланс:")
        self.l_balance = ttk.Label(self, text=get_fund(self.parent.u_name))
        self.b_to_main = ttk.Button(self, text="Назад", command=self.parent.from_bought)
        self.b_buy = ttk.Button(self, text="Купить товар", command=self.buy)

        self.l_category = ttk.Label(self, text="Категория товара")
        self.l_good_name = ttk.Label(self, text="Наименование товара")
        self.l_good_price = ttk.Label(self, text="Стоимость товара, руб.")
        self.l_amount_goods = ttk.Label(self, text="Количество товаров (штука; кг; уп)")
        self.l_error = ttk.Label(self, text="Все поля должны быть заполнены", foreground="red", font="16")

        self.l_goods = ttk.Label(self, text="Можно выбрать из\nимеющихся товаров")

        self.com_goods = ttk.Combobox(self, values=tuple(get_goods()), width=30)
        self.com_goods.bind('<<ComboboxSelected>>', self.insert)

        self.vcat = (self.register(self.validate_cat),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_category = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vcat)

        self.vname = (self.register(self.validate_name),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_good_name = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vname)

        self.vprice = (self.register(self.validate_price),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_good_price = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vprice)

        self.vamount = (self.register(self.validate_amount),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_amount_goods = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vamount)

    def get_values(self):
        self.l_balance.config(text=get_fund(self.parent.u_name))

    def insert(self, *args):
        desription = get_good_desr(self.com_goods.get()[:self.com_goods.get().index(".")])

        self.e_category.delete(0, tk.END)
        self.e_category.insert(0, desription[0])
        self.e_good_name.delete(0, tk.END)
        self.e_good_name.insert(0, desription[1])
        self.e_good_price.delete(0, tk.END)
        self.e_good_price.insert(0, desription[2])
        self.e_amount_goods.delete(0, tk.END)
        self.e_amount_goods.insert(0, desription[3])

    def put_widgets(self):
        self.l_to_balance.grid(row=0, column=0, padx=10, pady=5)
        self.l_balance.grid(row=0, column=1, padx=10, pady=5)
        self.l_category.grid(row=1, column=0, padx=10, pady=5)
        self.e_category.grid(row=1, column=1, padx=10, pady=5)
        self.l_good_name.grid(row=2, column=0, padx=10, pady=5)
        self.e_good_name.grid(row=2, column=1, padx=10, pady=5)
        self.l_good_price.grid(row=3, column=0, padx=10, pady=5)
        self.e_good_price.grid(row=3, column=1, padx=10, pady=5)
        self.l_amount_goods.grid(row=4, column=0, padx=10, pady=5)
        self.e_amount_goods.grid(row=4, column=1, padx=10, pady=5)

        self.l_goods.grid(row=5, column=0, padx=10, pady=5)
        self.com_goods.grid(row=5, column=1, padx=10, pady=5)

        self.b_buy.grid(row=7, column=1, padx=10, pady=5)
        self.b_to_main.grid(row=8, column=1, padx=10, pady=5)

    def clear_widgets(self):
        self.e_category.delete(0, tk.END)
        self.e_good_name.delete(0, tk.END)
        self.e_good_price.delete(0, tk.END)
        self.e_amount_goods.delete(0, tk.END)
        self.com_goods.set("")
        self.l_error.grid_forget()

    def buy(self):
        if self.check():
            print(self.e_good_price.get())
            if add_good(self.e_category.get(),
                     self.e_good_name.get(),
                     int(self.e_good_price.get()),
                     int(self.e_amount_goods.get()),
                     self.parent.u_name):
                self.parent.from_bought()
            else:
                self.l_error.config(text="Не хватает средств")
                self.l_error.grid(row=6, column=0, columnspan=2, padx=10, pady=5)


    def check(self):
        if (not self.e_category.get() or
                not self.e_good_name.get() or
                not self.e_good_price.get() or
                not self.e_amount_goods.get()):
            self.l_error.config(text="Все поля должны быть заполнены")
            self.l_error.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
            return False
        else:
            self.l_error.grid_forget()
            return True

    def validate_cat(self, action, index, value_if_allowed,
                      prior_value, text, validation_type, trigger_type, widget_):
        self.e_category.selection_clear()
        index = int(index)
        # print(action, index, text, prior_value)
        if int(action) == 1 and index == 0 and (not text.isalpha() and len(text) == 1 or (text[0] == " " and not text.isalpha())):
            self.e_category.icursor(index)
            return False
        if int(action) == 1 or int(action) == 1 and index == 0 and (text.isalpha() or text[0] != " ") or text == " ":
            if (not text.isalpha() and len(text) == 1 or (text[0] == " " and not text.isalpha())) and not text == " ":
                self.e_category.delete(0, tk.END)
                self.e_category.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                self.e_category.delete(0, tk.END)
                self.e_category.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_category.icursor(index)
            return True
        elif int(action) == 0:
            self.e_category.delete(0, tk.END)
            self.e_category.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_category.icursor(index)
            return True
        return False


    def validate_name(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_):
        self.e_good_name.selection_clear()
        index = int(index)
        # print(action, index, text, prior_value)
        if int(action) == 1 and index == 0 and (not text.isalpha() and len(text) == 1 or (text[0] == " " and not text.isalpha())):
            self.e_good_name.icursor(index)
            return False
        if int(action) == 1 or int(action) == 1 and index == 0 and (text.isalpha() or text == " "):
            if (not text.isalpha() and len(text) == 1 or (text[0] == " " and not text.isalpha())) and not text == " ":
                self.e_good_name.delete(0, tk.END)
                self.e_good_name.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                self.e_good_name.delete(0, tk.END)
                self.e_good_name.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_good_name.icursor(index)
            return True
        elif int(action) == 0:
            self.e_good_name.delete(0, tk.END)
            self.e_good_name.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_good_name.icursor(index)
            return True
        return False

    def validate_price(self, action, index, value_if_allowed,
                      prior_value, text, validation_type, trigger_type, widget_):
        self.e_good_price.selection_clear()
        index = int(index)
        # print(action, index, text, prior_value)
        if int(action) == 1 and index == 0 and not text.isnumeric():
            self.e_good_price.icursor(index)
            return False
        if int(action) == 1 or int(action) == 1 and index == 0 and text.isalpha():
            if not text.isnumeric():
                self.e_good_price.delete(0, tk.END)
                self.e_good_price.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                self.e_good_price.delete(0, tk.END)
                self.e_good_price.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_good_price.icursor(index)
            return True
        elif int(action) == 0:
            self.e_good_price.delete(0, tk.END)
            self.e_good_price.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_good_price.icursor(index)
            return True
        return False

    def validate_amount(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_):
        self.e_amount_goods.selection_clear()
        index = int(index)
        # print(action, index, text, prior_value)
        if int(action) == 1 and index == 0 and not text.isnumeric():
            self.e_amount_goods.icursor(index)
            return False
        if int(action) == 1 or int(action) == 1 and index == 0 and text.isalpha():
            if not text.isnumeric():
                self.e_amount_goods.delete(0, tk.END)
                self.e_amount_goods.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                self.e_amount_goods.delete(0, tk.END)
                self.e_amount_goods.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_amount_goods.icursor(index)
            return True
        elif int(action) == 0:
            self.e_amount_goods.delete(0, tk.END)
            self.e_amount_goods.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_amount_goods.icursor(index)
            return True
        return False