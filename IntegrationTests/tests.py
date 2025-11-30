import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import tkinter as tk
from peewee import SqliteDatabase
from money_controller import *

# Тестовая БД
Test_db = 'testMoneyController.db'


class GUIHelper:
    """Вспомогательный класс для работы с GUI элементами"""

    @staticmethod
    def set_entry_text(entry_widget, text):
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, text)
        entry_widget.update()

    @staticmethod
    def set_combobox_value(combobox, value):
        combobox.set(value)
        combobox.event_generate('<<ComboboxSelected>>')
        combobox.update()

    @staticmethod
    def click_button(button_widget):
        button_widget.invoke()
        button_widget.update()

    @staticmethod
    def get_treeview_data(treeview):
        data = []
        for item in treeview.get_children():
            values = treeview.item(item)['values']
            data.append(values)
        return data


@pytest.fixture
def run_database():
    # Подготовка базы данных

    # Запуск тестовой БД
    test_db = SqliteDatabase(Test_db)

    # Замена БД в моделях
    for model in [User, Password, Category, Good, Bought]:
        model._meta.database = test_db

    # Создание таблиц
    test_db.create_tables([User, Password, Category, Good, Bought])

    yield

    # Очистка БД
    if os.path.exists(Test_db):
        test_db.close()
        os.remove(Test_db)


