from psycopg2.extras import RealDictCursor

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
