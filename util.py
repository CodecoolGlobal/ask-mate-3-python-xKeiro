from datetime import datetime
import bcrypt


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
        row["submission_time"] = datetime.fromtimestamp(time)

    return data


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
