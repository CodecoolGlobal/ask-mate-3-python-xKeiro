import os

from flask import Flask, request, render_template, redirect, session
from werkzeug.utils import secure_filename

from bonus_questions import SAMPLE_QUESTIONS
import connection
import data_manager

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
def index():
    questions = data_manager.get_latest_questions()
    session['id'] = 1
    return render_template('index.html', questions=questions)


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
        questions = data_manager.get_sorted_questions(order_by, order_direction)
        return render_template('list.html', questions=questions, order_by=order_by,
                               order_direction=order_direction)


@app.route('/question/<question_id>')
def get_question(question_id):
    question_id = int(question_id)
    question = data_manager.get_question_by_id(question_id)
    question["view_count"] += 1
    connection.update_question_by_id(question_id, question)
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    tags = data_manager.get_tags_by_question_id(question_id)
    return render_template("questions.html", question=question, answers=answers, tags=tags, comments=comments)


@app.route("/search", methods=['POST'])
def get_search_result():
    if request.method == 'POST':
        search_phrase = request.form["search-question"]
        searched_question = data_manager.get_search_question(search_phrase)
        searched_answer = data_manager.get_search_answer(search_phrase)
        for answer in searched_answer:
            question_id = (answer["question_id"])
            searched_question.append(data_manager.get_question_by_id(question_id))
    return render_template("list.html", questions=searched_question, searched_answers=searched_answer,
                           search_phrase=search_phrase)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if 'id' in session:
        if data_manager.is_this_question_belongs_to_user(int(session['id']), int(question_id)):
            if request.method == 'POST':
                question = request.form.to_dict()
                tags = None
                if "tags" in question:
                    question.pop("tags")
                    tags = request.form.getlist("tags")
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    question["image"] = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))[1:]
                connection.update_question_by_id(question_id, question)
                if tags != None:
                    tags = [{"question_id": question_id, "tag_id": tag_id} for tag_id in tags]
                    connection.attach_tags(tags)
                else:
                    connection.del_tag_by_question_id(question_id)
                return redirect(f"/question/{question_id}")
            else:
                question = data_manager.get_question_by_id(int(question_id))
                ids_of_selected_tags = [tag["id"] for tag in data_manager.get_tags_by_question_id(question_id)]
                all_tags = data_manager.get_tags()
                return render_template('add-question.html', question=question, all_tags=all_tags,
                                       ids_of_selected_tags=ids_of_selected_tags)
    return redirect(request.referrer)


@app.route('/add-question', methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        if 'id' in session:
            new_question = request.form.to_dict()
            tags = None
            if "tags" in new_question:
                new_question.pop("tags")
                tags = request.form.getlist("tags")
            # check if the post request has the file part
            # if 'image' not in request.files:
            #     flash('No file part')
            #     return redirect(request.url)
            file = request.files['image']
            # if user does not select file, browser also
            # submit an empty part without filename
            # if file.filename == '':
            #     flash('No selected file')
            #     return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_question["image"] = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))[1:]
            question_id = connection.write_question_and_return_new_id(new_question, int(session['id']))
            if tags != None:
                tags = [{"question_id": question_id, "tag_id": tag_id} for tag_id in tags]
                connection.attach_tags(tags)
                return redirect(f'/question/{question_id}')
        else:
            redirect(request.referrer)
    all_tags = data_manager.get_tags()
    return render_template('add-question.html', question={}, all_tags=all_tags)


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
        # # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_answer["image"] = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))[1:]
        new_answer['question_id'] = question_id
        connection.write_answer(new_answer)
        return redirect(f'/question/{question_id}')
    return render_template('new-answer.html', id=question_id, answer={})


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_a_comment_to_answer(answer_id):
    if request.method == 'GET':
        return render_template('add-comment.html')
    elif request.method == 'POST':
        new_comment = request.form["add-comment"]
        connection.write_comment_by_answer_id(answer_id, new_comment)
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        return redirect(f"/question/{question_id}")


@app.route('/answer/<answer_id>/<parent_comment_id>', methods=['POST', 'GET'])
def add_a_comment_to_comment(answer_id, parent_comment_id):
    if request.method == 'GET':
        return render_template('comment-to-comment.html')
    elif request.method == 'POST':
        new_comment = request.form["comment-to-comment"]
        connection.write_comment_to_comment(parent_comment_id, answer_id, new_comment)
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        return redirect(f"/question/{question_id}")
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        return redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/delete')
def delete_question_id(question_id):
    question_id = int(question_id)
    connection.del_question_by_id(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answers(answer_id):
    answer_id = int(answer_id)
    connection.del_answer_by_id(answer_id)
    return redirect(request.referrer)


@app.route('/question/<question_id>/vote-up')
def question_vote_up(question_id):
    question = data_manager.get_question_by_id(question_id)
    question["vote_count"] += 1
    connection.update_question_by_id(question_id, question)
    return redirect(request.referrer)


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    question = data_manager.get_question_by_id(question_id)
    question["vote_count"] -= 1
    connection.update_question_by_id(question_id, question)
    return redirect(request.referrer)


@app.route('/comment/<comment_id>/vote-up')
def comment_vote_up(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    comment["vote_count"] += 1
    connection.update_comment_by_id(comment_id, comment)
    return redirect(request.referrer)


@app.route('/comment/<comment_id>/vote-down')
def comment_vote_down(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    comment["vote_count"] -= 1
    connection.update_comment_by_id(comment_id, comment)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    answer["vote_count"] += 1
    connection.update_answer_by_id(answer_id, answer)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    answer["vote_count"] -= 1
    connection.update_answer_by_id(answer_id, answer)
    return redirect(request.referrer)


# edit answer:
@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        answer = request.form.to_dict()
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            answer["image"] = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))[1:]
        connection.update_answer_by_id(answer_id, answer)
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        return redirect(f"/question/{question_id}")
    else:
        answer = data_manager.get_answer_by_id(int(answer_id))
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        return render_template('new-answer.html', answer=answer, answer_id=answer_id, question_id=question_id)


# edit comment
@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment_id = int(comment_id)
    if request.method == "POST":
        comment = request.form.to_dict()
        connection.update_comment_submission_time(comment_id)
        edit_count = data_manager.get_edit_count_by_comment_id(comment_id)
        connection.update_comment_edit(comment_id, edit_count)
        connection.update_comment_by_id(comment_id, comment)
        answer_id = data_manager.get_answer_id_from_comment(comment_id)
        question_id = data_manager.get_question_id_by_answer_id(answer_id)
        return redirect(f"/question/{question_id}")
    else:
        comment = data_manager.get_comment_by_id(comment_id)
        answer_id = data_manager.get_answer_id_from_comment(comment_id)
        return render_template('update-comment.html', comment=comment, comment_id=comment_id, answer_id=answer_id)


# delete comment
@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    connection.delete_comment_by_id(comment_id)
    return redirect(request.referrer)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


if __name__ == "__main__":
    app.run(debug=True)