class TestMoneyController:
    def test_successful_user_registration(self, run_database):
        # Тест на регистрацию пользователя
        app = App()
        app.withdraw()

        helper = GUIHelper()

        # Переход на форму регистрации
        helper.click_button(app.f_log_in.btn_register)
        assert hasattr(app, 'f_registr'), f"После нажатия должен открыться экран регистрации. {app}"

        # Заполнение данных регистрации
        helper.set_entry_text(app.f_registr.e_name, "registerUser")
        helper.set_entry_text(app.f_registr.e_pass, "Test_123")
        helper.set_entry_text(app.f_registr.e_pass_conf, "Test_123")
        helper.set_entry_text(app.f_registr.e_fund_cur, "1500")
        helper.set_entry_text(app.f_registr.e_fund_pay, "5000")
        helper.set_combobox_value(app.f_registr.com_date, "В 15-ый день месяца")

        # Нажатие кнопки регистрации
        helper.click_button(app.f_registr.btn_reg)

        # Проверка перехода на главный экран
        assert hasattr(app, 'f_main'), "После регистрации должен открыться главный экран."
        assert app.u_name == "registerUser", "Имя пользователя должно сохраниться."

        # Проверка отображения баланса
        balance = app.f_main.l_balance.cget("text")
        assert balance == 1500, f"Баланс должен отображаться корректно. Получено: {balance} вместо {1500}."

        app.destroy()

    def test_login_with_existing_user(self, run_database):
        # Тест на авторизацию существующего пользователя
        app = App()
        app.withdraw()

        helper = GUIHelper()

        # Запись пользователя в базу данных
        save_user("loginUser", "Pass123!", 2000, 1, 1000)

        # Заполнение формы авторизации
        helper.set_entry_text(app.f_log_in.e_name, "loginUser")
        helper.set_entry_text(app.f_log_in.e_pass, "Pass123!")

        # Нажатие кнопки входа
        helper.click_button(app.f_log_in.btn_log_in)

        # Проверка на успешность авторизации
        assert hasattr(app, 'f_main'), "После авторизации должен открыться главный экран"
        assert app.u_name == "loginUser", "Должно быть установлено имя пользователя"

        app.destroy()

    def test_invalid_login_attempt(self, run_database):
        # Тест на авторизацию несуществующего пользователя
        app = App()
        # app.withdraw()

        helper = GUIHelper()

        # Попытка входа с несуществующими данными
        helper.set_entry_text(app.f_log_in.e_name, "nonexistentUser")
        helper.set_entry_text(app.f_log_in.e_pass, "Wrong_p4ssword!")
        helper.click_button(app.f_log_in.btn_log_in)

        # Проверка экрана. Должен остаться экран авторизации
        assert hasattr(app, 'f_log_in'), "При ошибке входа должны остаться на форме авторизации"

        # Проверка отображения ошибки
        error_displayed = app.f_log_in.l_error.winfo_viewable()
        error_text = app.f_log_in.l_error.cget("text")

        assert error_displayed, f"Сообщение об ошибке должно отображаться."
        assert "не существует" in error_text, f"Должна быть ошибка о несуществующем пользователе. Получено: {error_text}"

        app.destroy()

    def test_successful_purchase(self, run_database):
        # Тест на оформление покупки
        app = App()
        app.withdraw()

        helper = GUIHelper()

        # Запись пользователя в бд и его авторизация
        save_user("purchaseUser", "Pass123!", 3000, 1, 1000)
        helper.set_entry_text(app.f_log_in.e_name, "purchaseUser")
        helper.set_entry_text(app.f_log_in.e_pass, "Pass123!")
        helper.click_button(app.f_log_in.btn_log_in)

        # Получение начального бюджета пользователя
        initial_fund = int(app.f_main.l_balance.cget("text"))

        # Переход на экран покупки
        helper.click_button(app.f_main.b_buy)

        # Заполнение данных покупки и её выполнение
        helper.set_entry_text(app.f_bought.e_category, "Еда")
        helper.set_entry_text(app.f_bought.e_good_name, "Молоко")
        helper.set_entry_text(app.f_bought.e_good_price, "80")
        helper.set_entry_text(app.f_bought.e_amount_goods, "2")
        helper.click_button(app.f_bought.b_buy)

        # Проверка возвращения на главный экран
        assert hasattr(app, 'f_main'), "После покупки должен быть главный экран"

        # Проверка обновления баланса средств пользователя
        new_fund = int(app.f_main.l_balance.cget("text"))
        expected_fund = initial_fund - 80 * 2
        assert new_fund == expected_fund, f"Баланс должен уменьшиться на 160. Было: {initial_fund}, стало: {new_fund}"

        # Проверка отображения совершённой покупки в таблице
        purchases_data = helper.get_treeview_data(app.f_main.t_boughts)
        milk_purchase = [p for p in purchases_data if "Молоко" in p[0]]
        assert len(milk_purchase) > 0, "Покупка молока должна быть в таблице"

        app.destroy()

    def test_purchase_with_insufficient_funds(self, run_database):
        # Тест на покупку при недостатке средств
        app = App()
        app.withdraw()

        helper = GUIHelper()

        # Запись пользователя в бд и его авторизация
        save_user("poorUser", "Pass123!", 100, 1, 50)
        helper.set_entry_text(app.f_log_in.e_name, "poorUser")
        helper.set_entry_text(app.f_log_in.e_pass, "Pass123!")
        helper.click_button(app.f_log_in.btn_log_in)

        # Получение списка текущих покупок
        initial_boughts = get_boughts("poorUser")

        # Переход на экран покупки
        helper.click_button(app.f_main.b_buy)

        # Заполнение данных покупки с стоимостью товара превышающей бюджета и её выполнение
        helper.set_entry_text(app.f_bought.e_category, "Электроника")
        helper.set_entry_text(app.f_bought.e_good_name, "Ноутбук")
        helper.set_entry_text(app.f_bought.e_good_price, "50000")
        helper.set_entry_text(app.f_bought.e_amount_goods, "1")
        helper.click_button(app.f_bought.b_buy)

        # Проверка, что возвращения на главный экран не произошло
        assert hasattr(app, 'f_bought'), "При ошибке должны остаться на экране покупки"

        # Проверка отображения ошибки
        error_text = app.f_bought.l_error.cget("text")
        assert "Не хватает средств" in error_text, f"Должна отображаться ошибка недостатка средств. Получено: {error_text}"

        # Проверка неизменности списка покупок
        assert initial_boughts == get_boughts("poorGuiUser"), f"Записи покупок не должны пополниться пустыми покупками."

        app.destroy()

    def test_refund(self, run_database):
        # Тест возврата покупки
        app = App()
        app.withdraw()

        helper = GUIHelper()

        # Запись пользователя и его покупки в бд и его авторизация
        save_user("refundUser", "Pass123!", 2000, 1, 500)
        add_good("Одежда", "Джинсы", 1500, 1, "refundUser")
        helper.set_entry_text(app.f_log_in.e_name, "refundUser")
        helper.set_entry_text(app.f_log_in.e_pass, "Pass123!")
        helper.click_button(app.f_log_in.btn_log_in)

        # Запись баланс до возврата
        balance_before_refund = int(app.f_main.l_balance.cget("text"))

        # Переход на экран возврата средств за покупку
        helper.click_button(app.f_main.b_return)

        # Выбор покупки для возврата и выполнение возврата
        purchases_list = app.f_return.com_boughts.cget("values")
        assert len(purchases_list) > 0, "Должны быть доступные покупки для возврата"
        helper.set_combobox_value(app.f_return.com_boughts, purchases_list[0])
        helper.click_button(app.f_return.b_delete)

        # Возвращение на главный экран и её проверка
        helper.click_button(app.f_return.b_back)
        assert hasattr(app, 'f_main'), "После возврата средств должен быть выполнен переход на главный экран"

        # Проверка обновление баланса
        balance_after_refund = int(app.f_main.l_balance.cget("text"))
        assert balance_after_refund > balance_before_refund, "Баланс должен увеличиться после возврата"

        # Проверка списка покупок для возврата
        purchases_list = app.f_return.com_boughts.cget("values")
        assert len(purchases_list) == 0, "Не должно быть покупок для возврата"

        app.destroy()

    def test_category_filter(self, run_database):
        # Тест фильтрации покупок по категории
        app = App()
        app.withdraw()

        helper = GUIHelper()

        # Запись пользователя и его покупкок в разных категориях в бд
        save_user("filterUser", "Pass123!", 5000, 1, 1000)
        add_good("Еда", "Хлеб", 50, 2, "filterUser")
        add_good("Одежда", "Футболка", 500, 1, "filterUser")
        add_good("Еда", "Молоко", 80, 1, "filterUser")
        add_good("едА", "Буханка хлеба", 45, 4, "filterUser")

        # Авторизация пользователя
        helper.set_entry_text(app.f_log_in.e_name, "filterUser")
        helper.set_entry_text(app.f_log_in.e_pass, "Pass123!")
        helper.click_button(app.f_log_in.btn_log_in)

        # Получение всех покупок и их фильтрация по категории "Еда"
        initial_count = len(helper.get_treeview_data(app.f_main.t_boughts))
        assert initial_count == 4, f"Должно быть 3 покупки. Получено: {initial_count}"

        # Фильтрация по категории "Еда" и количественная проверка отфильтрованных данных
        helper.set_combobox_value(app.f_main.com_cat, "Еда")
        filtered_purchases = helper.get_treeview_data(app.f_main.t_boughts)
        filtered_count = len(filtered_purchases)
        assert filtered_count == 2, f"После фильтрации по 'Еда' должно быть 2 покупки. Получено: {filtered_count}"

        # Проверка на соответствие категории отобранных по фильтру товаров
        for purchase in filtered_purchases:
            assert purchase[2] == "Еда", f"Все покупки должны быть категории 'Еда'. Найдено: {purchase[2]}"

        app.destroy()


