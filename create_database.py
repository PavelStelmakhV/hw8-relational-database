from datetime import date, datetime, timedelta
from random import randint
import sqlite3
from sqlite3 import Error
from pathlib import Path
import faker


# Make DataBase. Parameter - path filename with SQL skript
def create_db(filename: Path):
    db_name = filename.parent / f'{filename.name.split(".")[0]}.db'
    if not db_name.exists():
        print(f'create {db_name}')
        with open(filename, 'r') as f:
            sql = f.read()
        # Create connect with DataBase
        with sqlite3.connect(db_name) as conn:
            cur = conn.cursor()
            # execute script from file
            cur.executescript(sql)
            conn.commit()
    else:
        print(f'{db_name} exist')
    return db_name


# Generating of the list of training days
def data_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_data(db_name: Path):

    fake_group = ['KA-81', 'KA-82', 'KA-83']
    fake_disciplines = ['Математический анализ', 'Булевая алгебра', 'Теория вероятности', 'Программирование',
                      'Дискретная математика']
    number_students = 30
    number_teachers = 3
    fake_ = faker.Faker('ru-RU')

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    def fill_group_table():
        sql_group = 'INSERT INTO groups(name) VALUES (?)'
        cur.executemany(sql_group, zip(fake_group, ))

    def fill_students_table():
        fake_students = []
        sql_student = 'INSERT INTO students(fullname, group_id) VALUES (?, ?)'
        for _ in range(number_students):
            fake_students.append((fake_.name(), randint(1, len(fake_group))))
        cur.executemany(sql_student, fake_students)

    def fill_teachers_table():
        fake_teachers = []
        sql_teachers = 'INSERT INTO teachers(fullname) VALUES (?)'
        for _ in range(number_teachers):
            fake_teachers.append((fake_.name(), ))
        cur.executemany(sql_teachers, fake_teachers)

    def fill_disciplines_table():
        sql_disciplines = 'INSERT INTO disciplines(name, teacher_id) VALUES (?, ?)'
        for discipline in fake_disciplines:
            cur.execute(sql_disciplines, (discipline, randint(1, number_teachers)))

    def fill_grades_table():
        start_date = datetime.strptime('01.09.2021', '%d.%m.%Y')
        end_date = datetime.strptime('25.05.2022', '%d.%m.%Y')
        fake_date = data_range(start=start_date, end=end_date)

        sql_disciplines = 'INSERT INTO grades(name, teacher_id) VALUES (?, ?)'
        for discipline in fake_disciplines:
            cur.execute(sql_disciplines, (discipline, randint(1, number_teachers)))

    # for _ in range(number_teachers):
    #     fake_teachers.append(fake_.name())
    #

    # fill_group_table()
    # fill_students_table()
    # fill_teachers_table()
    # fill_disciplines_table()

    conn.commit()


if __name__ == '__main__':
    database_name = create_db(Path('education.sql'))
    fill_data(database_name)
