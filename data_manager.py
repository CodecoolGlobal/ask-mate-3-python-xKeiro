import database_common
from psycopg2 import sql


# ----------------QUESTION------------------
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


# ----------------ANSWER------------------


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


# ----------------COMMENT------------------

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


# ----------------TAG------------------

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
