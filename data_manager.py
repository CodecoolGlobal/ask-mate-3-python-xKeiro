import database_common
from psycopg2 import sql


# region ----------------QUESTION------------------
@database_common.connection_handler
def get_questions(cursor) -> list[dict]:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_sorted_questions(cursor, order_by: str, order_direction: str) -> list[dict]:
    '''
    :param order_by: title, submission_time, message, view_count, vote_count
    :param order_direction: asc, desc
    '''
    if order_by in ['id', 'title', 'submission_time', 'message', 'view_count', 'vote_count'] \
            and order_direction in ['asc', 'desc']:
        query = f"""
            SELECT *
            FROM question
            ORDER BY {order_by} {order_direction.upper()}
        """
        cursor.execute(sql.SQL(query))
        return cursor.fetchall()
    else:
        return get_questions()


@database_common.connection_handler
def get_question_by_id(cursor, id: int) -> dict:
    query = """
        SELECT *
        FROM question
        WHERE id = %s
        """
    val = (id,)
    cursor.execute(query, val)
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_latest_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id: int):
    cursor.execute("""
        SELECT question_id FROM answer
        WHERE id = %(answer_id)s""",
                   {'answer_id': answer_id})
    return cursor.fetchall()[0]['question_id']


@database_common.connection_handler
def is_this_question_belongs_to_user(cursor, user_id: int, question_id: int) -> bool:
    query = """
    SELECT
        CASE WHEN EXISTS(
            SELECT * FROM user_question
            WHERE user_id=%s AND question_id = %s
            )
            THEN TRUE
            ELSE FALSE
        END
    """
    val = (user_id, question_id)
    cursor.execute(query, val)
    return cursor.fetchall()[0]['case']


@database_common.connection_handler
def get_search_question(cursor, search_phrase):
    cursor.execute("""
    SELECT * FROM question
    WHERE title ILIKE %(m)s
    OR message ILIKE %(m)s; 
    """, {'m': "%" + search_phrase + '%'})
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_by_user_id(cursor, user_id: int):
    query = """
    SELECT question_id FROM user_question
    WHERE user_id=%s
    """
    val = (user_id,)
    cursor.execute(query, val)
    question_dictionaries_in_list = cursor.fetchall()
    if question_dictionaries_in_list != []:
        question_ids = [question['question_id'] for question in question_dictionaries_in_list]
    return question_ids


# endregion

# region ----------------ANSWER------------------


@database_common.connection_handler
def get_answers(cursor) -> list[dict]:
    query = """
        SELECT *
        FROM answer
        ORDER BY vote_count DESC
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_question_id(cursor, question_id: int) -> list[dict]:
    query = """
        SELECT *
        FROM answer
        WHERE question_id = %s
        ORDER BY vote_count DESC
        """
    val = (question_id,)
    cursor.execute(query, val)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_id_from_question_id(cursor, question_id: int) -> list[dict]:
    query = """
        SELECT id
        FROM answer
        WHERE question_id = %s
        """
    val = (question_id,)
    cursor.execute(query, val)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_id(cursor, id: int) -> dict:
    query = """
        SELECT *
        FROM answer
        WHERE id = %s
        ORDER BY vote_count DESC
        """
    val = (id,)
    cursor.execute(query, val)
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_search_answer(cursor, search_phrase):
    cursor.execute(""" 
    SELECT * FROM answer
    WHERE message ILIKE %(m)s;
    """, {'m': "%" + search_phrase + '%'})
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_edit_count_by_answer_id(cursor, id):
    query = """
        SELECT edit_count
        FROM answer
        WHERE id = %s
        """
    val = (id,)
    cursor.execute(query, val)
    return cursor.fetchall()[0]['edit_count']


@database_common.connection_handler
def is_this_answer_belongs_to_user(cursor, user_id: int, answer_id: int) -> bool:
    query = """
    SELECT
        CASE WHEN EXISTS(
            SELECT * FROM user_answer
            WHERE user_id=%s AND answer_id = %s
            )
            THEN TRUE
            ELSE FALSE
        END
    """
    val = (user_id, answer_id)
    cursor.execute(query, val)
    return cursor.fetchall()[0]['case']


@database_common.connection_handler
def get_answers_by_user_id(cursor, user_id: int):
    query = """
    SELECT answer_id FROM user_answer
    WHERE user_id=%s
    """
    val = (user_id,)
    cursor.execute(query, val)
    answer_dictionaries_in_list = cursor.fetchall()
    if answer_dictionaries_in_list != []:
        answer_ids = [answer['answer_id'] for answer in answer_dictionaries_in_list]
    return answer_ids


# endregion

# region ----------------COMMENT------------------

@database_common.connection_handler
def get_comments(cursor):
    query = """
    SELECT * 
    FROM comment 
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_answer_id(cursor, answer_id: int):
    query = """
    SELECT * FROM comment
    WHERE answer_id = %s
    """
    val = (answer_id,)
    cursor.execute(query, val)
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_id_from_comment(cursor, comment_id):
    cursor.execute("""
        SELECT answer_id FROM comment
        WHERE id = %(comment_id)s""",
                   {'comment_id': comment_id})
    return cursor.fetchall()[0]['answer_id']


