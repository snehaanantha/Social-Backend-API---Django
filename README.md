# 🧑‍🧑 Social Backend API

This is a Django REST Framework-based backend for a social networking application. It includes features like user authentication, friend requests, and friendships.

---

## 📂 Project Structure

```
social_backend/
├── users/                      # Custom user model and logic
├── friend_request/           # Friend request and friendship logic
├── social_backend/            # Main Django project settings
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd social-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Setup

Create a database named `social_backend` and update your `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_backend',
        'USER': 'postgres',
        'PASSWORD': '<your-password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Add a secret key

In `settings.py`, add:

```python
SECRET_KEY = 'your-secret-key'
```

You can generate one using:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

## 🏐 API Overview

| Endpoint                        | Method | Description                         |
|----------------------------------|--------|-------------------------------------|
| `/api/auth/register/`            | POST   | Register the user                  |
| `/api/auth/login/`               | POST   | Login the user                     |
| `/api/friends/send/`            | POST   | Send a friend request              |
| `/api/friends/respond/`         | POST   | Respond to a friend request (accept/reject) |
| `/api/friends/get_list/`        | GET    | Get a list of friends               |
| `/api/friends/suggestions/`     | GET    | Get friend suggestions              |
| `/api/auth/register/profile/`   | GET    | Get the logged-in user's profile    |
| `/api/auth/register/list/`      | GET    | Get a list of all users excluding the logged-in user |
| `/api/auth/refresh/`             | POST   | Get a new access token using the refresh token |

### Details

1. **Register a User**
    - **Endpoint**: `/api/auth/register/`
    - **Method**: `POST`
    - **Request Body**:
    ```json
    {
      "username": "username",
      "password": "password123",
      "email": "email@example.com"
    }
    ```

2. **Login a User**
    - **Endpoint**: `/api/auth/login/`
    - **Method**: `POST`
    - **Request Body**:
    ```json
    {
      "username": "username",
      "password": "password123"
    }
    ```

3. **Send Friend Request**
    - **Endpoint**: `/api/friends/send/`
    - **Method**: `POST`
    - **Authorization**: Bearer Token (`Authorization: Bearer <JWT_TOKEN>`)
    - **Request Body**:
    ```json
    {
      "to_user": 3
    }
    ```

4. **Respond to Friend Request**
    - **Endpoint**: `/api/friends/respond/`
    - **Method**: `POST`
    - **Authorization**: Bearer Token (`Authorization: Bearer <JWT_TOKEN>`)
    - **Request Body**:
    ```json
    {
      "request_id": 1,
      "action": "accept"  // or "reject"
    }
    ```

5. **Get a List of Friends**
    - **Endpoint**: `/api/friends/get_list/`
    - **Method**: `GET`
    - **Authorization**: Bearer Token (`Authorization: Bearer <JWT_TOKEN>`)

6. **Get Friend Suggestions**
    - **Endpoint**: `/api/friends/suggestions/`
    - **Method**: `GET`
    - **Authorization**: Bearer Token (`Authorization: Bearer <JWT_TOKEN>`)

7. **Get User Profile**
    - **Endpoint**: `/api/auth/register/profile/`
    - **Method**: `GET`
    - **Authorization**: Bearer Token (`Authorization: Bearer <JWT_TOKEN>`)

8. **Get All Users (Excluding Self)**
    - **Endpoint**: `/api/auth/register/list/`
    - **Method**: `GET`
    - **Authorization**: Bearer Token (`Authorization: Bearer <JWT_TOKEN>`)

9. **Refresh Token**
    - **Endpoint**: `/api/auth/refresh/`
    - **Method**: `POST`
    - **Request Body**:
    ```json
    {
      "refresh": "<refresh_token>"
    }
    ```
    - **Response**:
    ```json
    {
      "access": "<new_access_token>"
    }
    ```


## 🎓 Tech Stack

- Python 3.11+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Simple JWT

---

## 🚫 Troubleshooting

If you encounter any issues:

- Make sure PostgreSQL is running
- Ensure you’ve activated the correct virtual environment
- Check that `SECRET_KEY` is not empty
- If overriding the User model, ensure it is configured in `AUTH_USER_MODEL`

---

