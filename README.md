# Django OTP Authentication API

A RESTful API for user registration using email-based One-Time Password (OTP) verification, built with **Python, Django, and Django REST Framework**.

This project provides a simple registration workflow in which users request a six-digit OTP, verify the code, and create an account using their email address and password.

## Overview

The API implements an email-based OTP registration system with the following workflow:

1. A user submits their email address to request an OTP.
2. The system generates a secure six-digit verification code.
3. The OTP is stored in the database with a creation timestamp.
4. The user submits their email, full name, password, and OTP.
5. The API validates the OTP and checks whether it has expired or already been used.
6. If validation succeeds, a new user account is created.

**Note:** Actual email delivery has not yet been implemented. In the current development version, the generated OTP is returned directly in the API response.

## Features

- Email-based user registration
- Six-digit OTP generation using Python's `secrets` module
- Two-minute OTP expiration
- OTP verification before account creation
- Prevention of duplicate email registration
- Password validation using Django's built-in password validators
- Automatic invalidation of previously active OTP records when requesting a new code
- Django ORM integration
- RESTful API endpoints
- Structured API responses and validation errors

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST API development |
| SQLite | Database |
| Django ORM | Database operations |
| Python Secrets | Secure OTP generation |

## Project Structure

```text
otp_django/
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── user/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── manage.py
└── requirements.txt
```

## Getting Started

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd otp_django
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Documentation

The project currently provides two main endpoints.

### 1. Request OTP

Generates a six-digit OTP for the submitted email address.

**Endpoint:**

```http
POST /api/user/send-otp/
```

**Request Body:**

```json
{
    "email": "user@example.com"
}
```

**Successful Response (201 Created):**

```json
{
    "message": "OTP با موفقیت ساخته شد.",
    "otp": "123456"
}
```

**Validation:**

- The email must be valid.
- The email must not already belong to a registered user.
- Previous unused OTP records for the same email are deleted before generating a new code.

**Important:** The OTP is currently included in the response for development and testing purposes. It must not be exposed through public API responses in a production environment.

### 2. Register User

Verifies the OTP and creates a new user account.

**Endpoint:**

```http
POST /api/user/register/
```

**Request Body:**

```json
{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "YourStrongPassword123!",
    "otp": "123456"
}
```

**Successful Response (201 Created):**

```json
{
    "success": true,
    "message": "ثبت‌نام با موفقیت انجام شد.",
    "data": {
        "id": 1,
        "email": "user@example.com",
        "full_name": "John Doe",
        "date_joined": "2026-08-06T15:30:00Z"
    }
}
```

**Validation Rules:**

- The email must not already be registered.
- The full name is required.
- The password must satisfy Django's configured password validators.
- The OTP must contain exactly six numeric digits.
- The OTP must exist in the database.
- The OTP must not have expired.
- The OTP must not have been used previously.

After successful registration, the OTP is marked as used.

## OTP Lifecycle

The current OTP implementation follows this lifecycle:

```text
User submits email
       |
       v
Validate email
       |
       v
Delete previous unused OTPs
       |
       v
Generate six-digit OTP
       |
       v
Save OTP in database
       |
       v
Return OTP in API response
       |
       v
User submits registration data
       |
       v
Validate OTP
       |
       +---- Invalid / Expired
       |          |
       |          v
       |     Return validation error
       |
       v
Create user account
       |
       v
Mark OTP as used
       |
       v
Registration successful
```

## Database Model

The project uses a custom `OTP` model to manage verification codes.

| Field | Type | Description |
|---|---|---|
| id | BigAutoField | Primary key |
| email | EmailField | User email address |
| code | CharField | Six-digit OTP |
| created_at | DateTimeField | OTP creation timestamp |
| is_used | BooleanField | Indicates whether the OTP has been used |

### OTP Expiration

Each OTP has a validity period of two minutes.

The expiration status is calculated using the `is_expired()` method in the OTP model.

## Error Handling

The API uses Django REST Framework serializers for input validation.

Depending on the request, validation errors may include:

- Invalid email address
- Email already registered
- Missing OTP
- Incorrect OTP
- Expired OTP
- Invalid OTP format
- Password validation failure

Validation errors are returned using Django REST Framework's standard HTTP 400 response format.

## Current Limitations

This repository represents a development-stage implementation. The following features have not yet been implemented:

- Actual email delivery through an SMTP or email service provider
- Rate limiting for OTP requests
- Maximum OTP verification attempts
- OTP hashing before database storage
- Production-ready environment variable configuration
- Production database configuration
- Automated test coverage
- API documentation using Swagger or OpenAPI
- Authentication tokens and login endpoints

## Future Improvements

Potential improvements for future versions include:

- Integrating an email service for OTP delivery
- Implementing JWT authentication
- Adding login and password recovery endpoints
- Improving OTP security and lifecycle management
- Implementing request throttling
- Adding automated unit and integration tests
- Supporting PostgreSQL
- Improving production deployment configuration

## Development Status

**Status:** Initial implementation / Development

This project is intended as a backend learning and development project focused on Django REST Framework, serializers, database models, OTP verification, and user registration workflows.

## License

No license has been specified for this repository yet.
