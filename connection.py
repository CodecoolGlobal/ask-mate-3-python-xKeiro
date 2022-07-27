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
    for i, question in enumerate(questions):
        questions[i]['id'] = int(question['id'])
        questions[i]['submission_time'] = int(question['submission_time'])
        questions[i]['view_number'] = int(question['view_number'])
        questions[i]['vote_number'] = int(question['vote_number'])
    return questions


def get_answers(filename):
    answers = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            answers.append(row)
    return answers


def write_question(file_path, question_to_write):
    questions = get_questions()
    index_of_question_to_replace = None
    for i, question in enumerate(questions):
        if question['id'] == question_to_write['id']:
            index_of_question_to_replace = i
    if index_of_question_to_replace is None:
        questions.append(question_to_write)
    else:
        questions[index_of_question_to_replace] = question_to_write
    with open(file_path, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=QUESTION_HEADER)
        writer.writeheader()
        writer.writerows(questions)


def write_answer(filename, mylist):
    count = len(get_answers(filename))
    mylist.insert(0, count + 1)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ANSWER_HEADER
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        to_write = dict(zip(ANSWER_HEADER, mylist))
        writer.writerow(to_write)
