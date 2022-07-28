from flask import Flask, request, render_template, redirect
from connection import write_question, write_answer, del_answer_by_id, del_question_by_id
import util
from data_manager import sort_questions, get_question_by_id, get_answers_by_question_id, get_questions, \
    update_answer_vote_number, update_question_vote_number, get_questions_vote, get_answers_vote
import os
from werkzeug.utils import secure_filename

QUESTIONS_PATH = "./sample_data/question.csv"
ANSWERS_PATH = "./sample_data/answer.csv"
UPLOAD_FOLDER = './static/upload'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "Valami"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def starting_page():
    return redirect('/list')


@app.route('/list', methods=['GET'])
def list():
    questions = get_questions(QUESTIONS_PATH)
    converted_questions = util.convert_timestamp_to_date(questions)
    args = request.args
    order_by = args.get('order_by')
    order_direction = args.get('order_direction')
    if None not in (order_by, order_direction):
        sort_questions(order_by, order_direction)
    return render_template('list.html', questions=converted_questions)


@app.route('/question/<question_id>')
def get_qu(question_id):
    question_id = int(question_id)
    question = get_question_by_id(question_id)
    question["view_number"] += 1
    write_question(QUESTIONS_PATH, question)
    answers = get_answers_by_question_id(question_id)
    return render_template("questions.html", question=question, answers=answers)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = request.form.to_dict()
        write_question(ANSWERS_PATH, question)
        redirect(f"/question/{question_id}")
    else:
        question = get_question_by_id(int(question_id))
        return render_template('add-question.html', question=question)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    question_time_stamp = util.get_timestamp()
    question_id = util.generate_new_id()
    if request.method == "POST":
        new_question = request.form.to_dict()
        # check if the post request has the file part
        # if 'image' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_question["image"] = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))[1:]
        new_question['id'] = str(question_id)
        new_question['submission_time'] = question_time_stamp
        write_question(QUESTIONS_PATH, new_question)
        return redirect(f'/question/{question_id}')
    return render_template('add-question.html', question={})


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def post_answer(question_id):
    answer_time_stamp = util.get_timestamp()
    answer_id = util.generate_new_id_answer()
    if request.method == "POST":
        new_answer = request.form.to_dict()
        # # check if the post request has the file part
        # if 'image' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files['image']
        # # if user does not select file, browser also
        # # submit a empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_answer["image"] = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))[1:]
        new_answer['id'] = str(answer_id)
        new_answer['submission_time'] = answer_time_stamp
        new_answer['question_id'] = question_id
        write_answer('sample_data/answer.csv', new_answer)
        return redirect(f'/question/{question_id}')
    return render_template('new-answer.html', id=question_id, answer={})


@app.route('/question/<question_id>/delete')
def delete_question_id(question_id):
    question_id = int(question_id)
    del_question_by_id(QUESTIONS_PATH, question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answers(answer_id):
    answer_id = int(answer_id)
    del_answer_by_id(ANSWERS_PATH, answer_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    data = get_questions_vote()

    voted_dict = {}
    for dict in data:
        if dict["id"] == question_id:
            voted_dict = {"id": question_id,
                          "submission_time": dict["submission_time"],
                          "view_number": dict["view_number"],
                          "vote_number": int(dict["vote_number"]) + 1,
                          "title": dict["title"],
                          "message": dict["message"],
                          "image": dict["image"]
                          }
    update_question_vote_number(voted_dict)

    return redirect("/list")


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    data = get_questions_vote()

    voted_dict = {}
    for dict in data:
        if dict["id"] == question_id:
            voted_dict = {"id": question_id,
                          "submission_time": dict["submission_time"],
                          "view_number": dict["view_number"],
                          "vote_number": int(dict["vote_number"]) - 1,
                          "title": dict["title"],
                          "message": dict["message"],
                          "image": dict["image"]
                          }
    update_question_vote_number(voted_dict)

    return redirect("/list")


@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down(answer_id):
    question_id = request.args.get("question_id")

    data = get_answers_vote()
    voted_dict = {}
    for dict in data:
        if dict["id"] == answer_id:
            voted_dict = {"id": answer_id,
                          "submission_time": dict["submission_time"],
                          "vote_number": int(dict["vote_number"]) - 1,
                          "question_id": question_id,
                          "message": dict["message"],
                          "image": dict["image"]
                          }
    update_answer_vote_number(voted_dict)
    return redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    question_id = request.args.get("question_id")

    data = get_answers_vote()
    voted_dict = {}
    for dict in data:
        if dict["id"] == answer_id:
            voted_dict = {"id": answer_id,
                          "submission_time": dict["submission_time"],
                          "vote_number": int(dict["vote_number"]) + 1,
                          "question_id": dict["question_id"],
                          "message": dict["message"],
                          "image": dict["image"]
                          }
    update_answer_vote_number(voted_dict)
    return redirect(f"/question/{question_id}")


if __name__ == "__main__":
    app.run(debug=True)
