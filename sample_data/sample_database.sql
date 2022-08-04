DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS answer;
DROP TABLE IF EXISTS question_answer;

CREATE TABLE question
(
    id              SERIAL PRIMARY KEY,
    submission_time FLOAT        NOT NULL,
    view_number     INTEGER      NOT NULL,
    vote_number     INTEGER      NOT NULL,
    title           VARCHAR(150) NOT NULL,
    message         TEXT         NOT NULL,
    image           VARCHAR(255)
);

CREATE TABLE answer
(
    id              SERIAL PRIMARY KEY,
    submission_time FLOAT   NOT NULL,
    vote_number     INTEGER NOT NULL,
    message         TEXT    NOT NULL,
    image           VARCHAR(255)
);

CREATE TABLE question_answer
(
    question_id INTEGER NOT NULL,
    answer_id   INTEGER,
    PRIMARY KEY (question_id, answer_id),
    FOREIGN KEY (question_id) REFERENCES question (id),
    FOREIGN KEY (answer_id) REFERENCES answer (id)
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
VALUES (1, 1493398154.0, 4, 'You need to use brackets: my_list = []', NULL),

       (2, 1493088154.0, 35, 'Look it up in the Python docs', NULL),

       (3, 1658935457.113151, -7, 'You need to do something', NULL),

       (4, 1659038513.407616, 3,
        'You forgot to provide example code and context!,/static/upload\76-765183_cute-cat-stickers-series-cute-angry-cat-cartoon.png',
        NULL);


INSERT INTO question_answer
VALUES (3, 1),
       (3, 2),
       (2, 3),
       (4, 4);
