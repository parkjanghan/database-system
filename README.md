# 📚 Library Management System (RDB Project)

## 1. 프로젝트 개요

본 프로젝트는 관계형 데이터베이스(RDB)를 기반으로 한 **도서관 관리 시스템**을 구현하는 것을 목표로 합니다.
주요 목적은 ER 스키마를 설계하고 이를 MySQL 데이터베이스로 변환한 뒤, Python(PyMySQL)을 활용하여 데이터베이스를 조작하는 것입니다.

본 시스템은 다음과 같은 기능을 제공합니다:

* 도서(Book) 관리
* 사용자(User) 관리
* 대출(Book Loan) 관리
* CRUD(Create, Read, Update, Delete) 기능 구현
* CLI 기반 인터페이스 제공

---

## 2. 기술 스택

* **Database**: MySQL (Docker)
* **Backend**: Python
* **Library**: PyMySQL
* **Environment**: Python venv
* **Containerization**: Docker Compose

---

## 3. 프로젝트 구조

```
library-management/
├── compose.yaml
├── .env
├── .gitignore
├── requirements.txt
├── main.py
├── db/
│   ├── connection.py
│   ├── schema.py
│   └── seed.py
├── services/
│   ├── user_service.py
│   ├── book_service.py
│   └── loan_service.py
└── README.md
```

---

## 4. 데이터베이스 설계

### 주요 엔티티

* BOOK
* USER
* LIBRARIAN
* BOOK_LOAN
* ROOM
* BOOKSHELF

### 주요 관계

* 한 USER는 여러 BOOK을 대출할 수 있음
* 한 BOOK은 여러 번 대출될 수 있음
* BOOK_LOAN을 통해 USER와 BOOK 관계를 관리
* 한 LIBRARIAN은 여러 BOOK을 관리
* ROOM은 LIBRARIAN과 연결됨

---

## 5. 주요 기능

### 1. 데이터베이스 초기화

* 테이블 생성 (DDL)
* Primary Key / Foreign Key 설정

### 2. 더미 데이터 삽입

* 각 테이블에 5~10개의 테스트 데이터 삽입

### 3. CRUD 기능

#### USER

* 사용자 생성
* 사용자 조회
* 사용자 수정
* 사용자 삭제

#### BOOK

* 도서 등록
* 도서 조회
* 도서 수정
* 도서 삭제

#### BOOK_LOAN

* 도서 대출
* 도서 반납
* 대출 기록 조회

---

## 6. 핵심 비즈니스 로직

### 📌 도서 대출

* 사용자는 최대 3권까지 대출 가능
* 책의 remaining_copies가 0이면 대출 불가
* 대출 시 remaining_copies 감소

### 📌 도서 반납

* return_date가 NULL인 경우만 반납 가능
* 반납 시 remaining_copies 증가

---

## 7. 실행 방법

### 1. Docker 실행 (MySQL 서버 시작)

```bash
docker compose up -d
```

---

### 2. Python 가상환경 설정

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 3. 프로그램 실행

```bash
python main.py
```

---

## 8. 환경 변수 설정 (.env)

```env
# Python DB connection
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=library_db
DB_PORT=3306

# Docker MySQL
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=library_db
```

---

## 9. 요구사항 반영 내용

* ER 스키마 기반 관계형 DB 설계
* 모든 테이블 DDL 작성
* Primary Key / Foreign Key 설정
* 더미 데이터 삽입
* USER / BOOK / BOOK_LOAN CRUD 구현
* CLI 기반 프로그램 구성
* Python(PyMySQL) 사용

---

## 10. 실행 예시

```
1. Create User
2. View Users
3. Add Book
4. View Books
5. Loan Book
6. Return Book
0. Exit
```

---

## 11. 주의사항

* `.env` 파일은 Git에 포함되지 않음
* Docker 실행 후 DB가 완전히 올라올 때까지 잠시 대기 필요
* 포트 충돌 시 compose.yaml에서 포트 변경 필요

---

## 12. 향후 개선 방향

* GUI 인터페이스 추가
* 인증/로그인 기능 추가
* 카테고리 테이블 분리
* 트랜잭션 처리 강화
