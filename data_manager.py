from connection import get_questions, get_answers, write_question, write_answer


def sort_questions(order_by: str, order_direction: str) -> None:
    '''
    :param order_by: title, submission_time, message, view_number, vote_number
    :param order_direction: asc, desc
    '''
    if order_by in ['title', 'submission_time', 'message', 'view_number', 'vote_number'] \
            and order_direction in ['asc', 'desc']:
        questions = get_questions("./sample_data/question.csv")
        sorted_questions = sorted(questions, key=lambda question: question[order_by], reverse=order_direction == "desc")
        write_question("./sample_data/question.csv", sorted_questions)


def get_question_by_id(question_id: int) -> dict:
    questions = get_questions("./sample_data/question.csv")
    for i, question in enumerate(questions):
        if question["id"] == question_id:
            return question


def get_answers_by_question_id(question_id: int) -> list[dict]:
    answers_list = []
    answers = get_answers("./sample_data/answer.csv")
    for i, answer in enumerate(answers):
        if answer["question_id"] == question_id:
            answers_list.append(answer)
    return answers_list
