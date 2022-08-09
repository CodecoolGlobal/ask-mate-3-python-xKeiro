DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS answer;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS question_tag;

CREATE TABLE question
(
    id              SERIAL PRIMARY KEY,
    submission_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT LOCALTIMESTAMP(0),
    view_count      INTEGER                     NOT NULL DEFAULT 0,
    vote_count      INTEGER                     NOT NULL DEFAULT 0,
    title           VARCHAR(150)                NOT NULL,
    message         TEXT                        NOT NULL,
    image           VARCHAR(255),
    edit_count      INTEGER                     NOT NULL DEFAULT 0
);

CREATE TABLE answer
(
    id              SERIAL PRIMARY KEY,
    submission_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT LOCALTIMESTAMP(0),
    vote_count      INTEGER                     NOT NULL DEFAULT 0,
    question_id     INTEGER                     NOT NULL,
    message         TEXT                        NOT NULL,
    image           VARCHAR(255),
    edit_count      INTEGER                     NOT NULL DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE
);

CREATE TABLE comment
(
    id                SERIAL PRIMARY KEY,
    parent_comment_id INTEGER,
    answer_id         INTEGER,
    message           TEXT                        NOT NULL,
    submission_time   TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT LOCALTIMESTAMP(0),
    edit_count        INTEGER                     NOT NULL DEFAULT 0,
    FOREIGN KEY (answer_id) REFERENCES answer (id) ON DELETE CASCADE
);

CREATE TABLE tag
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(25)
);

CREATE TABLE question_tag
(
    question_id INTEGER,
    tag_id      INTEGER,
    FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag (id) ON DELETE CASCADE
);



INSERT INTO question(submission_time, view_count, vote_count, title, message, image)
VALUES ('2017-04-28 08:29:00', 1, 0, 'Test question', 'Am I doing this right?', NULL),
       ('2017-04-28 08:29:00', 56, 9, 'Wordpress loading multiple jQuery Versions',
        'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(''.myBook '').booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', NULL),
       ('2017-04-28 08:29:00', 71, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?',
        '/static/upload\1_pqJe7r067R7ZX569OloQew.jpg'),
       ('2017-04-28 08:29:00', 9, -3, 'Am I doing this right?', 'Am I doing this right?', NULL);

INSERT INTO answer(submission_time, vote_count, question_id, message, image)
VALUES ('2017-04-28 08:29:00', 4, 3, 'You need to use brackets: my_list = []', NULL),

       ('2017-04-28 08:29:00', 35, 3, 'Look it up in the Python docs', NULL),

       ('2017-04-28 08:29:00', -7, 2, 'You need to do something', NULL),

       ('2017-04-28 08:29:00', 3, 4,
        'You forgot to provide example code and context!',
        '/static/upload\76-765183_cute-cat-stickers-series-cute-angry-cat-cartoon.png');

INSERT INTO comment(parent_comment_id, answer_id, message, submission_time)
VALUES ( NULL, 1, 'This is a comment', '2017-04-28 08:29:00'),
       ( 1, NULL, 'This is a comment to a comment', '2017-04-28 08:29:00');

INSERT INTO tag(name)
VALUES ('Code'),
       ('Cooking'),
       ('Newbie');

INSERT INTO question_tag
VALUES (1, 1),
       (1, 2),
       (3, 3);
