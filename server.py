from flask import Flask, render_template, redirect, request

import connection
import util

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    # new_question_id = int(len(connection.get_questions('sample_data/question.csv'))+1)
    question_time_stamp = util.get_timestamp()
    if request.method == "POST":
        new_question = [question_time_stamp, 0, 0, request.form.get('question_title'),
                        request.form.get('question_message'), request.form.get('question_image')]
        connection.write_question('sample_data/question.csv', new_question)
        return redirect('/question/<question_id>')
    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def post_answer():
    answer_time_stamp = util.get_timestamp()
    if request.method == "POST":
        new_answer = [answer_time_stamp, 0, 0, 'question ID', request.form.get('answer_message'),
                      request.form.get('answer_image')]
        connection.write_answer('sample_data/answer.csv', new_answer)
        return redirect('/question/<question_id>')
    return render_template('new-answer.html')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
