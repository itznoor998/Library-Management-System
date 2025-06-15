# 📚 Library Management System

**Modern Application Development - I Project**  


A multi-user web application built to manage e-books, users, and librarians in a virtual library. Users can request and read e-books, while librarians manage book inventory, user access, and content. Built entirely with Flask, Jinja2, SQLite, and Bootstrap — no external servers required.

---

## 🚀 Project Overview

This Library Management System supports:

- **Librarian (Admin)** and **General User (Student)** roles
- Issuing and returning e-books
- Section-based categorization of books
- Feedback system
- Book borrowing limits and auto-revoke system

---

## 🧱 Tech Stack

| Layer        | Technology             |
|--------------|------------------------|
| Backend      | Flask                  |
| Templates    | Jinja2    |
| Database     | SQLite (Local Storage) |
| Frontend     | HTML/CSS    |

> ✅ All demos run locally without the need for any external database or frontend build tools.


---

## 👥 User Roles

### 🧑‍🎓 General User (Student)

- Register/Login
- View available **Sections** and **e-Books**
- Request and return up to **5 e-books**
- Borrow duration configurable (e.g., 7 days)
- Leave feedback for books
- Auto-revoke of access after borrowing period

### 🧑‍💼 Librarian (Admin)

- Separate login interface
- Add/edit/delete **Sections** and **e-Books**
- Issue or revoke access to books
- Assign books to sections
- View book status (issued/available) and borrowing users

---

## 📘 Core Functionalities

### ✅ Auth & Roles

- Separate login forms for Librarians and Users
- Role-based view rendering
- Basic session management (not production-secure)

### 📚 Book Management

- Add, edit, or remove e-books
- Assign to a section
- Handle UTF-8 encoded content (multi-language supported)
- View book status (available/issued)

### 🗂️ Section Management

- Add new sections
- Edit or delete sections
- Associate books with sections

### 🔍 Search Functionality

- Search for e-books by:
  - Section
  - Author
  - Name/title

- Search for sections by name

### 🔁 Book Borrowing Rules

- Max 5 active books per user
- Access is time-limited (e.g., N = 7 days)
- Access auto-revoked after N days if not returned

---

## 🧪 Demo Instructions

### Prerequisites
- Python 3.8+
- Any local IDE (e.g., VS Code)

### Install Dependencies
```windows powershell

pip install -r requirements.txt

```

### Additional Insttructions

1. Run the command `python app.py` in power shell to run the App
2. Open `http://127.0.0.1:5000/` in your browser