class TestValidation:
    def test_password_validation_in_registration(self, run_database):
        # Тест валидации пароля при регистрации
        app = App()
        # app.withdraw()

        helper = GUIHelper()

        # Переход на экран регистрации
        helper.click_button(app.f_log_in.btn_register)

        # Ввод слабого пароля
        helper.set_entry_text(app.f_registr.e_pass, "123")
        helper.set_entry_text(app.f_registr.e_pass_conf, "123")
        helper.click_button(app.f_registr.btn_reg)

        # Проверка отображения требований к паролю по длине
        requirements_text = app.f_registr.l_desr.cget("text")
        assert "Пароль должен быть не меньше 6 символов" in requirements_text, f"Должны отображаться требования к длине пароля. {requirements_text}"

        # Ввод слабого пароля увеличенной длины
        helper.set_entry_text(app.f_registr.e_pass, "1234567")
        helper.set_entry_text(app.f_registr.e_pass_conf, "1234567")
        helper.click_button(app.f_registr.btn_reg)

        # Проверка отображения требований к паролю по длине
        updated_text = app.f_registr.l_desr.cget("text")
        assert "Пароль должен быть не меньше 6 символов" not in updated_text, f"Должны отображаться требования к длине пароля. {updated_text}"
        assert updated_text[:] == requirements_text[:74], f"Должны иметь одинаковый набор требований, за исключением числа символов."

        app.destroy()

    def test_numeric_field_validation(self, run_database):
        # Тест валидации числовых полей
        app = App()
        app.withdraw()

        helper = GUIHelper()

        # Переход на форму регистрации
        helper.click_button(app.f_log_in.btn_register)

        # Попытка ввода букв и специальных символов в числовое поле
        helper.set_entry_text(app.f_registr.e_fund_cur, "abc!_")

        # Проверка отбрасывания нечисловых символов в поле
        current_value = app.f_registr.e_fund_cur.get()
        assert not current_value, "Числовое поле должно быть пустым при вводе символов отличных от чисел"

        app.destroy()
