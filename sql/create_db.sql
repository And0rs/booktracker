--============================
--  Создание таблиц
--============================
DROP TABLE IF EXISTS reading_statuses CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS users CASCADE;


CREATE TABLE IF NOT EXISTS users (
	id SERIAL NOT NULL,
	username VARCHAR(255) NOT NULL UNIQUE,
	email VARCHAR(255) NOT NULL UNIQUE,
	password_hash VARCHAR(255) NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE,
	created_at TIMESTAMP DEFAULT NOW(),
	PRIMARY KEY(id)
);




CREATE TABLE IF NOT EXISTS books (
	id SERIAL NOT NULL,
	title VARCHAR(255) NOT NULL,
	author_name VARCHAR(255) NOT NULL,
	year INTEGER,
	language VARCHAR(50),
	description TEXT,
	cover_url VARCHAR(500),
	added_by INTEGER,
	created_at TIMESTAMP DEFAULT NOW(),
	PRIMARY KEY(id)
);




CREATE TABLE IF NOT EXISTS reviews (
	id SERIAL NOT NULL,
	user_id INTEGER NOT NULL,
	book_id INTEGER NOT NULL,
	rating VARCHAR(20) CHECK(rating IN ('positive', 'negative', 'neutral')),
	text TEXT,
	created_at TIMESTAMP DEFAULT NOW(),
	UNIQUE(user_id, book_id),
	PRIMARY KEY(id)
);




CREATE TABLE IF NOT EXISTS reading_statuses (
	id SERIAL NOT NULL,
	user_id INTEGER NOT NULL,
	book_id INTEGER NOT NULL,
	status VARCHAR(20) NOT NULL CHECK(status IN ('want_to_read', 'reading', 'read')),
	updated_at TIMESTAMP DEFAULT NOW(),
	UNIQUE(user_id, book_id),
	PRIMARY KEY(id)
);



ALTER TABLE books
ADD FOREIGN KEY(added_by) REFERENCES users(id)
ON UPDATE NO ACTION ON DELETE SET NULL;

ALTER TABLE reviews
ADD FOREIGN KEY(user_id) REFERENCES users(id)
ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE reviews
ADD FOREIGN KEY(book_id) REFERENCES books(id)
ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE reading_statuses
ADD FOREIGN KEY(user_id) REFERENCES users(id)
ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE reading_statuses
ADD FOREIGN KEY(book_id) REFERENCES books(id)
ON UPDATE NO ACTION ON DELETE CASCADE;


--============================
--  Тестовые данные
--============================

-- Пользователи
INSERT INTO users (username, email, password_hash, is_admin) VALUES
  ('example', 'example@example.com', 'scrypt:32768:8:1$o6Y3UWncBB08Br4E$561c453732fdcbda17f400d2669f24145404e76bb5d41168ad41a51157c70625aae11b7ffbb25471fc16a069c856ab769fd2f4a5b732663bfc6c9fe606443336', 'FALSE'),
  ('bob',   'bob@example.com',   'scrypt:32768:8:1$JRgyEovXIgGp6i0A$19547b12f087513c6bdf541f8c41b05ca02ce0eae3cdc45d3b508659800a46874361c64111ccd3d141c10776dfae8e7048c7a8031ef762e8965ee564dc7ae9cb', 'TRUE');
-- Книги
INSERT INTO books (title, author_name, year, language, description, added_by) VALUES
  ('Мастер и Маргарита',    'Михаил Булгаков',         1967, 'русский',   'Роман о дьяволе в Москве',       1),
  ('1984',                  'Джордж Оруэлл',           1949, 'английский', 'Роман-антиутопия',              1),
  ('Преступление и наказание', 'Фёдор Достоевский',   1866, 'русский',    'Роман о студенте Раскольникове', 2),
  ('Маленький принц',       'Антуан де Сент-Экзюпери', 1943, 'французский','Философская сказка',             2);
-- Рецензии
INSERT INTO reviews (user_id, book_id, rating, text) VALUES
  (1, 4, 'positive', 'Мы в ответе за тех, кого приручили'),
  (1, 2, 'neutral',  'Сводка новостей за вчерашний день'),
  (2, 3, 'positive', 'Прекрасно, чудесно, замечательно, великолепно'),
  (2, 1, 'negative', 'Лорем ипсум');
-- Статусы чтения
INSERT INTO reading_statuses (user_id, book_id, status) VALUES
  (1, 1, 'read'),
  (1, 2, 'reading'),
  (2, 3, 'want_to_read'),
  (2, 4, 'read');
  
  
--============================
--  Выполнение запросов (обёрнуто в rollback, для идемпонентности)
--============================

BEGIN;

-- 1. Поиск книг на русском языке
SELECT title, author_name, year FROM books WHERE language = 'русский';

-- 2. Добавление новой книги
INSERT INTO books (title, author_name, year, language, added_by)
VALUES ('Война и мир', 'Лев Толстой', 1869, 'русский', 1);

-- 3. Изменение статуса чтения
UPDATE reading_statuses SET status = 'read', updated_at = NOW()
WHERE user_id = 1 AND book_id = 2;

-- 4. Удаление рецензии
DELETE FROM reviews WHERE user_id = 2 AND book_id = 1;

-- 5. Поиск книг + имена авторов рецензий
SELECT b.title, u.username, r.rating, r.text
FROM reviews r
JOIN books b ON r.book_id = b.id
JOIN users u ON r.user_id = u.id
ORDER BY b.title;

ROLLBACK;
