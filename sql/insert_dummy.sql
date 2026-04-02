SET NAMES utf8mb4;

DELETE FROM book_loan;
DELETE FROM book;
DELETE FROM bookshelf;
DELETE FROM room;
DELETE FROM users;
DELETE FROM librarian;

ALTER TABLE book_loan AUTO_INCREMENT = 1;
ALTER TABLE book AUTO_INCREMENT = 1;
ALTER TABLE bookshelf AUTO_INCREMENT = 1;
ALTER TABLE room AUTO_INCREMENT = 1;
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE librarian AUTO_INCREMENT = 1;

INSERT INTO librarian (name, phone, email) VALUES
('John Smith', '010-1111-1111', 'john.smith@test.com'),
('Emily Brown', '010-2222-2222', 'emily.brown@test.com');

INSERT INTO users (name, email, phone) VALUES
('Alice Johnson', 'user1@test.com', '010-3333-3333'),
('Michael Lee', 'user2@test.com', '010-4444-4444');

INSERT INTO room (room_name, librarian_id) VALUES
('Reading Room A', 1),
('Reading Room B', 2);

INSERT INTO bookshelf (category, room_id) VALUES
('Fiction', 1),
('Science', 1),
('History', 2);

INSERT INTO book (title, author, publisher, category, total_copies, remaining_copies, librarian_id, bookshelf_id) VALUES
('Harry Potter', 'J.K. Rowling', 'Bloomsbury', 'Fiction', 5, 5, 1, 1),
('Cosmos', 'Carl Sagan', 'Random House', 'Science', 3, 2, 1, 2),
('The History of Korea', 'Kim Writer', 'History Press', 'History', 4, 4, 2, 3);

INSERT INTO book_loan (book_id, user_id, loan_date, return_date) VALUES
(1, 1, '2026-04-01', NULL),
(2, 2, '2026-04-01', '2026-04-05');