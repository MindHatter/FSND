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

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = [c.type for c in Category.query.all()]

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })


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

    @app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        question = Question.query.filter(Question.id == q_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        return jsonify({
            "id": q_id,
            "success": True,
        })


    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        category = Category.query.filter(Category.id == int(data['category'])).one_or_none()
        if category is None or int(data['difficulty']) not in range(1,6):
            abort(422)

        question = Question(
            question=data['question'],
            answer=data['answer'],
            difficulty=int(data['difficulty']),
            category=int(data['category'])
        )
        question.insert()
        return jsonify({
            'id': question.id,
            'success': True
        })


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

    @app.route('/categories/<int:c_id>/questions', methods=['GET'])
    def get_questions_by_category(c_id):
        category = Category.query.filter(Category.id == c_id).one_or_none()

        if category is None:
            abort(404)

        try:
            questions = Question.query.filter_by(category=category.id)
            questions = [q.format() for q in questions]
            questions_in_page = paginate(request, questions)

            return jsonify({
                'success': True,
                'questions': questions_in_page,
                'total_questions': len(questions),
                'current_category': category.type
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def get_quizz_question_question():
        try:
            data = request.get_json()
            previous_questions = data.get('previous_questions', None)
            quiz_category = data.get('quiz_category', None)

            if quiz_category[0] == 'click':
                questions = [q.format() for q in Question.query.all()]
            else:
                questions = [q.format() for q in Question.query.filter_by(
                    category=int(quiz_category[1])
                )]

            questions = list(
                filter(lambda x: x['id'] not in previous_questions, questions))
            question = None
            if len(questions) > 0:
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'previousQuestions': previous_questions,
                'question': question
            })
        except:
            abort(422)

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
