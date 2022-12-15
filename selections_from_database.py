import sqlite3
from query_sql import query_list, task_list


def execute_query(sql: str) -> list:
    with sqlite3.connect('education.db') as conn:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


if __name__ == '__main__':
    [print(el) for el in task_list]
    print('[exit - выход]')
    while True:
        num_query = input('Введите номер запроса: ')
        if num_query == 'exit':
            break

        try:
            print(task_list[int(num_query)-1])
            print(execute_query(query_list[int(num_query)-1]))
        except IndexError as e:
            print('Нет такого номера')
        except ValueError:
            print('Значение должно быть целым числом')







