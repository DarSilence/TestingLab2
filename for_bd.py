from peewee import *
from datetime import *
from calendar import monthrange

db = SqliteDatabase('MoneyController.db')

array_of_days = {"В 1-ый день месяца": 1, "Во 2-ой день месяца": 2, "В 3-ий день месяца": 3,
                 "В 4-ый день месяца": 4, "В 5-ый день месяца": 5, "В 6-ой день месяца": 6,
                 "В 7-ой день месяца": 7, "В 8-ой день месяца": 8, "В 9-ый день месяца": 9,
                 "В 10-ый день месяца": 10, "Во 11-ый день месяца": 11, "В 12-ый день месяца": 12,
                 "В 13-ый день месяца": 13, "В 14-ый день месяца": 14, "В 15-ый день месяца": 15,
                 "В 16-ый день месяца": 16, "В 17-ый день месяца": 17, "В 18-ый день месяца": 18,
                 "В 19-ый день месяца": 19, "В 20-ый день месяца": 20, "В 21-ый день месяца": 21,
                 "В 22-ой день месяца": 22, "В 23-ий день месяца": 23, "В 24-ый день месяца": 24,
                 "В 25-ый день месяца": 25, "В 26-ой день месяца": 26, "В 27-ой день месяца": 27,
                 "В 28-ой день месяца": 28, "В предпоследний день месяца": -2, "В последний день месяца": -1}


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_name = TextField(primary_key=True)
    cur_fund = IntegerField(null=False)
    day_get_fund = IntegerField(null=False)
    pay_fund = IntegerField(null=False)
    month_got_fund = IntegerField(null=False, default=datetime.now().month)
    year_got_fund = IntegerField(null=False, default=datetime.now().year)

    class Meta:
        db_table = 'users'


class Password(BaseModel):
    user_name = ForeignKeyField(User, related_name="password", to_field='user_name', on_delete='cascade',
                                on_update='cascade', primary_key=True)
    password = TextField(null=False)

    class Meta:
        db_table = 'password'


class Category(BaseModel):
    cat_id = PrimaryKeyField(null=False)
    cat_name = TextField(null=False)

    class Meta:
        db_table = 'category'


class Good(BaseModel):
    good_id = PrimaryKeyField(null=False)
    good_name = TextField(null=False)
    cat_id = ForeignKeyField(Category, related_name="cat_id", to_field='cat_id', on_delete='cascade',
                                on_update='cascade')
    good_price = IntegerField(null=False)

    class Meta:
        db_table = 'goods'


class Bought(BaseModel):
    bought_id = PrimaryKeyField(null=False)
    user_name = ForeignKeyField(User, related_name="user_name", to_field='user_name', on_delete='cascade',
                                on_update='cascade')
    good_id = ForeignKeyField(Good, related_name="good_id", to_field='good_id', on_delete='cascade',
                                on_update='cascade')
    bought_date = DateField(default=datetime.now())
    bought_price = IntegerField(null=False)

    class Meta:
        db_table = 'boughts'


def get_pay_back(bought_id, user_name):
    with db:
        bought = Bought[bought_id]

        user = User[user_name]
        user.cur_fund = user.cur_fund + bought.bought_price
        user.save()

        bought.delete_instance()

def get_bought_id(good_name, bought_price, cat_name, bought_date, user_name):
    with db:
        category = Category.get(Category.cat_name == cat_name)
        goods = [i for i in Good.select().where(Good.good_name == good_name) if Category[i.cat_id].cat_id == category.cat_id]

        bought = []

        for good in goods:
            bought += [i for i in Bought.select().where(Bought.user_name == user_name) if Good[i.good_id].good_id == good.good_id
                      and i.bought_date == bought_date
                      and i.bought_price == int(bought_price)]

        return bought[0].bought_id


def add_good(category_name, good_name, good_price, amount_goods, user_name):
    with (db):
        user = User[user_name]
        if user.cur_fund >= good_price*amount_goods and amount_goods > 0:
            try:
                category = Category.get(Category.cat_name == category_name)
            except:
                Category.insert(cat_name=category_name).execute()
                category = Category.get(Category.cat_name == category_name)

            try:
                goods = Good.select().where(Good.good_name == good_name)
                good = [good for good in goods if Category[good.cat_id].cat_id == category.cat_id and good.good_price == good_price][0]
            except:
                Good.insert(good_name=good_name,
                            cat_id=category.cat_id,
                            good_price=good_price).execute()
                db.commit()
                goods = Good.select().where(Good.good_name == good_name)
                good = [good for good in goods if Category[good.cat_id].cat_id == category.cat_id and good.good_price == good_price][0]

            now = datetime.now()

            Bought.insert(user_name=user_name,
                          good_id=good.good_id,
                          bought_date=date(now.year, now.month, now.day).strftime("%d-%m-%Y"),
                          bought_price=good.good_price*amount_goods).execute()

            user.cur_fund = user.cur_fund - good.good_price * amount_goods
            user.save()
            return True
        else:
            return False


