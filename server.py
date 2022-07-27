from flask import Flask, request, render_template, redirect
from data_manager import sort_questions, get_question_by_id, get_answer_by_id
import connection

app = Flask(__name__)
QUESTIONS_PATH = "./sample_data/question.csv"
ANSWERS_PATH = "./sample_data/answer.csv"


@app.route('/list', methods=['GET'])
def list():
    questions = connection.get_questions(QUESTIONS_PATH)
    args = request.args
    order_by = args.get('order_by')
    order_direction = args.get('order_direction')
    if None not in (order_by, order_direction):
        sort_questions(order_by, order_direction)
    return render_template('list.html', questions=questions)

@app.route('/question/')
def question_page():
    question = connection.get_questions(QUESTIONS_PATH)
    return render_template("questionmain.html",question=question)

@app.route('/question/<question_id>')
def get_qu(question_id):
    question_id = int(question_id)
    question = get_question_by_id(question_id)
    answer= get_answer_by_id(question_id)
    return render_template("questions.html",question=question,answer=answer)

@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = request.form.to_dict()
        connection.write_question(ANSWERS_PATH, question)
        redirect(f"/question/{question_id}")
    else:
        question = get_question_by_id(question_id)
        return render_template('add_question.html', question=question)


if __name__ == "__main__":
    app.run(debug=True)
