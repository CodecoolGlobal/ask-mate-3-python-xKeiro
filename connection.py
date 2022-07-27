import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'data.csv'
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
QUESTION_PATH = './sample_data/question.csv'
ANSWER_PATH = './sample_data/answer.csv'


def get_questions(filename):
    questions = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    for i, question in enumerate(questions):
        questions[i]['id'] = int(question['id'])
        questions[i]['submission_time'] = float(question['submission_time'])
        questions[i]['view_number'] = int(question['view_number'])
        questions[i]['vote_number'] = int(question['vote_number'])
    return questions


def get_answers(filename):
    answers = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            answers.append(row)
    for i, answer in enumerate(answers):
        answers[i]['id'] = int(answer['id'])
        answers[i]['submission_time'] = float(answer['submission_time'])

        answers[i]['question_id'] = int(answer['question_id'])
        answers[i]['vote_number'] = int(answer['vote_number'])

    return answers


def write_question(file_path, question_to_write):
    questions = get_questions(QUESTION_PATH)

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


def write_answer(filename, answer_to_write):
    answers = get_answers(ANSWER_PATH)
    index_of_answer_to_replace = None
    for i, answer in enumerate(answers):
        if answer['id'] == answer_to_write['id']:
            index_of_answer_to_replace = i
    if index_of_answer_to_replace is None:
        answers.append(answer_to_write)
    else:
        answers[index_of_answer_to_replace] = answer_to_write
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        writer.writerows(answers)


def get_data_from_file(filename):
    data = []

    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(dict(row))
    return data


def write_data_to_file(dictionary, filename, fieldnames):
    data = get_data_from_file(filename)

    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        writer.writerow(dictionary)


def update_question_vote(dictionary, filename, fieldnames):
    data = get_data_from_file(filename)

    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            if row["id"] == dictionary["id"]:
                row = dictionary
            writer.writerow(row)


def del_question(filename, question_to_delete):
    id_to_delete = None
    questions = get_questions(filename)
    for i, question in enumerate(questions):
        if question['id'] == question_to_delete:
            questions.pop(i)
            id_to_delete = i
    if id_to_delete is not None:
        with open(filename, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=QUESTION_HEADER)
            writer.writeheader()
            writer.writerows(questions)
        answers = get_answers(filename)
        for answer in answers:
            if answer["question_id"] == id_to_delete:
                del_answer(filename, answer)


def del_answer(filename, answer_to_delete):
    answers = get_answers(filename)
    for i, answer in enumerate(answers):
        if answer['id'] == answer_to_delete:
            answers.pop(i)
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ANSWER_HEADER)
        writer.writeheader()
        writer.writerows(answers)