@database_common.connection_handler
def is_this_comment_belongs_to_user(cursor, user_id: int, comment_id: int) -> bool:
    query = """
    SELECT
        CASE WHEN EXISTS(
            SELECT * FROM user_comment
            WHERE user_id=%s AND comment_id = %s
            )
            THEN TRUE
            ELSE FALSE
        END
    """
    val = (user_id, comment_id)
    cursor.execute(query, val)
    return cursor.fetchall()[0]['case']


@database_common.connection_handler
def get_comments_by_user_id(cursor, user_id: int):
    query = """
    SELECT comment_id FROM user_comment
    WHERE user_id=%s
    """
    val = (user_id,)
    cursor.execute(query, val)
    comment_dictionaries_in_list = cursor.fetchall()
    if comment_dictionaries_in_list != []:
        comment_ids = [comment['comment_id'] for comment in comment_dictionaries_in_list]
    return comment_ids


# endregion

# region ----------------TAG------------------

@database_common.connection_handler
def get_tags(cursor) -> list[dict]:
    query = """
        SELECT *
        FROM tag
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_tags_by_question_id(cursor, question_id: int) -> list[dict]:
    query = """
        SELECT tag.*
        FROM tag
        LEFT JOIN question_tag ON tag.id = question_tag.tag_id
        WHERE question_tag.question_id = %s
        """
    val = (question_id,)
    cursor.execute(query, val)
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor, id):
    query = """
        SELECT *
        FROM comment
        WHERE id = %s
        """
    val = (id,)
    cursor.execute(query, val)
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_edit_count_by_comment_id(cursor, id):
    query = """
        SELECT edit_count
        FROM comment
        WHERE id = %s
        """
    val = (id,)
    cursor.execute(query, val)
    return cursor.fetchall()[0]['edit_count']


# endregion


# region ----------------USERS------------------

@database_common.connection_handler
def get_user_by_id(cursor, user_id):
    cursor.execute("""
        SELECT id,
        username,
        email,
        registration_date,
        number_of_asked_questions,
        number_of_answers,
        number_of_comments,
        reputation
        FROM "user"
        WHERE id=%(user_id)s""",
                   {'user_id': user_id})
    user = cursor.fetchall()[0]
    return user


@database_common.connection_handler
def get_question_ids_by_user(cursor, user_id):
    cursor.execute("""
        SELECT question_id
        FROM user_question
        JOIN "user" ON user_question.user_id ="user".id
        WHERE id=%(user_id)s""",
                   {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_ids_by_user(cursor, user_id):
    cursor.execute("""
        SELECT answer_id
        FROM user_answer
        JOIN "user" ON user_answer.user_id ="user".id
        WHERE id=%(user_id)s""",
                   {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_ids_by_user(cursor, user_id):
    cursor.execute("""
        SELECT comment_id
        FROM user_comment
        JOIN "user" ON user_comment.user_id ="user".id
        WHERE id=%(user_id)s""",
                   {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id_from_question_id(cursor, question_id):
    cursor.execute("""
        SELECT user_id
        FROM user_question
        LEFT JOIN question ON question.id = user_question.question_id
        WHERE id=%(question_id)s""",
                   {'question_id': question_id})
    return cursor.fetchone()


@database_common.connection_handler
def user_name_from_user_id(cursor, user_id):
    cursor.execute("""
        SELECT username
        FROM "user"
        WHERE id=%(user_id)s""",
                   {'user_id': user_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_id_from_answer(cursor, answer_id):
    cursor.execute("""
        SELECT user_id
        FROM user_answer
        LEFT JOIN answer ON answer.id = user_answer.answer_id
        WHERE id=%(answer_id)s""",
                   {'answer_id': answer_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_name_from_question(cursor, question_id):
    query = """
    SELECT username
    FROM "user"
    JOIN user_question ua ON "user".id = ua.user_id
    WHERE ua.question_id = %s
    """
    val = (question_id,)
    cursor.execute(query, val)
    return cursor.fetchone()['username']


@database_common.connection_handler
def get_user_name_from_answer(cursor, answer_id):
    query = """
    SELECT username
    FROM "user"
    JOIN user_answer ua ON "user".id = ua.user_id
    WHERE ua.answer_id = %s
    """
    val = (answer_id,)
    cursor.execute(query, val)
    return cursor.fetchone()['username']


@database_common.connection_handler
def get_user_name_from_comment(cursor, comment_id):
    query = """
    SELECT username
    FROM "user"
    JOIN user_comment ua ON "user".id = ua.user_id
    WHERE ua.comment_id = %s
    """
    val = (comment_id,)
    cursor.execute(query, val)
    return cursor.fetchone()['username']

# endregion
