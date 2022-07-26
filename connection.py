import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_questions(filename):
    questions = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    return questions


def get_answers(filename):
    answers = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            answers.append(row)
    return answers


def write_question(filename, mylist):
    count = len(get_questions(filename))
    mylist.insert(0, count + 1)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = QUESTION_HEADER
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        to_write = dict(zip(QUESTION_HEADER, mylist))
        writer.writerow(to_write)


def write_answer(filename, mylist):
    count = len(get_answers(filename))
    mylist.insert(0, count + 1)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ANSWER_HEADER
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        to_write = dict(zip(ANSWER_HEADER, mylist))
        writer.writerow(to_write)
