import os

from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.utils import secure_filename

from bonus_questions import SAMPLE_QUESTIONS
import connection
import data_manager
import util

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
    for i, question in enumerate(questions):
        questions[i]["username"] = data_manager.get_user_name_from_answer(question['id'])

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
        for i, question in enumerate(questions):
            questions[i]["username"] = data_manager.get_user_name_from_answer(question['id'])
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

    question['username'] = data_manager.get_user_name_from_question(question_id)
    question['reputation'] = data_manager.get_reputation_from_question_username(question['username'])
    # user to answer
    for i, answer in enumerate(answers):
        answers[i]["username"] = data_manager.get_user_name_from_answer(answer['id'])
        answers[i]['reputation'] = data_manager.get_reputation_from_answer_username(answer["username"])

    # user to comment
    for i, comment in enumerate(comments):
        comments[i]["username"] = data_manager.get_user_name_from_comment(comment['id'])
        comments[i]["reputation"] = data_manager.get_reputation_from_comments_username(comment["username"])

    user_content = dict()
    if "user_id" in session:
        user_id = session["user_id"]
        user_content["question_ids"] = data_manager.get_questions_by_user_id(user_id)
        user_content["answer_ids"] = data_manager.get_answers_by_user_id(user_id)
        user_content["comment_ids"] = data_manager.get_comments_by_user_id(user_id)
    return render_template("questions.html", question=question, answers=answers, tags=tags, comments=comments,
                           user_content=user_content)


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
    if 'user_id' in session:
        if data_manager.is_this_question_belongs_to_user(int(session['user_id']), int(question_id)):
            if request.method == 'POST':
                question = request.form.to_dict()
                tags = None
                question_edit_count = data_manager.get_question_edit_count_by_id(question_id)
                connection.update_question_edit_count(question_id, question_edit_count)
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
    if 'user_id' in session:
        if request.method == "POST":
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
            new_question['user_id'] = session['user_id']
            question_id = connection.write_question_and_return_new_id(new_question, int(session['user_id']))
            if tags != None:
                tags = [{"question_id": question_id, "tag_id": tag_id} for tag_id in tags]
                connection.attach_tags(tags)
            return redirect(f'/question/{question_id}')
        else:
            all_tags = data_manager.get_tags()
            return render_template('add-question.html', question={}, all_tags=all_tags)
    return redirect(url_for('login'))


@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def post_answer(question_id):
    if 'user_id' in session:
        if request.method == "POST":
            new_answer = request.form.to_dict()
            # # check if the post request has the file part
            # if 'image' not in request.files:
            #     flash('No file part')
            #     return redirect(request.url)
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
            new_answer['user_id'] = session['user_id']
            connection.write_answer(new_answer, int(session['user_id']))
            return redirect(f'/question/{question_id}')
        return render_template('new-answer.html', id=question_id, answer={})
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/new-comment', methods=['POST', 'GET'])
def add_a_comment_to_answer(answer_id):
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('add-comment.html')
        elif request.method == 'POST':
            new_comment = request.form["add-comment"]
            connection.write_comment_by_answer_id(answer_id, new_comment, int(session['user_id']))
            question_id = data_manager.get_question_id_by_answer_id(answer_id)
            return redirect(f"/question/{question_id}")
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/<parent_comment_id>', methods=['POST', 'GET'])
def add_a_comment_to_comment(answer_id, parent_comment_id):
    if 'user_id' in session:
        if request.method == 'GET':
            return render_template('comment-to-comment.html')
        elif request.method == 'POST':
            new_comment = request.form["comment-to-comment"]
            connection.write_comment_to_comment(parent_comment_id, answer_id, new_comment, int(session['user_id']))
            question_id = data_manager.get_question_id_by_answer_id(answer_id)
            return redirect(f"/question/{question_id}")
            question_id = data_manager.get_question_id_by_answer_id(answer_id)
            return redirect(f"/question/{question_id}")
    return redirect(request.referrer)


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
    user_name = data_manager.get_user_name_from_question(question_id)
    connection.update_add_reputation_by_username(user_name)
    return redirect(request.referrer)


@app.route('/question/<question_id>/vote-down')
def question_vote_down(question_id):
    question = data_manager.get_question_by_id(question_id)
    question["vote_count"] -= 1
    connection.update_question_by_id(question_id, question)
    user_name = data_manager.get_user_name_from_question(question_id)
    connection.update_decrease_reputation_by_username(user_name)
    return redirect(request.referrer)


