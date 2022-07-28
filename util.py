from datetime import datetime
from connection import get_questions, get_answers


def get_timestamp():
    tstamp = datetime.now().timestamp()
    return tstamp


def generate_new_id() -> int:
    questions = get_questions('./sample_data/question.csv')
    ids = [question['id'] for question in questions]
    return max(ids) + 1


def generate_new_id_answer() -> int:
    answers = get_answers('./sample_data/answer.csv')
    ids = [answer['id'] for answer in answers]
    return max(ids) + 1


def convert_timestamp_to_date(data):

    for row in data:
        time = int(row["submission_time"])
        row["submission_time"] = datetime.utcfromtimestamp(time)

    return data
