# Django Blogging Platform

A full-stack blogging application built with Django featuring role-based access control (RBAC), post management (CRUD), comments with moderation, tagging, search, and engagement metrics.

## Demo Video


## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Local Setup](#local-setup)
- [Running the Server](#running-the-server)
- [Tests](#tests)
- [Environment Variables](#environment-variables)
- [Usage Guide (Roles)](#usage-guide-roles)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
This project is a system-design style assignment implementing a blogging platform with role-based permissions. It supports Admin, Author, and Reader roles. Authors can manage their own posts; Admins manage the system and moderate comments; Readers can view, search, like, and comment (comments require admin approval).

## Features
- Authentication
  - Role-Based Access: Admin, Author, Reader
  - Secure registration & login
  - Role-specific permissions
- Blog Management
  - Create / Edit / Delete posts
  - Draft vs Published states
  - Tagging system (Many-to-Many)
- Interactions
  - Comments with moderation (Admin approval required)
  - Like/unlike toggle for posts
  - Share links (WhatsApp, LinkedIn, Email)
- Discovery & Analytics
  - Keyword search (Title & Tags)
  - View counters for analytics

## Tech Stack
- Backend: Python 3.11+, Django 5.x
- Database: SQLite (default for local development)
- Frontend: HTML5, Bootstrap 5
- Testing: Django `TestCase` (unit tests)

## Local Setup

1. Clone the repository
```bash
git clone https://github.com/Abhishek2634/Blogger.git
cd Blogger
```

2. Create a virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply database migrations
```bash
python manage.py makemigrations users blog
python manage.py migrate
```

5. Create a superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

6. Run the development server
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser.

## Running Tests
Run the unit tests for the blog app:
```bash
python manage.py test blog.tests  
```
Expected output (example):
```
Found 5 test(s).
Creating test database for alias 'default'...
.....
Ran 5 tests in 0.023s

OK
```

## Environment Variables
For local development the project defaults to DEBUG=True and SQLite and doesn't strictly require a `.env`. For production, you should set:
- `SECRET_KEY` — your Django secret key
- `DEBUG` — set to `False`
- `ALLOWED_HOSTS` — e.g. `['your-domain.com']`

You can load env vars with your preferred method (django-environ, python-decouple, etc.).

## Usage Guide (Roles)

- Admin
  - Login at `/admin/` or via the app login.
  - Approve or reject comments, manage users, create tags, and delete any post.

- Author
  - Sign up or be assigned the Author role.
  - Create, edit, and delete only your posts.
  - Save drafts or publish posts.

- Reader
  - Default role on registration.
  - Read posts, search by keywords or tags, like/unlike posts, and comment (comments are held for admin approval).

## Project Structure
```
django_blog_assignment/
├── blog/              # Core Blog App (models, views, forms, tests, admin)
│   ├── models.py
│   ├── views.py
|   |-- urls.py
│   ├── forms.py
│   ├── tests.py
│   └── admin.py
|
├── users/             # User Management App (custom user model, registration)
│   ├── models.py
│   |── views.py
|   |-- urls.py
│   ├── forms.py
│   |── admin.py
|
├── templates/         # HTML templates (base, blog, users)
│   ├── base.html
│   ├── blog/
│   └── users/
├── config/            # Project settings
├── manage.py
|-- .gitignore
|-- LICENCE
|-- README.md
└── requirements.txt
```

## Contributing
- Fork the repository and create a new branch for your feature or bugfix.
- Follow PEP8 and Django best practices.
- Add or update tests for new behavior.
- Submit a pull request describing your changes.

## License
Specify your chosen license here (e.g., MIT). If you don't have one yet, add a LICENSE file to the repository.

## Contact
For questions about this project, reach out to the [Abhishek](https://github.com/Abhishek2634)

Build with ❤️ by Abhishek.