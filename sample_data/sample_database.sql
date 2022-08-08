DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS answer;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS question_tag;

CREATE TABLE question
(
    id              SERIAL PRIMARY KEY,
    submission_time FLOAT        NOT NULL,
    view_number     INTEGER      NOT NULL,
    vote_number     INTEGER      NOT NULL,
    title           VARCHAR(150) NOT NULL,
    message         TEXT         NOT NULL,
    image           VARCHAR(255),
    edit_count      INTEGER      NOT NULL DEFAULT 0
);

CREATE TABLE answer
(
    id              SERIAL PRIMARY KEY,
    submission_time FLOAT   NOT NULL,
    vote_number     INTEGER NOT NULL,
    question_id     INTEGER NOT NULL,
    message         TEXT    NOT NULL,
    image           VARCHAR(255),
    edit_count      INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE
);

CREATE TABLE comment
(
    id                SERIAL PRIMARY KEY,
    parent_comment_id INTEGER,
    answer_id         INTEGER,
    message           TEXT    NOT NULL,
    submission_time   FLOAT   NOT NULL,
    edit_count        INTEGER NOT NULL DEFAULT 0,
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



INSERT INTO question
VALUES (1, 1659038514.0, 1, 0, 'Test question', 'Am I doing this right?', NULL),
       (2, 1493068124.0, 56, 9, 'Wordpress loading multiple jQuery Versions',
        'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(''.myBook '').booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', NULL),
       (3, 1659036107.082323, 71, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?',
        '/static/upload\1_pqJe7r067R7ZX569OloQew.jpg'),
       (4, 1659038414.753183, 9, -3, 'Am I doing this right?', 'Am I doing this right?', NULL);

INSERT INTO answer
VALUES (1, 1493398154.0, 4, 3, 'You need to use brackets: my_list = []', NULL),

       (2, 1493088154.0, 35, 3, 'Look it up in the Python docs', NULL),

       (3, 1658935457.113151, -7, 2, 'You need to do something', NULL),

       (4, 1659038513.407616, 3, 4,
        'You forgot to provide example code and context!,/static/upload\76-765183_cute-cat-stickers-series-cute-angry-cat-cartoon.png',
        NULL);

INSERT INTO comment
VALUES (1, NULL, 1, 'This is a comment', 1893088154.0),
       (2, 1, NULL, 'This is a comment to a comment', 1993088154.0);

INSERT INTO tag
VALUES (1, 'Code'),
       (2, 'Cooking'),
       (3, 'Newbie');

INSERT INTO question_tag
VALUES  (1,1),
        (1,2),
        (3,3);
