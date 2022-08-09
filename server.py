from flask import Flask, request, render_template, redirect
from connection import write_question_and_return_new_id, write_answer, del_answer_by_id, del_question_by_id, \
    update_question_by_id, \
    update_answer_by_id
import util
from data_manager import get_sorted_questions, get_question_by_id, get_answers_by_question_id, get_answer_by_id, \
    get_questions, get_question_id_by_answer_id
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
    return list()


@app.route('/list', methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        order_by = request.form.get("order_by")
        order_direction = request.form.get("order_direction")
        return redirect(f"/list?order_by={order_by}&order_direction={order_direction}")
    else:
        args = request.args
        order_by = args.get('order_by')
        order_direction = args.get('order_direction')
        questions = get_sorted_questions(order_by, order_direction)
        return render_template('list.html', questions=questions, order_by=order_by,
                               order_direction=order_direction)


@app.route('/question/<question_id>')
def get_question(question_id):
    question_id = int(question_id)
    question = get_question_by_id(question_id)
    question["view_count"] += 1
    update_question_by_id(question_id, question)
    answers = get_answers_by_question_id(question_id)
    return render_template("questions.html", question=question, answers=answers)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = request.form.to_dict()
        update_question_by_id(question_id, question)
        return redirect(f"/question/{question_id}")
    else:
        question = get_question_by_id(int(question_id))
        return render_template('add-question.html', question=question)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
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
        question_id = write_question_and_return_new_id(new_question)
        return redirect(f'/question/{question_id}')  # !!!! NEEED TO BE UPDATED TO HAVE QUESTION ID !!!!
    return render_template('add-question.html', question={})


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def post_answer(question_id):
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
        new_answer['question_id'] = question_id
        write_answer(new_answer)
        return redirect(f'/question/{question_id}')
    return render_template('new-answer.html', id=question_id, answer={})


@app.route('/question/<question_id>/delete')
def delete_question_id(question_id):
    question_id = int(question_id)
    del_question_by_id(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answers(answer_id):
    answer_id = int(answer_id)
    del_answer_by_id(answer_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    question = get_question_by_id(question_id)
    question["vote_count"] += 1
    update_question_by_id(question_id, question)
    return redirect("/list")


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    question = get_question_by_id(question_id)
    question["vote_count"] -= 1
    update_question_by_id(question_id, question)
    return redirect("/list")


@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    question_id = request.args.get("question_id")

    answer = get_answer_by_id(answer_id)
    answer["vote_count"] += 1
    update_answer_by_id(answer_id, answer)
    return redirect("/list")
    return redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down(answer_id):
    question_id = request.args.get("question_id")

    answer = get_answer_by_id(answer_id)
    answer["vote_count"] -= 1
    update_answer_by_id(answer_id, answer)
    return redirect("/list")
    return redirect(f"/question/{question_id}")


# edit answer:
@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        answer = request.form.to_dict()
        update_answer_by_id(answer_id, answer)
        question_id= get_question_id_by_answer_id(answer_id)
        return redirect(f"/question/{question_id}")
    else:
        answer = get_answer_by_id(int(answer_id))
        question_id = get_question_id_by_answer_id(answer_id)
        return render_template('new-answer.html', answer=answer, answer_id=answer_id, question_id=question_id)


if __name__ == "__main__":
    app.run(debug=True)
