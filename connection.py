import csv
import os
from psycopg2 import sql

import database_common


# region ----------------QUESTION------------------

@database_common.connection_handler
def write_question_and_return_new_id(cursor, fields: dict, user_id: int) -> int:
    query = "INSERT INTO question(" + ", ".join(fields.keys()) + ") VALUES ("
    for value in fields.values():
        query += "%s, "
    query = query[:-2] + ") RETURNING id"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)
    id_of_new_row = cursor.fetchone()["id"]
    write_user_question(user_id, id_of_new_row)
    return id_of_new_row


@database_common.connection_handler
def write_user_question(cursor, user_id: int, question_id: int) -> None:
    query = """
    INSERT INTO user_question(user_id, question_id)
    VALUES (%s,%s)
    """
    val = user_id, question_id
    cursor.execute(query, val)


@database_common.connection_handler
def update_question_by_id(cursor, id: int, fields: dict) -> None:
    query = "UPDATE question SET "
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


# endregion

# region ----------------ANSWER------------------


@database_common.connection_handler
def write_answer(cursor, fields: dict, user_id:int) -> int:
    query = "INSERT INTO answer(" + ", ".join(fields.keys()) + ") VALUES ("
    for value in fields.values():
        query += "%s, "
    query = query[:-2] + ")"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)
    id_of_new_row = cursor.fetchone()["id"]
    write_user_answer(user_id, id_of_new_row)


@database_common.connection_handler
def write_user_answer(cursor, user_id: int, answer_id: int) -> None:
    query = """
    INSERT INTO user_answer(user_id, answer_id)
    VALUES (%s,%s)
    """
    val = user_id, answer_id
    cursor.execute(query, val)



@database_common.connection_handler
def update_answer_by_id(cursor, id: int, fields: dict) -> None:
    query = "UPDATE answer SET "
    for key, value in fields.items():
        query += f"{key} = %s, "
    query = query[:-2] + f"WHERE id = {id}"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)


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
def update_answer_edit_count(cursor, id, edit_count):
    cursor.execute("""
    UPDATE answer SET edit_count= edit_count+1
    WHERE id = %(id)s""",
                   {'id': id, 'edit_count': edit_count})


# endregion

#region ----------------COMMENT------------------


@database_common.connection_handler
def write_comment_by_answer_id(cursor, answer_id, new_comment):
    cursor.execute(""" 
    INSERT INTO comment (answer_id, message) 
    VALUES (%(a_s)s, %(n_c)s);
    """, {'a_s': int(answer_id), 'n_c': new_comment})


@database_common.connection_handler
def update_comment_by_id(cursor, id: int, fields: dict) -> None:
    query = "UPDATE comment SET "
    for key, value in fields.items():
        query += f"{key} = %s, "
    query = query[:-2] + f"WHERE id = {id}"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)


@database_common.connection_handler
def update_comment_edit(cursor, id, edit_count):
    cursor.execute("""
    UPDATE comment SET edit_count= edit_count+1
    WHERE id = %(id)s""",
                   {'id': id, 'edit_count': edit_count})


@database_common.connection_handler
def update_comment_submission_time(cursor, id):
    query = """
        UPDATE comment
        SET submission_time=LOCALTIMESTAMP(0)
        WHERE id = %s;
        """
    val = (id,)
    cursor.execute(query, val)


@database_common.connection_handler
def write_comment_to_comment(cursor, parent_comment_id, answer_id, new_comment):
    cursor.execute("""
    INSERT INTO comment (parent_comment_id, answer_id, message)
     VALUES (%(p_cid)s, %(a_s)s, %(n_c)s); 
     """, {'p_cid': parent_comment_id, 'a_s': answer_id, 'n_c': new_comment})


@database_common.connection_handler
def delete_comment_by_id(cursor, comment_id):
    cursor.execute("""
    DELETE FROM comment 
    WHERE id =%(comment_id)s""",
                   {'comment_id': comment_id})


# endregion

# region ----------------TAG------------------


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


# endregion

# region ----------------USER------------------


# endregion