def get_user(name):
    try:
        with db:
            user = User[name]
            return True
    except:
        return False


def check_user_pass(name, password):
    try:
        passes = Password.get(Password.user_name == name)
        if passes.password == password:
            return True
        return False
    except:
        return False


def save_user(name, password, fund_cur, date, fund_pay):
    try:
        with db:
            now = datetime.now()
            date = date if date > 0 else monthrange(now.year, now.month)[1] + 1 + date
            last_year = now.year
            last_month = now.month


            if now.day < date:
                sup = last_year * 12 + last_month - 1
                last_year = sup // 12
                last_month = sup % 12

            User.insert(user_name=name,
                        cur_fund=fund_cur,
                        day_get_fund=date,
                        pay_fund=fund_pay,
                        month_got_fund=last_month,
                        year_got_fund=last_year).execute()
            Password.insert(user_name=name,
                            password=password).execute()
            db.commit()
        return True
    except:
        return False

def get_cats(user_name):
    with db:
        categories = {bought[2] for bought in get_boughts(user_name)}
        return list(categories)


def get_dates(user_name):
    with db:
        dates = {bought[3] for bought in get_boughts(user_name)}
        return list(dates)


def get_goods():
    with db:
        goods = [str(good.good_id) + ". " + good.good_name + "; цена: " + str(good.good_price) for good in Good.select()]

        return goods

def get_good_desr(good_id):
    with db:
        goods = Good[good_id]

        descr = [Category[goods.cat_id].cat_name, goods.good_name, goods.good_price, 1]

        return descr

def get_boughts(name, cat="Все", date="Все"):
    with db:
        boughts = [bought for bought in Bought.select().where(Bought.user_name == name)]

        if cat == date == "Все":
            boughts = [[Good[bought.good_id].good_name, int(bought.bought_price),
                        Category[Good[bought.good_id].cat_id].cat_name, bought.bought_date] for bought in boughts]
        elif cat == "Все" and date != "Все":
            boughts = [[Good[bought.good_id].good_name, int(bought.bought_price),
                        Category[Good[bought.good_id].cat_id].cat_name, bought.bought_date] for bought in boughts if bought.bought_date == date]
        elif date == "Все" and cat != "Все":
            boughts = [[Good[bought.good_id].good_name, int(bought.bought_price),
                        Category[Good[bought.good_id].cat_id].cat_name, bought.bought_date] for bought in boughts if Category[Good[bought.good_id].cat_id].cat_name == cat]
        else:
            boughts = [[Good[bought.good_id].good_name, int(bought.bought_price),
                        Category[Good[bought.good_id].cat_id].cat_name, bought.bought_date] for bought in boughts
                       if Category[Good[bought.good_id].cat_id].cat_name == cat and bought.bought_date == date]

        return boughts


def get_fund(u_name):
    with db:
        selected_user = User[u_name]
        now = datetime.now()
        last_year = now.year
        last_month = now.month
        if selected_user.day_get_fund < 0:
            day = monthrange(last_year, last_month)[1] + 1 - selected_user.day_get_fund
        else:
            day = selected_user.day_get_fund

        year_sub = (last_year - selected_user.year_got_fund)
        month_sub = (last_month - selected_user.month_got_fund)
        if now.day < day:
            month_sub -= 1
            last_month -= 1

        new_fund_cur = selected_user.cur_fund + (year_sub * 12 + month_sub) * selected_user.pay_fund

        selected_user.cur_fund = new_fund_cur
        selected_user.month_got_fund = last_month
        selected_user.year_got_fund = last_year
        selected_user.save()
        db.commit()
        return new_fund_cur


# db.connect()
# User.create_table()
# Password.create_table()
# Category.create_table()
# Good.create_table()
# Bought.create_table()
#
# save_user("Admin", "W1n_ner", 9999999999, 1, 9999999999)
# print(get_fund("Admin"))
# print(get_boughts("Admin"))
# print(add_good("Фрукты", "Яблоки", 20, 15, "Admin"))
# print(get_goods())
# print(get_good_desr('2'))
# print(get_bought_id("Диван", "0", "Мебель", "16-05-2024", "Admin"))

# print(check_user_pass("filterUser", "Pass123!"))