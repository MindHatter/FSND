import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    current = selection[start:end]

    return current


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,PUT,POST,DELETE,OPTIONS')
        return response
    '''

    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = [c.type for c in Category.query.all()]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = [q.format() for q in Question.query.all()]
        questions_in_page = paginate(request, questions)
        categories = [c.type for c in Category.query.all()]

        if len(questions_in_page) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions_in_page,
            'total_questions': len(questions),
            'categories': categories,
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        try:
            question = Question.query.filter(Question.id == q_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                "id": q_id,
                "success": True,
            })
        except:
            abort(422)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.    
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            data = request.get_json()
            question = Question(
                question=data['question'],
                answer=data['answer'],
                difficulty=int(data['difficulty']),
                category=int(data['category'])+1
            )
            question.insert()
            return jsonify({
                'success': True
            })
        except:
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            search_term = request.get_json()['searchTerm']
        except:
            abort(422)

        matches = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term)))
        questions = [q.format() for q in matches]

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': len(questions),
        })

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:c_id>/questions', methods=['GET'])
    def get_questions_by_category(c_id):
        category = Category.query.filter(Category.id == c_id).one_or_none()

        if category is None:
            abort(404)

        try:
            questions = [q.format()
                            for q in Question.query.filter(Category.id == c_id)]
            questions_in_page = paginate(request, questions)

            return jsonify({
                'success': True,
                'questions': questions_in_page,
                'total_questions': len(questions),
                'current_category': category.type
            })
        except:
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quizz_question_question():
        # try:
        data = request.get_json()
        previous_questions = data.get('previous_questions', None)
        quiz_category = data.get('quiz_category', None)

        print(previous_questions, quiz_category)
        if quiz_category['type'] == 'click':
            questions = [q.format() for q in Question.query.all()]
        else:
            questions = [q.format() for q in Question.query.filter_by(
                category=int(quiz_category['id'])+1
            )]

        questions = list(
            filter(lambda x: x['id'] not in previous_questions, questions))
        question = None
        if len(questions) > 1:
            question = random.choice(questions)

        print(question)
        return jsonify({
            'success': True,
            'previousQuestions': previous_questions,
            'currentQuestion': question,
            'question': question
        })
        # except:
        #     abort(422)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    return app
