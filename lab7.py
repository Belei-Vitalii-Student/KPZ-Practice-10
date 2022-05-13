import sys
import sqlite3
global db
global sql

db = sqlite3.connect('accounts')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT
)""")

db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS tasks (
    task TEXT
)""")

db.commit()


def start_action():
    print("""Виберіть дію: 
        1. Вийти
        2. Створити новий аккаунт
        3. Створити завдання
        4. Видалити завдання
        5. Змінити завдання
        6. Перевірити список завдань
        """)
    user_input = input("Для вибору дії введіть цифру цієї дії: ")
    return user_input


def registation_operation():
    userLogin = input("Логін (введіть логін): ")
    userPassword = input("Пароль (введіть пароль): ")
    userTask = ''
    sql.execute(f"SELECT task FROM tasks WHERE task = '{userTask}'")

    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO tasks VALUES (?)", (userTask,))
        db.commit()
        print("Таблиця завдання успішно створена")
    sql.execute(f"SELECT login FROM users WHERE login = '{userLogin}'")

    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?)", (userLogin, userPassword))
        db.commit()
        print("Регестрація завершена!")
    else:
        print("Такий аккаунт уже існує!")

    for value in sql.execute("SELECT * FROM users"):
        print(value)

    for value in sql.execute("SELECT * FROM tasks"):
        print(value)


def login_operation():
    userLogin = input("Login: ")
    userPassword = input("Password: ")

    sql.execute(f"SELECT login FROM users WHERE login = '{userLogin}'")
    if sql.fetchone() is None:
        print("Не вірний логін або пароль!")
        userAction = input("Хочете створити новий аккаунт? (print 'y' or 'n')")
        if userAction == 'y':
            registation_operation()
        else:
            False
    else:
        print("Успішний вхід!")
        return start_action()


def taskAction(action):
    if action == "add":
        user_task = input("Введіть назву завдання: ")
        sql.execute(f"INSERT INTO tasks VALUES (?)", (user_task,))
        db.commit()
    elif action == "delete":
        user_task = input("Введіть назву завдання якого хочете видалити: ")
        sql.execute(f"DELETE FROM tasks WHERE task = '{user_task}'")
        db.commit()
        print("Завдання видалено")
    elif action == "change":
        user_task = input("Введіть назву завдання яке хочете змінити: ")
        sql.execute(f"UPDATE tasks SET task = '{user_task}'")
        db.commit()
    elif action == "list":
        for value in sql.execute("SELECT * FROM tasks"):
            print(value)


def user_actions(user_input):
    if user_input == "1":
        sys.exit()
    elif user_input == "2":
        registation_operation()
    elif user_input == "3":
        taskAction("add")
    elif user_input == "4":
        taskAction("delete")
    elif user_input == "5":
        taskAction("change")
    elif user_input == "6":
        taskAction("list")

def main():
    user_actions(login_operation())


main()
