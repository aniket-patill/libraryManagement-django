# Library Management System

A Django-based REST API for managing users and books, allowing user registration, book registration, rental (disbursement), returns, authorization, and deletion. Data is stored in a MySQL database.

---

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Database Schema](#database-schema)
- [Environment Variables](#environment-variables)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [API Testing](#api-testing)
- [Troubleshooting](#troubleshooting)

---

## Features

- Register users (with password)
- Register books
- Authorize (login) users
- Rent/disburse books
- Return books
- Delete users (with password)
- Delete books
- Healthcheck endpoint

---

## Setup

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd library-management/myproject
   ```

2. **Install dependencies**
   ```sh
   pip install django mysql-connector-python python-dotenv
   ```

3. **Configure MySQL**
   - Create a database (e.g., `librarydb`)
   - Update `.env` file with your MySQL credentials:
     ```
     DB_HOST=localhost
     DB_USER=root
     DB_PASSWORD=yourpassword
     DB_NAME=librarydb
     ```

4. **Create tables**
   - Use the following SQL in your MySQL client:
     ```sql
     DROP TABLE IF EXISTS Rental;
     DROP TABLE IF EXISTS Book;
     DROP TABLE IF EXISTS User;

     CREATE TABLE User (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(100) NOT NULL,
         email VARCHAR(100) NOT NULL UNIQUE,
         password VARCHAR(255) NOT NULL,
         created_at DATETIME DEFAULT CURRENT_TIMESTAMP
     );

     CREATE TABLE Book (
         id INT AUTO_INCREMENT PRIMARY KEY,
         title VARCHAR(200) NOT NULL,
         author VARCHAR(100) NOT NULL,
         available BOOLEAN DEFAULT TRUE,
         created_at DATETIME DEFAULT CURRENT_TIMESTAMP
     );

     CREATE TABLE Rental (
         id INT AUTO_INCREMENT PRIMARY KEY,
         user_id INT NULL,
         book_id INT NULL,
         rented_at DATETIME DEFAULT CURRENT_TIMESTAMP,
         returned_at DATETIME DEFAULT NULL,
         FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE SET NULL,
         FOREIGN KEY (book_id) REFERENCES Book(id) ON DELETE SET NULL
     );
     ```

---

## Environment Variables

- Place your `.env` file in `myproject/` directory.
- Example:
  ```
  DB_HOST=localhost
  DB_USER=root
  DB_PASSWORD=yourpassword
  DB_NAME=librarydb
  ```

---

## Running the Server

```sh
python manage.py runserver
```
Server runs at `http://127.0.0.1:8000/`

---

## API Endpoints

| Endpoint                | Method | Description                          | Required Fields                |
|-------------------------|--------|--------------------------------------|--------------------------------|
| `/healthcheck/`         | GET    | Check DB connection                  | None                           |
| `/register-user/`       | POST   | Register a new user                  | name, email, password          |
| `/authorize-user/`      | POST   | Login/authorize user                 | email, password                |
| `/register-book/`       | POST   | Register a new book                  | title, author                  |
| `/book-disbursement/`   | POST   | Rent a book to a user                | user_name, user_email, book_title |
| `/return-book/`         | POST   | Return a rented book                 | user_name, user_email, book_title |
| `/delete-user/`         | POST   | Delete a user                        | user_name, user_email, password|
| `/delete-book/`         | POST   | Delete a book                        | book_title                     |

---

## API Testing

You can use [Postman](https://www.postman.com/) or `curl` for testing.

**In Postman:**  
- Select **Body** → **raw** → **JSON** for requests.
- Example JSON for each endpoint:

### Register User

```json
POST http://127.0.0.1:8000/register-user/
Body (raw, JSON):
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secret"
}
```

### Authorize User (Login)

```json
POST http://127.0.0.1:8000/authorize-user/
Body (raw, JSON):
{
  "email": "john@example.com",
  "password": "secret"
}
```

### Register Book

```json
POST http://127.0.0.1:8000/register-book/
Body (raw, JSON):
{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien"
}
```

### Book Disbursement (Rent)

```json
POST http://127.0.0.1:8000/book-disbursement/
Body (raw, JSON):
{
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "book_title": "The Hobbit"
}
```

### Return Book

```json
POST http://127.0.0.1:8000/return-book/
Body (raw, JSON):
{
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "book_title": "The Hobbit"
}
```

### Delete User

```json
POST http://127.0.0.1:8000/delete-user/
Body (raw, JSON):
{
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "password": "secret"
}
```

### Delete Book

```json
POST http://127.0.0.1:8000/delete-book/
Body (raw, JSON):
{
  "book_title": "The Hobbit"
}
```

**Note:**  
If you use `curl`, use `-H "Content-Type: application/json"` and `-d '{...}'` for JSON

## Author

Aniket Patil

---

## Notes

- Passwords are stored in plain text for demo purposes. For production, always hash passwords!
- Rentals are not deleted when users/books are deleted (see schema).
- For advanced features (pagination, search, etc.), extend the API as
