import csv
import os
from psycopg2 import sql

import database_common



@database_common.connection_handler
def write_question_and_return_new_id(cursor, fields: dict) -> int:
    query = "INSERT INTO question(" + ", ".join(fields.keys()) + ") VALUES ("
    for value in fields.values():
        query += "%s, "
    query = query[:-2] + ") RETURNING id"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)
    id_of_new_row = cursor.fetchone()["id"]
    return id_of_new_row



@database_common.connection_handler
def write_answer(cursor, fields: dict) -> int:
    query = "INSERT INTO answer(" + ", ".join(fields.keys()) + ") VALUES ("
    for value in fields.values():
        query += "%s, "
    query = query[:-2] + ")"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)



@database_common.connection_handler
def update_question_by_id(cursor, id: int, fields: dict) -> None:
    query = "UPDATE question SET "
    for key, value in fields.items():
        query += f"{key} = %s, "
    query = query[:-2] + f"WHERE id = {id}"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)


@database_common.connection_handler
def update_answer_by_id(cursor, id: int, fields: dict) -> None:
    query = "UPDATE answer SET "
    for key, value in fields.items():
        query += f"{key} = %s, "
    query = query[:-2] + f"WHERE id = {id}"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)


@database_common.connection_handler
def update_question_vote(cursor, id: int, vote_count: int) -> None:
    query = """
        UPDATE question
        SET vote_count = %s
        WHERE id = %s;
        """
    val = (vote_count, id)
    cursor.execute(query, val)


@database_common.connection_handler
def del_question_by_id(cursor, id: int) -> None:
    query = """
        DELETE FROM question
        WHERE id = %s;
        """
    val = (id,)
    cursor.execute(query, val)


@database_common.connection_handler
def del_answer_by_id(cursor, id: int) -> None:
    query = """
        DELETE FROM answer
        WHERE id = %s;
        """
    val = (id,)
    cursor.execute(query, val)

@database_common.connection_handler
def attach_tags(cursor, tags):
    del_tag_by_question_id(tags[0]["question_id"])
    for fields in tags:
        query = "INSERT INTO question_tag(" + ", ".join(fields.keys()) + ") VALUES ("
        for value in fields.values():
            query += "%s, "
        query = query[:-2] + ")"
        val = tuple([field for field in fields.values()])
        cursor.execute(sql.SQL(query), val)

@database_common.connection_handler
def del_tag_by_question_id(cursor, question_id: int) -> None:
    query = """
        DELETE FROM question_tag
        WHERE question_id = %s;
        """
    val = (question_id,)
    cursor.execute(query, val)

@database_common.connection_handler
def write_comment_by_answer_id(cursor, answer_id, new_comment):
    cursor.execute(""" 
    INSERT INTO comment (answer_id, message) 
    VALUES (%(a_s)s, %(n_c)s);
    """, {'a_s': int(answer_id), 'n_c': new_comment})

@database_common.connection_handler
def write_comment_to_comment(cursor,parent_comment_id,answer_id,new_comment):
    cursor.execute("""
    INSERT INTO comment (parent_comment_id, answer_id, message)
     VALUES (%(p_cid)s, %(a_s)s, %(n_c)s); 
     """, {'p_cid' : parent_comment_id, 'a_s': answer_id, 'n_c': new_comment})