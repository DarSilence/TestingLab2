from tkinter import messagebox as mbox
from Log_in_frame import *
from Register_frame import *
from Main_frame import *
from Bought_frame import *
from Return_frame import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Вход в систему')
        self.change_geometry(360, 230)
        self.resizable(width=False, height=False)
        self.put_frames()

    def put_frames(self):
        self.u_name = None

        self.f_log_in = LogInFrame(self)
        self.f_registr = RegisterFrame(self)

        self.f_log_in.grid(row=0, column=0)

    def to_registr(self):
        self.f_log_in.grid_forget()
        self.change_geometry(600, 500)
        self.f_registr.grid(row=0, column=0)

    def to_main(self):
        self.title("Менеджер покупок")
        self.menu = MainMenu(self)
        self.config(menu=self.menu)
        self.f_registr.grid_forget()
        self.f_registr.clear_widgets()
        self.f_log_in.grid_forget()
        self.f_log_in.clear_widgets()
        self.f_main = MainFrame(self)
        self.f_bought = BoughtFrame(self)
        self.f_return = ReturnFrame(self)
        get_fund(self.u_name)
        self.change_geometry(650, 400)
        self.f_main.grid(row=0, column=0)


    def to_log_in(self):
        self.f_registr.grid_forget()
        self.f_registr.clear_widgets()
        self.change_geometry(360, 230)
        self.f_log_in.grid(row=0, column=0)

    def back(self):
        self.f_main.grid_forget()
        self.menu.destroy()
        self.f_bought.destroy()
        self.f_return.destroy()
        self.change_geometry(360, 230)
        self.f_log_in.grid(row=0, column=0)

    def to_bougth(self):
        self.title("Оформление покупки")
        self.f_main.grid_forget()
        self.f_bought.get_values()
        self.change_geometry(450, 300)
        self.f_bought.grid(row=0, column=0)

    def from_bought(self):
        self.title("Менеджер покупок")
        self.f_bought.grid_forget()
        self.f_bought.clear_widgets()
        self.f_main.re_table()
        self.f_main.get_values()
        self.change_geometry(650, 400)
        self.f_main.grid(row=0, column=0)

    def to_return(self):
        self.title("Возврат денежных средств")
        self.f_main.grid_forget()
        self.f_return.get_values()
        self.change_geometry(360, 170)
        self.f_return.grid(row=0, column=0)

    def from_return(self):
        self.title("Менеджер покупок")
        self.f_return.grid_forget()
        self.f_return.clear_widgets()
        self.f_main.re_table()
        self.f_main.get_values()
        self.change_geometry(650, 400)
        self.f_main.grid(row=0, column=0)

    def change_geometry(self, width, height):
        w = self.winfo_screenwidth() // 2 - width//2
        h = self.winfo_screenheight() // 2 - height//2
        self.geometry(f'{width}x{height}+{w}+{h}')

    def close(self):
        self.destroy()


class MainMenu(tk.Menu):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        self.parent = mainwindow

        sys_menu = tk.Menu(self)
        help_menu = tk.Menu(self)

        sys_menu.add_command(label="Сменить пользователя", command=self.parent.back)
        sys_menu.add_command(label="Выход", command=self.parent.close)

        help_menu.add_command(label="Информация", command=self.show_info)

        self.add_cascade(label="Система", menu=sys_menu)
        self.add_cascade(label="Справка", menu=help_menu)

    def show_info(self):
        mbox.showinfo("FAQ", 'Это приложение'
                             ' для контроля собственных средств.'
                             ' Оно позволяет составлять покупки,'
                             ' сортировать их или удалять, с'
                             ' возвратом средств.')


if __name__ == "__main__":
    app = App()
    app.mainloop()