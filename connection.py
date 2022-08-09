import csv
import os
from psycopg2 import sql

import database_common



@database_common.connection_handler
def write_question_and_return_new_id(cursor, fields):
    query = "INSERT INTO question("
    for key in fields.keys():
        query += f"{key}, "
    query = query[:-2] + f") VALUES ("
    for value in fields.values():
        query += "%s, "
    query = query[:-2] + ") RETURNING id"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)
    id_of_new_row = cursor.fetchone()["id"]
    return id_of_new_row



@database_common.connection_handler
def write_answer(cursor, fields):
    query = "INSERT INTO answer("
    for key in fields.keys():
        query += f"{key}, "
    query = query[:-2] + f") VALUES ("
    for value in fields.values():
        query += "%s, "
    query = query[:-2] + ")"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)



@database_common.connection_handler
def update_question_by_id(cursor, id, fields):
    query = "UPDATE question SET "
    for key, value in fields.items():
        query += f"{key} = %s, "
    query = query[:-2] + f"WHERE id = {id}"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)


@database_common.connection_handler
def update_answer_by_id(cursor, id, fields):
    query = "UPDATE answer SET "
    for key, value in fields.items():
        query += f"{key} = %s, "
    query = query[:-2] + f"WHERE id = {id}"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)


@database_common.connection_handler
def update_question_vote(cursor, id, vote_count):
    query = """
        UPDATE question
        SET vote_count = %s
        WHERE id = %s;
        """
    val = (vote_count, id)
    cursor.execute(query, val)


@database_common.connection_handler
def del_question_by_id(cursor, id):
    query = """
        DELETE FROM question
        WHERE id = %s;
        """
    val = (id,)
    cursor.execute(query, val)


@database_common.connection_handler
def del_answer_by_id(cursor, id):
    query = """
        DELETE FROM answer
        WHERE id = %s;
        """
    val = (id,)
    cursor.execute(query, val)
