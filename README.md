# Library Management System API

A simplified Library Management System API built with Django and Django REST Framework (DRF). This API enables users to perform CRUD operations on Books, Authors, and Borrowers while enforcing role-based authentication and permissions.

---

## Project Overview

This project allows users to:
- Manage **Authors**: Create, read, update, and delete authors. (Only staff and admin users are allowed to create, update, or delete.)
- Manage **Books**: Perform CRUD operations on books. (Book creation and updates are restricted to staff and admin users; all users can view books.)
- **Borrow Books**: Regular users can borrow books if available. A borrower cannot have more than 3 books borrowed at any time. Borrowing a book marks it as unavailable, and returning a book makes it available again.
- Authenticate using Django’s built-in authentication and JWT tokens, with role-based permissions:
  - **Admin:** Full access.
  - **Staff:** Can manage authors and books.
  - **Regular User:** Can borrow/return books but cannot manage authors or books.
- Validate data to ensure ISBN uniqueness and correct formatting, as well as enforce the borrowing limit.
- (Bonus) Provide additional features such as caching, search/filter endpoints, signals to update last borrowed dates, and proper error handling.

---

## Requirements

### Models
- **Author**
  - `name`
  - `bio`
- **Book**
  - `title`
  - `isbn` (must be unique and follow a valid ISBN format)
  - `author` (ForeignKey to Author)
  - `published_date`
  - `available` (Boolean indicating if the book is available for borrowing)
- **Borrower**
  - `user` (ForeignKey to Django's User model)
  - `books_borrowed` (ManyToManyField to Book, with a limit of 3 books at any given time)

### Views and API Endpoints

#### Authentication
- **POST** `/api/auth/register/` - Register a new user
- **POST** `/api/auth/login/` - Login and obtain JWT tokens

#### Author Management (Staff/Admin Only for Create/Update/Delete)
- **GET** `/api/authors/` - List all authors
- **POST** `/api/authors/create/` - Create a new author
- **GET** `/api/authors/<id>/` - Retrieve author details
- **PUT** `/api/authors/<id>/update/` - Update author details
- **DELETE** `/api/authors/<id>/delete/` - Delete an author

#### Book Management
- **GET** `/api/books/` - List all books (accessible to everyone)
- **POST** `/api/books/create/` - Create a new book (Staff/Admin only)
- **GET** `/api/books/<id>/` - Retrieve book details
- **PUT** `/api/books/<id>/update/` - Update book details (Staff/Admin only)
- **DELETE** `/api/books/<id>/delete/` - Delete a book (Staff/Admin only)

#### Borrowing Books
- **POST** `/api/books/borrow/` - Borrow a book (Regular users only; only if the book is available)
- **POST** `/api/books/return/` - Return a borrowed book (Regular users only)

#### Bonus Endpoints (Optional)
- **GET** `/api/search-filter/` - Search books by title and filter by author and availability
- **GET** `/api/library/statistics/` - Retrieve library statistics (Staff only)
- **GET** `/api/borrowers/` - List all borrowers (Staff only)

### Data Validation & Testing
- **Data Validation:**  
  - ISBN must be unique and valid.
  - Borrowers cannot exceed the limit of 3 books.
- **Unit Testing:**  
  - Validate that users cannot borrow more than 3 books.
  - Test permissions for CRUD operations on authors and books.
  - Test the borrowing and returning processes using Django’s `TestCase` or `pytest`.



## Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- **On Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
pythom manage.py makemigration
python manage.py migrate
```

### 6. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### 7. Run the Development Server
```bash
python manage.py runserver
```
The API will be available at **http://127.0.0.1:8000/api/**.

---

## Usage

- **Authentication:**  
  Use the `/api/auth/register/` and `/api/auth/login/` endpoints to create an account and obtain a JWT token.

- **Author & Book Management:**  
  CRUD operations for authors and books are available based on user role restrictions.

- **Borrowing Books:**  
  Regular users can borrow an available book via `/api/books/borrow/` and return it via `/api/books/return/`.

- **Bonus Features:**  
  Explore search, filtering, and statistics endpoints if implemented.

---

## Technologies Used
- **Python & Django**
- **Django REST Framework**
- **JWT for Authentication**
- **PostgreSQL/MySQL/SQLite** (configurable)
- Other libraries as specified in the `requirements.txt`

---

## Contributing

Contributions are welcome! To contribute:

1. **Fork the repository.**
2. **Create a new branch:**
   ```bash
   git checkout -b feature-branch
   ```
3. **Commit your changes:**
   ```bash
   git commit -m "Description of your changes"
   ```
4. **Push to your fork:**
   ```bash
   git push origin feature-branch
   ```
5. **Open a Pull Request** on GitHub.

---

## License

This project is licensed under the **MIT License**.

---

## Contact

For questions or support, please contact:
- **Email:** wahabkazim
- **GitHub:** [Wahab Kazim](https://github.com/wahab1)
