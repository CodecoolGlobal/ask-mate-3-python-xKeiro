from flask import Flask, request, render_template, redirect
from connection import write_question, write_answer, get_questions
import util
from data_manager import sort_questions, get_question_by_id, get_answer_by_id

app = Flask(__name__)
QUESTIONS_PATH = "./sample_data/question.csv"
ANSWERS_PATH = "./sample_data/answer.csv"


@app.route('/list', methods=['GET'])
def list():
    questions = get_questions(QUESTIONS_PATH)
    args = request.args
    order_by = args.get('order_by')
    order_direction = args.get('order_direction')
    if None not in (order_by, order_direction):
        sort_questions(order_by, order_direction)
    return render_template('list.html', questions=questions)


@app.route('/question/')
def question_page():
    question = get_questions(QUESTIONS_PATH)
    return render_template("questionmain.html", question=question)


@app.route('/question/<question_id>')
def get_qu(question_id):
    question_id = int(question_id)
    question = get_question_by_id(question_id)
    answer = get_answer_by_id(question_id)
    return render_template("questions.html", question=question, answer=answer)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = request.form.to_dict()
        write_question(ANSWERS_PATH, question)
        redirect(f"/question/{question_id}")
    else:
        question = get_question_by_id(question_id)
        return render_template('add-question.html', question=question)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    question_time_stamp = util.get_timestamp()
    question_id = util.generate_new_id()
    if request.method == "POST":
        new_question = request.form.to_dict()
        new_question['id'] = str(question_id)
        new_question['submission_time'] = question_time_stamp
        write_question('./sample_data/question.csv', new_question)
        return redirect(f'/question/{question_id}')
    return render_template('add-question.html', question={})


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def post_answer(question_id):
    answer_time_stamp = util.get_timestamp()
    answer_id = util.generate_new_id_answer()
    if request.method == "POST":
        new_answer = request.form.to_dict()
        new_answer['id'] = str(answer_id)
        new_answer['submission_time'] = answer_time_stamp
        new_answer['question_id'] = question_id
        write_answer('sample_data/answer.csv', new_answer)
        return redirect(f'/question/{question_id}')
    return render_template('new-answer.html', id=question_id, answer={})


if __name__ == "__main__":
    app.run(debug=True)
