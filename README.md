# User and Role Management APIs

This Django-based API provides functionality for managing users and roles.

## Features
- Role CRUD operations with search functionality
- User CRUD operations with search functionality
- User Authentication (Signup and Login)
- Access Module
- Bulk User Update

## Python Version
This project requires Python 3.12 or greater version

### Dependencies:
- Django: The web framework used for this project.
- python-dotenv: To load environment variables from a .env file.

## Project Structure
- user/: Handles user and role management. Contains API endpoints for CRUD operations on users and roles.
- user_role_management/: Contains project-level settings and URL configurations.
- .env: Environment variables (e.g., secret keys).
- db.sqlite3: SQLite database file.
- manage.py: Django's CLI tool for running the server and performing tasks.
- requirements.txt: Lists the dependencies for the project.
- README.md: Project documentation.

## Running the Project Locally
1. Clone the repository and navigate to it:
    ```
    git clone user_role_management
    cd user_role_management
    ```

2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Apply database migrations:
    ```
    python manage.py migrate
    ```

5. Run the server:
    ```
    python manage.py runserver
    ```

6. Access the API:
    The server will be running at http://127.0.0.1:8000/.


## API Endpoints

### Role APIs
- Get all roles: GET /api/roles/
- Get all roles with search: GET /api/roles/?search='Ad'
- Create a new role: POST /api/roles/
- Get a specific role by ID: GET /api/role/<int:pk>/
- Update a specific role by ID: PUT /api/role/<int:pk>/
- Delete a specific role by ID: DELETE /api/role/<int:pk>/

### User APIs
- Get all users: GET /api/users/
- Get all users with search: GET /api/users/?search='Ad'
- Create a new user: POST /api/users/
- Get a specific user by ID: GET /api/user/<int:pk>/
- Update a specific user by ID: PUT /api/user/<int:pk>/
- Delete a specific user by ID: DELETE /api/user/<int:pk>/

### Authentication APIs
- User signup: POST /api/signup/
- User login: POST /api/login/

### Access Module Management
- Check access to a module by user ID: GET /api/access_modules/<int:pk>/?module=<module_name>
- Add access to multiple modules for a role: PUT /api/access_modules/<int:pk>/
- Remove a module from a role: DELETE /api/access_modules/<int:pk>/

### Bulk User Updates
- Update multiple users with the same data: PUT /api/bulk_user_update/ with type='same_data'
- Update multiple users with different data: PUT /api/bulk_user_update/ with type='different_data'

## Steps for create the Project
1. Create the Directory and navigate to it:
    ```
    mkdir python_task
    cd python_task
    ```

2. Create a virtual environment and activate it:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install the dependencies:
    ```
    pip install django python-dotenv
    ```

4. Create the Django project and navigate to it:
    ```
    django-admin startproject user_role_management
    cd user_role_management
    ```

5. Create the user app:
    ```
    python manage.py startapp user
    ```

6. Add the App to Installed Apps in settings.py:
    ```
    INSTALLED_APPS = [
        # ...,
        user'
    ]
    ```

7. Do code for Models, Views, and URLs as Described.

8. Migrations

    Create Migrations:
    ```
    python manage.py makemigrations
    ```

    Apply Migrations:
    ```
    python manage.py migrate
    ```
