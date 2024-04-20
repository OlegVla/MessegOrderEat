import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ создать подключение к SQLite базе данных, указанной в db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Соединение с {db_file} установлено. SQLite DB версия: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ создать таблицу в SQLite базе данных, используя предоставленный SQL запрос """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "food_ordering.db"

    sql_create_categories_table = """
    CREATE TABLE IF NOT EXISTS Categories (
        category_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    """

    sql_create_dishes_table = """
    CREATE TABLE IF NOT EXISTS Dishes (
        dish_id INTEGER PRIMARY KEY,
        category_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        price REAL,
        FOREIGN KEY (category_id) REFERENCES Categories (category_id)
    );
    """

    sql_create_orders_table = """
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        total_price REAL,
        status TEXT,
        created_at DATETIME
    );
    """

    sql_create_order_details_table = """
    CREATE TABLE IF NOT EXISTS OrderDetails (
        order_detail_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        dish_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (order_id) REFERENCES Orders (order_id),
        FOREIGN KEY (dish_id) REFERENCES Dishes (dish_id)
    );
    """

    sql_create_payment_methods_table = """
    CREATE TABLE IF NOT EXISTS PaymentMethods (
        payment_method_id INTEGER PRIMARY KEY,
        method TEXT NOT NULL
    );
    """

    sql_create_payments_table = """
    CREATE TABLE IF NOT EXISTS Payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        payment_method_id INTEGER,
        amount REAL,
        paid_at DATETIME,
        FOREIGN KEY (order_id) REFERENCES Orders (order_id),
        FOREIGN KEY (payment_method_id) REFERENCES PaymentMethods (payment_method_id)
    );
    """

    sql_create_reviews_table = """
    CREATE TABLE IF NOT EXISTS Reviews (
        review_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        dish_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_at DATETIME,
        FOREIGN KEY (dish_id) REFERENCES Dishes (dish_id)
    );
    """

    # создаем подключение к базе данных
    conn = create_connection(database)

    # создаем таблицы
    if conn is not None:
        create_table(conn, sql_create_categories_table)
        create_table(conn, sql_create_dishes_table)
        create_table(conn, sql_create_orders_table)
        create_table(conn, sql_create_order_details_table)
        create_table(conn, sql_create_payment_methods_table)
        create_table(conn, sql_create_payments_table)
        create_table(conn, sql_create_reviews_table)

        conn.close()
    else:
        print("Ошибка! Невозможно установить соединение с базой данных.")


if __name__ == '__main__':
    main()




def insert_data(conn, insert_sql, data):
    """ Вставляет данные в БД """
    try:
        c = conn.cursor()
        c.executemany(insert_sql, data)
        conn.commit()
    except Error as e:
        print(e)


def select_data(conn, query):
    """ Выполняет запрос SELECT и печатает результаты """
    try:
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()

        for row in rows:
            print(row)
    except Error as e:
        print(e)


def main():
    # Как было определено ранее
    database = "food_ordering.db"
    conn = create_connection(database)

    # Создаем таблицы
    ...

    # Вставка данных в таблицы
    categories_data = [(1, 'Закуски'), (2, 'Основные блюда')]
    insert_data(conn, 'INSERT INTO Categories (category_id, name) VALUES (?, ?)', categories_data)

    dishes_data = [
        (1, 1, 'Салат Цезарь', 'Классический Цезарь с курицей', 290.0),
        (2, 2, 'Стейк', 'Жареный стейк с соусом', 550.0)
    ]
    insert_data(conn, 'INSERT INTO Dishes (dish_id, category_id, name, description, price) VALUES (?, ?, ?, ?, ?)',
                dishes_data)

    orders_data = [
        (1, 101, 840.0, 'Ожидание', '2023-10-12 18:30:00'),
        (2, 102, 400.0, 'Готово к доставке', '2023-10-13 20:20:00')
    ]
    insert_data(conn, 'INSERT INTO Orders (order_id, user_id, total_price, status, created_at) VALUES (?, ?, ?, ?, ?)',
                orders_data)

    order_details_data = [
        (1, 1, 1, 2, 580.0),
        (2, 2, 2, 1, 550.0)
    ]
    insert_data(conn,
                'INSERT INTO OrderDetails (order_detail_id, order_id, dish_id, quantity, price) VALUES (?, ?, ?, ?, ?)',
                order_details_data)

    # Визуализация данных
    print("Категории:")
    select_data(conn, "SELECT * FROM Categories")

    print("\nБлюда:")
    select_data(conn, "SELECT * FROM Dishes")

    print("\nЗаказы:")
    select_data(conn, "SELECT * FROM Orders")

    # Закрываем соединение
    conn.close()


if __name__ == '__main__':
    main()
