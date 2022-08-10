import database_common
from psycopg2 import sql


@database_common.connection_handler
def get_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY id
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor):
    query = """
        SELECT *
        FROM answer
        ORDER BY vote_count DESC
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_comments(cursor):
    query = """
    SELECT * 
    FROM comment 
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_sorted_questions(cursor, order_by: str, order_direction: str):
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
def get_question_by_id(cursor, id: int):
    query = """
        SELECT *
        FROM question
        WHERE id = %s
        """
    val = (id,)
    cursor.execute(query, val)
    return cursor.fetchall()[0]


@database_common.connection_handler
def get_answer_by_id(cursor, id: int):
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
def get_answers_by_question_id(cursor, question_id: int):
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
def get_latest_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time desc
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_comment_by_answer_id(cursor,answer_id: int):
    query = """
    SELECT * FROM comment
    WHERE answer_id = %s
    """
    val = (answer_id, )
    cursor.execute(query, val)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id: int):
    cursor.execute("""
        SELECT question_id FROM answer
        WHERE id = %(answer_id)s""",
        {'answer_id': answer_id})
    return cursor.fetchall()[0]['question_id']
