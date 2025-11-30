import tkinter as tk
from tkinter import ttk
from for_bd import *


class RegisterFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=700, height=600)
        self.parent = parent
        self.create_widgets()
        self.put_widgets()


    def create_widgets(self):
        self.conditions = ["заглавные буквы", "строчные буквы", "цифры", "специальные символы", "Пароль должен быть не меньше 6 символов"]
        self.cond = [False, False, False, False, False]

        self.l_desr = ttk.Label(self)
        self.l_name = ttk.Label(self, text="Введите имя пользователя:")
        self.l_pass = ttk.Label(self, text="Введите пароль:")
        self.l_pass_conf = ttk.Label(self, text="Повторите пароль:")
        self.l_fund_cur = ttk.Label(self, text="Введите денежные средства,\nимеющиеся в наличии:")
        self.l_date = ttk.Label(self, text="Выберите день месяца\nдля поступления денежных средств:")
        self.l_fund_pay = ttk.Label(self, text="Введите сумму денежных средств,\nкоторая будет зачисляться ежемесячно:")
        self.l_error = ttk.Label(self, text="Пароли не совпадают", foreground="red", font="16")
        self.l_error_exist = ttk.Label(self, text="Пользователь с таким именем уже существует", foreground="red", font="16")
        self.l_error_date = ttk.Label(self, text="Введите дату\nзачисления средств", foreground="red", font="16")

        self.vname = (self.register(self.validate_name),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_name = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vname, width=30)
        self.vpass = (self.register(self.validate_pass),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_pass = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vpass, width=30)
        self.vpass_conf = (self.register(self.validate_pass_conf),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_pass_conf = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vpass_conf, width=30)

        self.vfund_cur = (self.register(self.validate_fund_cur),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_fund_cur = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vfund_cur, width=30)

        self.com_date = ttk.Combobox(self, values=tuple(array_of_days.keys()), width=20)

        self.vfund_pay = (self.register(self.validate_fund_pay),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.e_fund_pay = ttk.Entry(self, justify=tk.RIGHT, validate='key', validatecommand=self.vfund_pay, width=30)


        self.btn_log_in = ttk.Button(self, text="Вернуться на авторизацию", command=self.parent.to_log_in)

        self.btn_reg = ttk.Button(self, text="Зарегистрироваться", command=self.check)
        self.btn_exit = ttk.Button(self, text="Выйти из приложения", command=self.parent.close)


    def put_widgets(self):
        self.l_name.grid(row=0, column=0, padx=10, pady=10)
        self.e_name.grid(row=0, column=1, padx=10, pady=10)
        self.put_desc([0, 1, 2, 3, 4])
        self.l_pass.grid(row=2, column=0, padx=10, pady=10)
        self.e_pass.grid(row=2, column=1, padx=10, pady=10)
        self.l_pass_conf.grid(row=3, column=0, padx=10, pady=10)
        self.e_pass_conf.grid(row=3, column=1, padx=10, pady=10)
        self.l_fund_cur.grid(row=4, column=0, padx=10, pady=10)
        self.e_fund_cur.grid(row=4, column=1, padx=10, pady=10)
        self.l_date.grid(row=5, column=0, padx=10, pady=10)
        self.com_date.grid(row=5, column=1, padx=10, pady=10)
        self.l_fund_pay.grid(row=6, column=0, padx=10, pady=10)
        self.e_fund_pay.grid(row=6, column=1, padx=10, pady=10)
        self.btn_log_in.grid(row=8, column=1, sticky='sw', padx=10, pady=5)
        self.btn_reg.grid(row=9, column=1, sticky='sw', padx=10, pady=5)
        self.btn_exit.grid(row=10, column=1, sticky='sw', padx=10, pady=5)


    def check_pass(self):
        self.cond = [False, False, False, False, False]
        password = self.e_pass.get()
        length = len(password)
        if length >= 6:
            self.cond[-1] = True

        for i in password:
            if i.isalpha():
                if i.isupper():
                    self.cond[0] = True
                elif i.islower():
                    self.cond[1] = True
            elif i.isnumeric():
                self.cond[2] = True
            elif not i.isalpha():
                self.cond[3] = True

        needs = []
        len_needs = 0
        for i in range(len(self.cond)):
            if not self.cond[i]:
                needs.append(i)
                len_needs += 1

        if len_needs:
            self.put_desc(needs)
            return False
        else:
            self.l_desr.grid_forget()
            return True

    def put_desc(self, needs):
        string = ""
        ans = ', '.join([self.conditions[i] for i in needs if i < 4])

        if needs[0] < 4:
            string = f"В пароле должны быть: {ans}"
            if needs[-1] == 4:
                string += "\n" + self.conditions[4]
        elif needs[-1] == 4:
            string = self.conditions[4]

        self.l_desr.config(text=string)
        self.l_desr.grid(row=1, column=0, columnspan=2, padx=15, pady=10)
    def check(self):
        ready = True

        if not self.e_name.get() or self.e_name.get() == "нет имени":
            self.e_name.delete(0, tk.END)
            self.e_name.insert(0, "нет имени")
            self.e_name.config(background="red", foreground="red")
            ready = False
        else:
            self.e_name.config(background="white", foreground="black")

        if not self.e_pass.get() or self.e_pass.get() == "нет пароля":
            self.check_pass()
            self.e_pass.delete(0, tk.END)
            self.e_pass.insert(0, "нет пароля")
            self.e_pass.config(background="red", foreground="red")
            ready = False
        elif self.e_pass.get() != self.e_pass_conf.get():
            self.check_pass()
            self.l_error_exist.grid_forget()
            self.l_error.grid(row=7, column=1, padx=10, pady=5)
            self.e_pass.config(background="white", foreground="black")
            self.e_pass_conf.config(background="red", foreground="red")
            ready = False
        else:
            self.check_pass()
            self.l_error.grid_forget()
            self.e_pass.config(background="white", foreground="black")
            self.e_pass_conf.config(background="white", foreground="black")
        if not self.e_fund_cur.get() or self.e_fund_cur.get() == "поле должно быть заполнено":
            self.e_fund_cur.delete(0, tk.END)
            self.e_fund_cur.insert(0, "поле должно быть заполнено")
            self.e_fund_cur.config(background="red", foreground="red")
            ready = False
        else:
            self.e_fund_cur.config(background="white", foreground="black")

        if not self.com_date.get() in array_of_days:
            self.l_error_exist.grid_forget()
            self.l_error_date.grid(row=7, column=0, padx=10, pady=5)
            ready = False
        else:
            self.l_error_date.grid_forget()

        if not self.e_fund_pay.get() or self.e_fund_pay.get() == "поле должно быть заполнено":
            self.e_fund_pay.delete(0, tk.END)
            self.e_fund_pay.insert(0, "поле должно быть заполнено")
            self.e_fund_pay.config(background="red", foreground="red")
            ready = False
        else:
            self.e_fund_pay.config(background="white", foreground="black")
        if ready:
            ready = save_user(self.e_name.get(),
                      self.e_pass.get(),
                      int(self.e_fund_cur.get()),
                      array_of_days[self.com_date.get()],
                      int(self.e_fund_pay.get()))
            if ready:
                self.l_error_exist.grid_forget()
                self.parent.u_name = self.e_name.get()
                self.parent.to_main()
            else:
                self.l_error_exist.grid(row=7, column=0, columnspan=2, padx=10, pady=5)


    def clear_widgets(self):
        self.e_name.delete(0, tk.END)
        self.e_pass.delete(0, tk.END)
        self.e_pass_conf.delete(0, tk.END)
        self.e_fund_cur.delete(0, tk.END)
        self.e_fund_pay.delete(0, tk.END)
        self.com_date.set("")
        self.l_error.grid_forget()
        self.l_error_exist.grid_forget()
        self.l_error_date.grid_forget()

#p
    def validate_name(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_):
        self.e_name.selection_clear()
        index = int(index)
        if text == "нет имени" and int(action) == 1 and prior_value == "":
            if "нет имени" in prior_value:
                prior_value = prior_value.replace("нет имени", "")
            self.e_name.delete(0, tk.END)
            self.e_name.insert(0, prior_value[0:index] + text + prior_value[index:])
            index += len(text)
            self.e_name.icursor(index)
        elif int(action) == 1 and index == 0 and not text.isalpha():
            self.e_name.icursor(index)
            return False
        elif int(action) == 1:
            if not text.isalpha():
                self.e_name.delete(0, tk.END)
                self.e_name.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                if "нет имени" in prior_value:
                    prior_value = prior_value.replace("нет имени", "")
                self.e_name.config(background="white", foreground="black")
                self.e_name.delete(0, tk.END)
                self.e_name.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_name.icursor(index)
            return True
        elif int(action) == 0:
            if text in "нет имени" and prior_value in "нет имени":
                index = 0
                text = "нет имени"
            self.e_name.delete(0, tk.END)
            self.e_name.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_name.icursor(index)
            return True
        return False

#p
    def validate_fund_pay(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_):
        self.e_fund_pay.selection_clear()
        index = int(index)
        if text == "поле должно быть заполнено" and int(action) == 1 and prior_value == "":
            if "поле должно быть заполнено" in prior_value:
                prior_value = prior_value.replace("поле должно быть заполнено", "")
            self.e_fund_pay.delete(0, tk.END)
            self.e_fund_pay.insert(0, prior_value[0:index] + text + prior_value[index:])
            index += len(text)
            self.e_fund_pay.icursor(index)
        elif int(action) == 1 and index == 0 and not text.isnumeric():
            self.e_fund_pay.icursor(index)
            return False
        elif int(action) == 1:
            if not text.isnumeric():
                self.e_fund_pay.delete(0, tk.END)
                self.e_fund_pay.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                if "поле должно быть заполнено" in prior_value:
                    prior_value = prior_value.replace("поле должно быть заполнено", "")
                self.e_fund_pay.config(background="white", foreground="black")
                if len(prior_value) >= 10:
                    self.e_fund_pay.icursor(index)
                    return False
                else:
                    self.e_fund_pay.delete(0, tk.END)
                    self.e_fund_pay.insert(0, prior_value[0:index] + text + prior_value[index:])
                    index += 1
            self.e_fund_pay.icursor(index)
            return True
        elif int(action) == 0:
            if text in "поле должно быть заполнено" and prior_value in "поле должно быть заполнено":
                index = 0
                text = "поле должно быть заполнено"
            self.e_fund_pay.delete(0, tk.END)
            self.e_fund_pay.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_fund_pay.icursor(index)
            return True
        return False

    def validate_fund_cur(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_):
        self.e_fund_cur.selection_clear()
        index = int(index)
        if text == "поле должно быть заполнено" and int(action) == 1 and prior_value == "":
            if "поле должно быть заполнено" in prior_value:
                prior_value = prior_value.replace("поле должно быть заполнено", "")
            self.e_fund_cur.delete(0, tk.END)
            self.e_fund_cur.insert(0, prior_value[0:index] + text + prior_value[index:])
            index += len(text)
            self.e_fund_cur.icursor(index)
        elif int(action) == 1 and index == 0 and not text.isnumeric():
            self.e_fund_cur.icursor(index)
            return False
        elif int(action) == 1:
            if not text.isnumeric():
                self.e_fund_cur.delete(0, tk.END)
                self.e_fund_cur.insert(0, prior_value[0:index] + prior_value[index:])
            else:
                if "поле должно быть заполнено" in prior_value:
                    prior_value = prior_value.replace("поле должно быть заполнено", "")
                self.e_fund_cur.config(background="white", foreground="black")
                if len(prior_value) >= 10:
                    self.e_fund_cur.icursor(index)
                    return False
                else:
                    self.e_fund_cur.delete(0, tk.END)
                    self.e_fund_cur.insert(0, prior_value[0:index] + text + prior_value[index:])
                    index += 1
            self.e_fund_cur.icursor(index)
            return True
        elif int(action) == 0:
            if text in "поле должно быть заполнено" and prior_value in "поле должно быть заполнено":
                index = 0
                text = "поле должно быть заполнено"
            self.e_fund_cur.delete(0, tk.END)
            self.e_fund_cur.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_fund_cur.icursor(index)
            return True
        return False

    def validate_pass(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_):
        self.e_pass.selection_clear()
        index = int(index)
        if text == "нет пароля" and int(action) == 1 and prior_value == "":
            if "нет пароля" in prior_value:
                prior_value = prior_value.replace("нет пароля", "")
            self.e_pass.delete(0, tk.END)
            self.e_pass.insert(0, prior_value[0:index] + text + prior_value[index:])
            index += len(text)
            self.e_pass.icursor(index)
        elif int(action) == 1:
            if "нет пароля" in prior_value:
                prior_value = prior_value.replace("нет пароля", "")
            self.e_pass.config(background="white", foreground="black")
            if len(prior_value) >= 10:
                self.e_pass.icursor(index)
                return False
            else:
                self.e_pass.delete(0, tk.END)
                self.e_pass.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_pass.icursor(index)
            return True
        elif int(action) == 0:
            if text in "нет пароля" and prior_value in "нет пароля":
                index = 0
                text = "нет пароля"
            self.e_pass.delete(0, tk.END)
            self.e_pass.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_pass.icursor(index)
            return True
        return False


    def validate_pass_conf(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_):
        self.e_pass_conf.selection_clear()
        index = int(index)
        if text == "нет пароля" and int(action) == 1 and prior_value == "":
            if "нет пароля" in prior_value:
                prior_value = prior_value.replace("нет пароля", "")
            self.e_pass_conf.delete(0, tk.END)
            self.e_pass_conf.insert(0, prior_value[0:index] + text + prior_value[index:])
            index += len(text)
            self.e_pass_conf.icursor(index)
        elif int(action) == 1:
            if "нет пароля" in prior_value:
                prior_value = prior_value.replace("нет пароля", "")
            self.e_pass_conf.config(background="white", foreground="black")
            if len(prior_value) >= 10:
                self.e_pass_conf.icursor(index)
                return False
            else:
                self.e_pass_conf.delete(0, tk.END)
                self.e_pass_conf.insert(0, prior_value[0:index] + text + prior_value[index:])
                index += 1
            self.e_pass_conf.icursor(index)
            return True
        elif int(action) == 0:
            if text in "нет пароля" and prior_value in "нет пароля":
                index = 0
                text = "нет пароля"
            self.e_pass_conf.delete(0, tk.END)
            self.e_pass_conf.insert(0, prior_value[0:index] + prior_value[index + len(text):])
            self.e_pass_conf.icursor(index)
            return True
        return False
