import csv
import os
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_count', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_count', 'vote_count', 'title', 'message', 'image']
QUESTION_PATH = './sample_data/question.csv'
ANSWER_PATH = './sample_data/answer.csv'


@database_common.connection_handler
def write_question(cursor, fields):
    query = "INSERT INTO question("
    for key in fields.keys():
        query += f"{key}, "
    query = query[:-2] + f") VALUES ("
    for value in fields.values():
        query += "%s, "
    query = query[:-2] + ")"
    val = tuple([field for field in fields.values()])
    cursor.execute(sql.SQL(query), val)
    #
    # query = """
    #     INSERT INTO question(view_count, vote_count, title, message, image, edit_count)
    #     VALUES (%s,%s,%s,%s,%s,%s)
    # """
    # val = (question_to_write["view_count"], question_to_write["vote_count"], question_to_write["title"],
    #        question_to_write["message"], question_to_write["image"], question_to_write["edit_count"])
    # cursor.execute(query, val)


# def write_questions(file_path, questions_to_write):
#     with open(file_path, mode="w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=QUESTION_HEADER)
#         writer.writeheader()
#         writer.writerows(questions_to_write)


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


# def get_data_from_file(filename):
#     data = []
#
#     with open(filename) as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             data.append(dict(row))
#     return data


# def write_data_to_file(dictionary, filename, fieldnames):
#     data = get_data_from_file(filename)
# 
#     with open(filename, "w") as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)
#         writer.writerow(dictionary)


@database_common.connection_handler
def update_question_by_id(cursor, id, fields):
    # query = """
    #     UPDATE question
    #     SET """
    # for field in fields:
    #     query += "%s=%s "
    # query += "WHERE id = %s"
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

@database_common.connection_handler
def write_comment_by_answer_id(cursor, answer_id, new_comment):
    cursor.execute(""" 
    INSERT INTO comment (answer_id, message) 
    VALUES (%(a_s)s, %(n_c)s);
    """, {'a_s': int(answer_id), 'n_c': new_comment})