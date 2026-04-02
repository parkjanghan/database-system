CREATE TABLE librarian (
    librarian_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL, 
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL
);

CREATE TABLE room (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_name VARCHAR(50) NOT NULL,
    librarian_id INT UNIQUE,
    FOREIGN KEY (librarian_id) REFERENCES librarian(librarian_id)
);

CREATE TABLE bookshelf (
    bookshelf_id INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(50),
    room_id INT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE TABLE book (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    category VARCHAR(50),
    total_copies INT NOT NULL,
    remaining_copies INT NOT NULL,

    CHECK (total_copies >= 0),
    CHECK (remaining_copies >= 0),
    CHECK (remaining_copies <= total_copies),

    librarian_id INT,
    bookshelf_id INT,
    FOREIGN KEY (librarian_id) REFERENCES librarian(librarian_id),
    FOREIGN KEY (bookshelf_id) REFERENCES bookshelf(bookshelf_id)
);

CREATE TABLE book_loan (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    user_id INT NOT NULL,
    loan_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);