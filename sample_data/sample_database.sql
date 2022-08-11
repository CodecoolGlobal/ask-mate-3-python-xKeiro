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
    answer_id         INTEGER NOT NULL,
    vote_count      INTEGER                     NOT NULL DEFAULT 0,
    message           TEXT                        NOT NULL,
    submission_time   TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT LOCALTIMESTAMP(0),
    edit_count        INTEGER                     NOT NULL DEFAULT 0,
    FOREIGN KEY (answer_id) REFERENCES answer (id) ON DELETE CASCADE
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



INSERT INTO question(submission_time,view_count,vote_count,title,message,image,edit_count)
VALUES ('2022-08-11 15:15:55', 4,  0, 'Miből van a kenyér hélya? :D', 'Kenyírt szeretnékap stüni! Tudnátaok segíni?', NULL, 0),
	  ('2022-08-12 12:17:55', 15, 2, 'Földrajz érettségi', 'Sziasztok! Szerintetek, ha az érettségin a kifejtős kérdésre a paprikás krumpli receptjét írom le, akkor valahogy át lehet csusszani a vizsgán?', NULL, 0),
  	  ('2022-08-11 21:19:55', 11, 5, 'Paprikás krumpli ', 'Sziasztok! :) Tudna esetleg valaki  NorbiUpdate paprikás krumpli receptet ajánlani?', NULL, 0),
  	  ('2022-08-11 22:14:55', 12, 6, 'Valakinél vetési tarhonya eladó?', 'Sziasztok! Tudja valaki, hogy honnan tudnék vetési tarhonyát beszerezni? Szeretnék ültetni mert a család kifejezetten tarhonyával szereti a pörköltet.','/static/upload\tarhonya-elkeszitese-recept-foto.jpg', 0);

INSERT INTO answer(submission_time,vote_count,question_id,message,image)
VALUES ('2022-08-11 15:14:55', 0, 2, 'Persze, ha jó a recept akkor minden bizonnyal. xD', '/static/upload\paprikas-krumpli.jpg'),
	  ('2022-08-11 15:15:01', 1, 2, 'Te most magadtól vagy ennyire hülye, vagy valaki fogja a kezedet? O.o ', '/static/upload\areyouserious.jpg'),
	  ('2022-08-11 15:18:23', 3, 3, 'Persze, fél kilóval kevesebb zsírszalonnán pirítsd le a hagymát hozzá xDDD', '/static/upload\szalonna.jpg'),
	  ('2022-08-11 16:25:29', 4, 3, 'Budapesten tuti kapsz ötezerééééé :D ', NULL),
	  ('2022-08-11 17:48:39', 5, 4, 'Ezt most teljesen komolyan kérdezed? O.o xDD', NULL),
	  ('2022-08-11 19:25:48', 4, 4, 'Persze, milyen kiszerelésben kéne? Ez jó lesz?', '/static/upload\tarhonyavetomag.jpg'),
	  ('2022-08-11 20:15:45', 2, 1, 'héJa a kenyér kívülről sült héja. valamelyik fajta liszt felhasználából.', NULL),
 	  ('2022-08-11 21:14:32', 1, 1, '85% A könyér haja azér van hogy mögegyed, nem csak a belit köll zabáni.', NULL),
	  ('2022-08-11 22:22:22', 0, 1, 'Há héjjjamadárbó, mibő lenne.', NULL);

INSERT INTO comment (parent_comment_id, answer_id, message, submission_time,edit_count)
VALUES (NULL, 1, 'Yummii, ez tök jól néz ki. Linkelnéd a receptet légyszíves? :D ','2022-08-12 14:11:25', 0),
  	  (1, 1,'Google a barátod. :P ','2022-08-12 17:12:35',0),
 	  (NULL, 3, 'Fuuu, de jól néz ki tuti faluról van. ','2022-08-13 15:16:45', 0),
	  (NULL, 6,'Hát kicsit többre gondoltam úgy két mázsa kéne, annyid is van? ','2022-08-14 15:14:55', 0);

INSERT INTO tag(name)
VALUES ('Code'),
       ('Cooking'),
       ('Newbie');

INSERT INTO question_tag(question_id,tag_id)
VALUES (2,2),
   	  (3,2),
	  (4,2),
 	  (1,3);
