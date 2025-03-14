# FastAPI User-Order API

## Overview
This is a FastAPI-based user and order management system with JWT authentication. It supports role-based access control (Admin & Customer) and follows best practices with database migrations, middleware, and structured project organization.

---

## Features
- **User Authentication:** Secure JWT-based authentication.
- **Role-Based Access Control:** Admins can manage users and orders; customers can manage their own profile and orders.
- **Database:** PostgreSQL with SQLAlchemy ORM.
- **Dockerized Environment:** Runs in a containerized setup.
- **Git Flow Workflow:** Follows a structured development approach.

---

## Project Structure
```
app/
├── auth/            # Authentication, JWT helpers, middleware
│   ├── auth.py
│   ├── key_manager.py
│   ├── middleware.py
├── db/              # Database connection
│   ├── database.py
├── models/          # SQLAlchemy models
│   ├── user.py
│   ├── order.py
├── routes/          # API endpoints
│   ├── auth.py
│   ├── users.py
│   ├── orders.py
├── schemas/
│   ├── order.py
│   ├── user.py
├── main.py          # FastAPI application entry point
│
├── migrations/      # Alembic migrations
├── Dockerfile       # Docker configuration
├── .env             # Environment variables
├── .gitignore       # Git ignore rules
├── README.md        # Project documentation
```

---

## Setup & Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/jawadshahid07/fastapi-user-order-api.git
cd fastapi-user-order-api
```

### 2️⃣ Create & Configure Environment Variables
Configure:
```sh
DATABASE_URL= <url>
ACCESS_TOKEN_EXPIRE_MINUTES= <time-in-minutes>
ALGORITHM= <algorithm-choice>
```
Update `.env` with your database connection.

### 3️⃣ Install Dependencies
#### Using Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

### 4️⃣ Run Database Migrations
```sh
alembic upgrade head
```
Note that postgreSQL is used for this application.

### 5️⃣ Start the Server
#### Using Uvicorn (Local Development)
```sh
uvicorn app.main:app --reload
```

Server will be running at: `http://127.0.0.1:8000`

---

## API Documentation
FastAPI automatically generates interactive API docs:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Usage
### 🔐 Authentication
#### Register a User
```http
POST /auth/register
```
**Request Body:**
```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Login & Get JWT Token
```http
POST /auth/login
```
**Response:**
```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```
Use this token in API requests as an `Authorization` header:
```http
Authorization: Bearer your_jwt_token
```

### 📌 Users API
#### Get Current User Profile
```http
GET /users/me
```

#### Get All Users (Admin Only)
```http
GET /users
```

#### Update Current User Profile
```http
PUT /users/me
```
**Request Body:**
```json
{
  "username": "newname",
  "email": "new@example.com"
}
```

### 🛒 Orders API
#### Create an Order
```http
POST /orders
```
**Request Body:**
```json
{
  "total_amount": 100.00
}
```

#### Get Order Details (Admin or Order Owner Only)
```http
GET /orders/{order_id}
```

#### List All Orders (Admin Only)
```http
GET /orders
```

#### Delete an Order (Admin or Order Owner)
```http
DELETE /orders/{order_id}
```

---

## Deployment
#### Deploy with Docker
```sh
docker-compose -f docker-compose.prod.yml up --build -d
```

#### Deploy with Gunicorn (Production)
```sh
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

---

## Contributing
1. Clone the repo & create a new feature branch:
```sh
git checkout -b feature/your-feature
```
2. Commit changes & push:
```sh
git commit -m "Added new feature"
git push origin feature/your-feature
```
3. Open a pull request!

---