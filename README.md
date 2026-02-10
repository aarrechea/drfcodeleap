# DRF CodeLeap - Django REST Framework API

A robust REST API built with Django REST Framework, featuring JWT authentication, post management, and granular permission controls. Designed for scalability and secure content management.

## 🚀 Features

- **Authentication**: Secure JWT (JSON Web Token) authentication using `djangorestframework-simplejwt`.
  - Registration, Login, Token Refresh.
- **Post Management**: Full CRUD operations for posts.
- **Permissions**:
  - **Read Access**: Authenticated users can read all posts.
  - **Ownership Control**: Users can only update or delete their own posts.
  - **Safe Defaults**: Unauthenticated access is strictly limited to auth endpoints.
- **Pagination**: Cursor-based pagination for efficient data loading.
- **Filtering**: Filter posts by username.
- **Deployment Ready**: Configured for Heroku with `gunicorn`, `whitenoise`, and PostgreSQL.

## 🛠️ Tech Stack

- **Backend**: Python 3.13, Django 6.0
- **API**: Django REST Framework (DRF)
- **Database**: PostgreSQL (Production), SQLite (Dev)
- **Authentication**: JWT
- **Deployment**: Gunicorn, Whitenoise, Docker-ready structure

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aarrechea/drfcodeleap.git
   cd drfcodeleap
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get tokens
- `POST /api/auth/refresh/` - Refresh access token

### Posts
- `GET /api/post/` - List all posts (with pagination & filtering)
- `POST /api/post/` - Create a new post
- `GET /api/post/{id}/` - Retrieve a specific post
- `PATCH /api/post/{id}/` - Partially update a post (Owner only)
- `DELETE /api/post/{id}/` - Delete a post (Owner only)

## 🚀 Deployment

This project includes a `Procfile` and `runtime.txt` for easy deployment to Heroku.

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
