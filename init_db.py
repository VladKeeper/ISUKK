import sqlite3

connection = sqlite3.connect('database.db')
cur = connection.cursor()

# Создание таблицы для накладных
cur.execute("""CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            status TEXT NOT NULL,
            time DATE
            )""")

# Создание таблицы для товарных позиций
cur.execute("""CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            quantity INTEGER,
            FOREIGN KEY (item_id) REFERENCES items (id)
            )""")

# Вставка данных в таблицу items
cur.execute("INSERT INTO items (title, company, status) VALUES (?, ?, ?)",
            ('Накладная №1 от 25.05.2022', 'Авангард Групп', 'не выдан'))

cur.execute("INSERT INTO items (title, company, status) VALUES (?, ?, ?)",
            ('Накладная №2 от 25.05.2022', 'Браво Групп', 'не выдан'))

# Вставка товарных позиций
cur.execute("INSERT INTO positions (item_id, name, unit, quantity) VALUES (?, ?, ?, ?)",
            (1, 'Мандарины', 'кг', 7))

cur.execute("INSERT INTO positions (item_id, name, unit, quantity) VALUES (?, ?, ?, ?)",
            (1, 'Финики', 'уп', 10))

# Вставка товарных позиций для второй накладной
cur.execute("INSERT INTO positions (item_id, name, unit, quantity) VALUES (?, ?, ?, ?)",
            (2, 'Яблоки', 'кг', 5))

cur.execute("INSERT INTO positions (item_id, name, unit, quantity) VALUES (?, ?, ?, ?)",
            (2, 'Груши', 'кг', 3))

connection.commit()
connection.close()
