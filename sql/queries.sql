-- 데이터베이스 선택
USE library_db;

-- =====================================
-- 1. 기본 조회
-- =====================================

-- 전체 사용자 조회
SELECT * FROM users;

-- 전체 도서 조회
SELECT * FROM book;

-- =====================================
-- 2. 조건 조회 (WHERE)
-- =====================================

-- 남은 책이 있는 도서
SELECT title, remaining_copies
FROM book
WHERE remaining_copies > 0;

-- 특정 카테고리 도서
SELECT title, category
FROM book
WHERE category = 'Science';

-- =====================================
-- 3. JOIN (핵심)
-- =====================================

-- 누가 어떤 책을 빌렸는지
SELECT u.name AS user_name, b.title AS book_title, bl.loan_date
FROM book_loan bl
JOIN users u ON bl.user_id = u.user_id
JOIN book b ON bl.book_id = b.book_id;

-- 책 + 책장 + 방 정보
SELECT b.title, bs.category AS shelf_category, r.room_name
FROM book b
JOIN bookshelf bs ON b.bookshelf_id = bs.bookshelf_id
JOIN room r ON bs.room_id = r.room_id;

-- 책 + 담당 사서
SELECT b.title, l.name AS librarian_name
FROM book b
JOIN librarian l ON b.librarian_id = l.librarian_id;

-- =====================================
-- 4. JOIN + WHERE
-- =====================================

-- 특정 사용자가 빌린 책
SELECT u.name, b.title
FROM book_loan bl
JOIN users u ON bl.user_id = u.user_id
JOIN book b ON bl.book_id = b.book_id
WHERE u.name = 'Alice Johnson';

-- 아직 반납하지 않은 책
SELECT u.name, b.title, bl.loan_date
FROM book_loan bl
JOIN users u ON bl.user_id = u.user_id
JOIN book b ON bl.book_id = b.book_id
WHERE bl.return_date IS NULL;

-- =====================================
-- 5. GROUP BY (집계)
-- =====================================

-- 사용자별 대출 횟수
SELECT u.name, COUNT(*) AS loan_count
FROM book_loan bl
JOIN users u ON bl.user_id = u.user_id
GROUP BY u.name;

-- 카테고리별 도서 수
SELECT category, COUNT(*) AS book_count
FROM book
GROUP BY category;

-- =====================================
-- 6. ORDER BY (정렬)
-- =====================================

-- 대출 횟수 많은 순
SELECT u.name, COUNT(*) AS loan_count
FROM book_loan bl
JOIN users u ON bl.user_id = u.user_id
GROUP BY u.name
ORDER BY loan_count DESC;