@app.route('/comment/<comment_id>/vote-up')
def comment_vote_up(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    comment["vote_count"] += 1
    connection.update_comment_by_id(comment_id, comment)
    user_name = data_manager.get_user_name_from_comment(comment_id)
    connection.update_add_reputation_by_username(user_name)
    return redirect(request.referrer)


@app.route('/comment/<comment_id>/vote-down')
def comment_vote_down(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    comment["vote_count"] -= 1
    connection.update_comment_by_id(comment_id, comment)
    user_name = data_manager.get_user_name_from_comment(comment_id)
    connection.update_decrease_reputation_by_username(user_name)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/vote-up')
def answer_vote_up(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    answer["vote_count"] += 1
    connection.update_answer_by_id(answer_id, answer)
    user_name = data_manager.get_user_name_from_answer(answer_id)
    connection.update_add_reputation_by_username(user_name)
    return redirect(request.referrer)


@app.route('/answer/<answer_id>/vote-down')
def answer_vote_down(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    answer["vote_count"] -= 1
    connection.update_answer_by_id(answer_id, answer)
    user_name = data_manager.get_user_name_from_answer(answer_id)
    connection.update_decrease_reputation_by_username(user_name)
    return redirect(request.referrer)


# edit answer:
@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if 'user_id' in session:
        if data_manager.is_this_answer_belongs_to_user(int(session['user_id']), int(answer_id)):
            if request.method == 'POST':
                answer = request.form.to_dict()
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    answer["image"] = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))[1:]
                answer_edit_count = data_manager.get_answer_edit_count_by_answer_id(answer_id)
                connection.update_answer_edit_count(answer_id, answer_edit_count)
                connection.update_answer_by_id(answer_id, answer)
                question_id = data_manager.get_question_id_by_answer_id(answer_id)
                return redirect(f"/question/{question_id}")
            else:
                answer = data_manager.get_answer_by_id(int(answer_id))
                question_id = data_manager.get_question_id_by_answer_id(answer_id)
                return render_template('new-answer.html', answer=answer, answer_id=answer_id, question_id=question_id)
        return redirect(request.referrer)


# edit comment
@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment_id = int(comment_id)
    if 'user_id' in session:
        if data_manager.is_this_comment_belongs_to_user(int(session['user_id']), comment_id):
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
                return render_template('update-comment.html', comment=comment, comment_id=comment_id,
                                       answer_id=answer_id)
    return redirect(request.referrer)


# delete comment
@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    connection.delete_comment_by_id(comment_id)
    return redirect(request.referrer)


@app.route('/users')
def user_list():
    users = data_manager.get_users()
    return render_template('users.html', users=users)


@app.route('/user/<user_id>')
def user_page(user_id):
    user = data_manager.get_user_by_id(user_id)
    user_question_ids = data_manager.get_question_ids_by_user(user_id)
    questions = []
    for item in user_question_ids:
        id = item['question_id']
        questions.append(data_manager.get_question_by_id(id))

    user_answer_ids = data_manager.get_answer_ids_by_user(user_id)
    answers = []
    for item in user_answer_ids:
        answer_id = item['answer_id']
        answers.append(data_manager.get_answer_by_id(answer_id))

    user_comment_ids = data_manager.get_comment_ids_by_user(user_id)
    comments = []
    answer_ids_by_comment = []
    if user_comment_ids:
        for item in user_comment_ids:
            comment_id = item['comment_id']
            comments.append(data_manager.get_comment_by_id(comment_id))
            answer_id = data_manager.get_answer_id_from_comment(comment_id)
            question_id = data_manager.get_question_id_by_answer_id(answer_id)
    else:
        question_id = ''

    return render_template('user-page.html', user=user, questions=questions, answers=answers, comments=comments,
                           question_id=question_id)


@app.route("/bonus-questions")
def bonus_questions():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/tags")
def tags_page():
    tags = data_manager.get_tags()
    searched_tag_id = request.args.get('tag_id')
    filtered_questions = data_manager.get_questions_by_tag_id(searched_tag_id)
    return render_template("tags.html", tags=tags, questions=filtered_questions)


@app.route('/registration', methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("un")
        email = request.form.get("em")
        password = util.hash_password(request.form.get("pw"))
        data_manager.register_new_user(
            username, email, password)
        return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/accept/<answer_id>', methods=["POST"])
def accept_answer(answer_id):
    question = data_manager.get_question_id_by_answer_id(answer_id)
    answer = data_manager.get_answer_by_id(answer_id)
    data_manager.change_accept_state(answer_id)
    return redirect(request.referrer)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_details = data_manager.user_login(username)
        if user_details:
            username_login = user_details.get('username')
            username_password = user_details.get('password')
            user_id = int(user_details.get('id'))
            if username_login != username or util.verify_password(password, username_password) is False:
                error = 'Invalid username/password. Please try again.'
            else:
                session['user_id'] = user_id
                session['username'] = username
                return redirect(url_for('index'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
