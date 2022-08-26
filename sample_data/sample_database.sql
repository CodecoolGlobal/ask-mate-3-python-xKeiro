DROP TABLE IF EXISTS question CASCADE;
DROP TABLE IF EXISTS answer CASCADE;
DROP TABLE IF EXISTS comment CASCADE;
DROP TABLE IF EXISTS tag CASCADE;
DROP TABLE IF EXISTS question_tag CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS user_question CASCADE;
DROP TABLE IF EXISTS user_answer CASCADE;
DROP TABLE IF EXISTS user_comment CASCADE;

CREATE TABLE "user"
(
    id                SERIAL PRIMARY KEY,
    username          VARCHAR(25)                 NOT NULL UNIQUE,
    email             VARCHAR(25)                 NOT NULL UNIQUE,
    password          VARCHAR                     NOT NULL,
    registration_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT LOCALTIMESTAMP(0),
    reputation        INTEGER                     NOT NULL DEFAULT 0,
    CHECK (LENGTH(username) >= 5),
    CHECK (LENGTH(email) >= 5),
    CHECK (LENGTH(password) >= 5)
);

CREATE TABLE question
(
    id              SERIAL PRIMARY KEY,
    submission_time TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT LOCALTIMESTAMP(0),
    view_count      INTEGER                     NOT NULL DEFAULT 0,
    vote_count      INTEGER                     NOT NULL DEFAULT 0,
    title           VARCHAR(150)                NOT NULL,
    message         TEXT                        NOT NULL,
    image           VARCHAR(255),
    edit_count      INTEGER                     NOT NULL DEFAULT 0,
    user_id         INTEGER                     NOT NULL,
    CHECK (LENGTH(title) >= 5),
    CHECK (LENGTH(message) >= 5),
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE
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
    accepted        BOOLEAN                     NOT NULL DEFAULT FALSE,
    user_id         INTEGER                     NOT NULL,
    CHECK (LENGTH(message) >= 5),
    FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE TABLE comment
(
    id                SERIAL PRIMARY KEY,
    parent_comment_id INTEGER,
    answer_id         INTEGER                     NOT NULL,
    vote_count        INTEGER                     NOT NULL DEFAULT 0,
    message           TEXT                        NOT NULL,
    submission_time   TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT LOCALTIMESTAMP(0),
    edit_count        INTEGER                     NOT NULL DEFAULT 0,
    user_id           INTEGER                     NOT NULL,
    CHECK (LENGTH(message) >= 5),
    FOREIGN KEY (answer_id) REFERENCES answer (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

CREATE TABLE tag
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(25) NOT NULL
);

CREATE TABLE question_tag
(
    question_id INTEGER NOT NULL,
    tag_id      INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag (id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, tag_id)
);



CREATE TABLE user_question
(
    user_id     INTEGER,
    question_id INTEGER UNIQUE,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question (id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, question_id)
);

CREATE TABLE user_answer
(
    user_id   INTEGER,
    answer_id INTEGER UNIQUE,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
    FOREIGN KEY (answer_id) REFERENCES answer (id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, answer_id)
);

CREATE TABLE user_comment
(
    user_id    INTEGER,
    comment_id INTEGER UNIQUE,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comment (id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, comment_id)
);

INSERT INTO "user"(username, email, password, registration_date, reputation)
VALUES ('JohnyChef', 'john@mail.com', 'apple', '2022-08-14 15:14:55', 5),
       ('Harry', 'harry@mail.com', 'banana', '2022-08-14 15:14:55', 4),
       ('BestCook50', 'emil_s@mail.com', 'asdasd', '2022-08-15 15:14:55', 0),
       ('Elizabeth', 'bella@mail.com', 'broccoli', '2022-08-14 15:14:55', 0);

INSERT INTO question(submission_time, view_count, vote_count, title, message, image, edit_count, user_id)
VALUES ('2022-08-11 15:15:55', 4, 0, 'Pesto for pasta', 'Which kind of pesto should I try firstly?',
        NULL, 0, 1),
       ('2022-08-12 12:17:55', 15, 2, 'Burrito',
        'Can I make burrito at home? I do not know how to roll it...',
        NULL, 0, 2),
       ('2022-08-11 21:19:55', 11, 5, 'Hungarian Potato Paprika',
        'Has anyone tried it? Is it good?', NULL, 0, 3),
       ('2022-08-11 22:14:55', 12, 6, 'Chocolate Cake',
        'How can I make a chocolate cake like this?',
        '/static/upload\chocolate_cake.jpg', 0, 4);

INSERT INTO answer(submission_time, vote_count, question_id, message, image, accepted, user_id)
VALUES ('2022-08-11 15:14:55', 0, 2, 'Yes, you can! I made these:',
        '/static/upload\burrito.jpg', False, 1),
       ('2022-08-11 15:15:01', 1, 2, 'Burrito at home? Just go to a mexican restaurant! ',
        '/static/upload\areyouserious.jpg', False, 2),
       ('2022-08-11 15:18:23', 3, 3, 'Good! Try to make at home or travel to Hungary to taste it!',
        '/static/upload\paprikas-krumpli2.jpg',True, 3),
       ('2022-08-11 16:25:29', 4, 3, 'Yes, very tasty! ', NULL, False, 4),
       ('2022-08-11 17:48:39', 5, 4, 'Try this filling: whisk together sugar, flour, salt, half & half and egg yolks until smooth.', NULL, True, 1),
       ('2022-08-11 19:25:48', 4, 4, 'It is similar to mine cake, do you want the recipe ? ',
        '/static/upload\cake.jpg', False, 2),
       (' 2022-08-11 20:15:45', 2, 1, 'Try green basil pesto: basil, olive oil, Parmesan cheese, some nuts.', NULL, False, 3),
       (' 2022-08-11 21:14:32', 1, 1, 'Red pesto is sweeter ! The main ingredient is dried tomato.', NULL, False, 4),
       (' 2022-08-11 22:22:22', 0, 1, 'For a healthy option broccoli pesto is also a good one.', NULL, False, 1);

INSERT INTO comment (parent_comment_id, answer_id, message, submission_time, edit_count, user_id)
VALUES (NULL, 1, 'Looks delicious, please give me the recipe! ', '2022-08-12 14:11:25', 0, 1),
       (1, 1, 'Me too! ', '2022-08-12 17:12:35', 0, 2),
       (NULL, 3, 'Looks very good! ', '2022-08-13 15:16:45', 0, 3),
       (NULL, 6, 'Looks amazing! ', '2022-08-14 15:14:55', 0, 4),
       (4, 6, 'Makes me hungry! ', '2022-08-14 15:14:55', 0, 1);

INSERT INTO tag(name)
VALUES ('Cooking'),
       ('Italian'),
       ('Desserts'),
       ('Mexican');

INSERT INTO question_tag(question_id, tag_id)
VALUES (2, 4),
       (3, 1),
       (4, 3),
       (1, 2);



INSERT INTO user_question(user_id, question_id)
VALUES (1, 1),
       (2, 2),
       (3, 3),
       (4, 4);


INSERT INTO user_answer(user_id, answer_id)
VALUES (1, 1),
       (2, 2),
       (3, 3),
       (4, 4),
       (1, 5),
       (2, 6),
       (3, 7),
       (4, 8),
       (1, 9);



INSERT INTO user_comment(user_id, comment_id)
VALUES (1, 1),
       (2, 2),
       (3, 3),
       (4, 4),
       (1, 5);
