import tkinter as tk
from tkinter import ttk
from for_bd import *

class LogInFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=450, height=200)
        self.parent = parent
        self.create_widgets()
        self.put_widgets()


    def create_widgets(self):
        self.l_name = ttk.Label(self, text="Введите имя пользователя:")
        self.l_pass = ttk.Label(self, text="Введите пароль:")
        self.l_error = ttk.Label(self, text="Заполните все поля", foreground="red")

        self.vname = (self.register(self.validate_name),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_name = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vname)
        self.e_pass = ttk.Entry(self, justify=tk.RIGHT)


        self.btn_register = ttk.Button(self, text="Зарегистрироваться", command=self.parent.to_registr)

        self.btn_log_in = ttk.Button(self, text="Войти", command=self.check)
        self.btn_exit = ttk.Button(self, text="Выйти из приложения", command=self.parent.close)


    def put_widgets(self):
        self.l_name.grid(row=0, column=0, padx=10, pady=10)
        self.e_name.grid(row=0, column=1, padx=10, pady=10)
        self.l_pass.grid(row=1, column=0, padx=10, pady=10)
        self.e_pass.grid(row=1, column=1, padx=10, pady=10)
        self.btn_register.grid(row=3, column=1, sticky='sw', padx=10, pady=5)
        self.btn_log_in.grid(row=4, column=1, sticky='sw', padx=10, pady=5)
        self.btn_exit.grid(row=5, column=1, sticky='sw', padx=10, pady=5)

    def clear_widgets(self):
        self.e_name.delete(0, tk.END)
        self.e_pass.delete(0, tk.END)
        self.l_error.grid_forget()

    def check(self):
        if not self.e_name.get() or not self.e_pass.get():
            self.l_error.config(text="Заполните все поля")
            self.l_error.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            return
        if not get_user(self.e_name.get()):
            self.l_error.config(text="Такого пользователя не существует")
            self.l_error.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            return

        if not check_user_pass(self.e_name.get(), self.e_pass.get()):
            self.l_error.config(text="Такого пользователя не существует")
            self.l_error.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            return

        self.l_error.grid_forget()
        self.parent.u_name = self.e_name.get()
        self.parent.to_main()

    def validate_name(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_):
        self.e_name.selection_clear()
        index = int(index)
        # print(action, index, text, prior_value)
        if int(action) == 1 and index == 0 and not text.isalpha():
            self.e_name.icursor(index)
            return False
        if int(action) == 1 or int(action) == 1 and index == 0 and text.isalpha():
            if not text.isalpha():
                self.e_name.delete(0, tk.END)
                self.e_name.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                self.e_name.delete(0, tk.END)
                self.e_name.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_name.icursor(index)
            return True
        elif int(action) == 0:
            self.e_name.delete(0, tk.END)
            self.e_name.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_name.icursor(index)
            return True
        return False