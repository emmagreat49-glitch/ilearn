"""Shared DB insert helper used by all seed modules."""


def insert_lessons_and_quizzes(c, course_id, lessons_data, quizzes_data):
    """
    lessons_data: list of (order, title, module_id, content, duration)
                  OR legacy (order, title, content, duration)
    quizzes_data: dict of {lesson_order: [(q, a, b, c, ans, expl), ...]}
    """
    lesson_ids = {}
    for item in lessons_data:
        if len(item) == 5:
            order, title, module_id, content, duration = item
        else:
            order, title, content, duration = item
            module_id = None

        c.execute(
            """INSERT INTO lessons
               (course_id, lesson_title, lesson_content, lesson_order, duration_mins, module_id)
               VALUES (?,?,?,?,?,?)""",
            (course_id, title, content, order, duration, module_id)
        )
        lesson_ids[order] = c.lastrowid

    for lesson_order, questions in quizzes_data.items():
        lid = lesson_ids.get(lesson_order)
        if lid:
            for q, a, b, cc, ans, expl in questions:
                c.execute(
                    """INSERT INTO quiz
                       (lesson_id,question,option_a,option_b,option_c,correct_answer,explanation)
                       VALUES (?,?,?,?,?,?,?)""",
                    (lid, q, a, b, cc, ans, expl)
                )
