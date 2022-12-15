task_list = [
    "1. 5 студентов с наибольшим средним баллом по всем предметам.",
    "2. 1 студент с наивысшим средним баллом по одному предмету.",
    "3. средний балл в группе по одному предмету.",
    "4. Средний балл в потоке.",
    "5. Какие курсы читает преподаватель.",
    "6. Список студентов в группе.",
    "7. Оценки студентов в группе по предмету.",
    "8. Оценки студентов в группе по предмету на последнем занятии.",
    "9. Список курсов, которые посещает студент.",
    "10. Список курсов, которые студенту читает преподаватель.",
    "11. Средний балл, который преподаватель ставит студенту.",
    "12. Средний балл, который ставит преподаватель."
]
query_list = [
    """
    --1. 5 студентов с наибольшим средним баллом по всем предметам.
    SELECT s.fullname, round(avg(g.grade), 2) AS avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 5;
    """,

    """
    --2. 1 студент с наивысшим средним баллом по одному предмету.
    SELECT d.name, s.fullname, round(avg(g.grade), 2) AS avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    WHERE d.id =1
    GROUP BY s.fullname, d.name 
    ORDER BY avg_grade DESC
    LIMIT 1;
    """,

    """
    --3. средний балл в группе по одному предмету.
    SELECT d.name, gr.name , round(avg(g.grade), 2) AS avg_grade
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    LEFT JOIN [groups] gr ON gr.id = s.group_id 
    WHERE d.id =1
    GROUP BY gr.name, d.name 
    ORDER BY avg_grade DESC;
    """,

    """
    --4. Средний балл в потоке.
    SELECT round(avg(g.grade), 2) AS avg_grade
    FROM grades g;
    """,

    """
    --5. Какие курсы читает преподаватель.
    SELECT d.id, t.fullname, d.name  
    FROM teachers t 
    LEFT JOIN disciplines d ON t.id = d.teacher_id
    WHERE t.id = 1;
    """,

    """
    --6. Список студентов в группе.
    SELECT s.id, s.fullname, gr.name 
    FROM students s 
    LEFT JOIN [groups] gr ON gr.id = s.group_id 
    WHERE gr.id = 1;
    """,

    """
    --7. Оценки студентов в группе по предмету.
    SELECT s.id, d.name, gr.name , s.fullname, g.grade, g.date_of 
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    LEFT JOIN [groups] gr ON gr.id = s.group_id 
    WHERE d.id =1 AND gr.id = 1;
    """,

    """
    --8. Оценки студентов в группе по предмету на последнем занятии.
   	SELECT s.id, d.name, gr.name , s.fullname, g.grade, g.date_of 
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    LEFT JOIN [groups] gr ON gr.id = s.group_id 
    WHERE d.id =1 AND gr.id = 1 AND g.date_of =(SELECT g.date_of 
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN [groups] gr ON gr.id = s.group_id 
    WHERE g.discipline_id = 1 and gr.id = 1
    ORDER BY g.date_of DESC 
    LIMIT 1);
    """,

    """
    --9. Список курсов, которые посещает студент.
    SELECT d.name, s.fullname
    FROM grades g
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    WHERE s.id =1
    GROUP BY d.name;
    """,

    """
    --10. Список курсов, которые студенту читает преподаватель.
    SELECT s.fullname, t.fullname, d.name  
    FROM grades g 
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    LEFT JOIN teachers t ON t.id = d.teacher_id
    WHERE t.id = 1 AND g.student_id = 1
    GROUP BY d.name;
    """,

    """
    --11. Средний балл, который преподаватель ставит студенту.
    SELECT DISTINCT s.fullname, t.fullname, round(avg(g.grade), 2) AS avg_grade
    FROM grades g 
    LEFT JOIN students s ON s.id = g.student_id
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    LEFT JOIN teachers t ON t.id = d.teacher_id
    WHERE t.id = 1 AND s.id = 1
    GROUP BY s.fullname;
    """,

    """
    --12. Средний балл, который ставит преподаватель.
    SELECT t.fullname, round(avg(g.grade), 2) AS avg_grade
    FROM grades g 
    LEFT JOIN disciplines d  ON d.id = g.discipline_id
    LEFT JOIN teachers t ON t.id = d.teacher_id
    WHERE t.id = 1
    GROUP BY t.fullname
    """
]
