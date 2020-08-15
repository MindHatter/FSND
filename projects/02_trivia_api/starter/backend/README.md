# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Endpoints

GET '/categories'
- Description: Return all available categories
- Request data: None
- Response data: {
    'success': True,
    'categories': ["Science", "Art", ...]
}

GET '/questions'
- Description: Return every 10 question per page
- Request data: None
- Response data: {
    'success': True,
    'questions': [{
        "question": "question",
        "answer": "answer",
        "category": 1,
        "difficulty": 1,
        "id": 1,
        }, ...],
    'total_questions': 18,
    'categories': ["Science", "Art", ...],
}

GET '/categories/<int:id>/questions'
- Description: Return questions by category
- Request data: question ID (int)
- Response data: {
    'success': True,
    'questions': questions_in_page,
    'total_questions': len(questions),
    'current_category': category.type
}

POST '/questions'
- Description: Create question in database
- Request data: {
    "question": "question"
    "answer": "answer",
    "category": 1,
    "difficulty": 1,
}
- Response data: {
    'id': 1,
    'success': True
}

POST '/questions/search'
- Description: Return all question by search
- Request data: {
    "searchTerm": "Text"
}
- Response data: {
    'success': True,
    'questions': [{
        "question": "question",
        "answer": "answer",
        "category": 1,
        "difficulty": 1,
        "id": 1,
        }, ...],
    'total_questions': 18,
}

POST '/quizzes'
- Description: Return next question for quiz
- Request data: {
    'previous_questions': [10, 14, ...]
    'quiz_category': {
        'type': "Science",
        "id": 1
    }
}
- Response data: {
    'success': True,
    'previousQuestions': [10, 14, 6, ...],
    'question': {
        "question": "question",
        "answer": "answer",
        "category": 1,
        "difficulty": 1,
        "id": 1,
    }
}

DELETE '/questions/<int:id>'
- Description: Delete auestion by ID from database
- Request data: question ID (int)
- Response data: {
    "id": 1,
    "success": True,
}

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```