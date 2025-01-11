**Library Management System**

This is a Python-based library management system using FastAPI, SQLAlchemy, and Alembic for database management and API creation.

**Features**

•	Manage books, readers, and loans.

•	Filter books based on multiple criteria.

•	Track loans and due dates.

•	Database migrations with Alembic.

•	RESTful APIs for interaction.

**Prerequisites**

Before running this project, ensure you have the following installed:

•	Python 3.10+

•	PostgreSQL

•	pip for installing Python packages

**Installation**

1.	Clone the repository:

```jsx
git clone https://github.com/Maria-Shakhverdyan/library_project.git
cd library-management
```

2.	Create and activate a virtual environment:

```jsx
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3.	Install dependencies:

```jsx
pip install -r requirements.txt
```

1. Configure enviroment variables:

Create a .env file in the root directory and set the following variables:

```python
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=library_db
```

**Setting Up the Database**

1.	Ensure PostgreSQL is running on your machine.

2.	Create the database:

```python
psql -U postgres
CREATE DATABASE library_db;
```

3.	Run the database migrations:

```python
alembic upgrade head
```

**Running the Application**

1.	Start the FastAPI server:

```python
uvicorn app.library_rest_api:app --reload
```

2.	Open your browser and navigate to:

```python
http://127.0.0.1:8000/docs
```

This opens the automatically generated API documentation.

**Usage**

•	Use the Swagger UI (http://127.0.0.1:8000/docs) to test and interact with the APIs.

•	Manage books, readers, and loans via API endpoints.

**Common Issues**

1.	**Database Connection Error**:

•	Ensure your PostgreSQL server is running.

•	Verify the credentials in the .env file.

2.	**Alembic Migration Issues**:

•	Check the alembic.ini file for the correct sqlalchemy.url.
