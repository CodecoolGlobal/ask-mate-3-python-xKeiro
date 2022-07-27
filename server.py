from flask import Flask, request, render_template, redirect
from data_manager import sort_questions, get_question_by_id
from connection import write_question

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/list', methods=['GET'])
def list():
    args = request.args
    order_by = args.get('order_by')
    order_direction = args.get('order_direction')
    if None not in (order_by, order_direction):
        sort_questions(order_by, order_direction)
    return render_template('list.html')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = request.form.to_dict()
        write_question("/sample_data/answer.csv", question)
        redirect(f"/question/{question_id}")
    else:
        question = get_question_by_id(question_id)
        return render_template('add_question.html', question=question)


if __name__ == "__main__":
    app.run()
