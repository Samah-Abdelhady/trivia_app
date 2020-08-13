import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [Question.format(question) for question in selection]
  current_questions = questions[start:end]

  # if(len(questions) < ((page - 1) * QUESTIONS_PER_PAGE) + 1):
  #   current_questions = []# in case there isn't at least one question to be set in the given page 
  
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins":"*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories')
  def available_categories():
    try:
      categories = Category.query.all()

      current_categories = {category.id:category.type for category in categories}
      total_categories = len(categories)

      return jsonify({
        'success': True,
        'categories': current_categories,
         'total_categories': total_categories
      })
    except:
      abort(500) #if can't retreive data, it is then a server error
    finally:
      db.session.close()


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
  @app.route('/api/questions')
  def available_questions():
    # try:
      questions = Question.query.all()
      current_questions = paginate_questions(request, questions)
      total_questions = len(questions)

      categories = Category.query.all()
      current_categories = {category.id:category.type for category in categories}

      db.session.close()

      if len(current_questions) == 0: # if there is no questions in db
        abort(404) # then tell user that no questions are founded

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': total_questions,
        'current_catogery': None,
        'categories': current_categories
      })
    # except:
    #   abort(500) #if can't retreive data, it is then a server
    # finally:
    #   db.session.close()

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      else:
        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id
        })
    except:
        abort(422)
    finally:
        db.session.close() 

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions', methods=['POST'])
  def create_new_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search = body.get('searchTerm', None)
    search = search.strip()

    try:
      if search:
        selection = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
        current_questions = paginate_questions(request, selection)
        current_questions = [question.format() for question in selection]
        # total_questions = len(selection)

        return jsonify({
          'success': True,
          'questions': current_questions
          # 'total_questions': total_questions
          })

      else:
        if((new_question=="") or (new_answer=="")):
          abort(400)
        else:
          question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
          question.insert()
          selection = Question.query.all()
          db.session.close()
          # current_questions = paginate_questions(request, selection)

          total_questions = len(selection)

          return jsonify({
            'success': True,
            'created': question.id,
            # 'questions': current_questions,
            'total_questions': total_questions
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
  @app.route('/api/questions/<string:search_term>/questionTerm')
  def get_exist_question(search_term):
    # body = request.json
    search = search_term.strip()

    try:
      if search:
        selection = Question.query.filter(Question.question.ilike(f'%{search}%')).all()
        current_questions = paginate_questions(request, selection)
        current_questions = [question.format() for question in selection]
        

        return jsonify({
          'success': True,
          'questions': current_questions
          })
      else:
        abort(404)

    except:
      abort(422)
    finally:
      db.session.close()

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:category_id>/questions')
  def get_specific_category_questions(category_id):
    # try:
    questions = Question.query.filter_by(category=str(category_id)).all()
    total_questions = len(questions)
    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': total_questions,
        'current_category': category_id,
        'categories': Category.query.get(category_id)
        })
    # except:
    #   abort(422)
    # finally:
    #   db.session.close()

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
  @app.route('/api/quizzes', methods=['POST'])
  def play_the_quiz():

    try:
      body = request.get_json()
      category = body['quiz_category']['id']
      previous_questions = body['previous_questions']
    except:
      abort(400)

    if (category == 0):# zerofor all qustions
      current_questions = Question.query.all() # get all qustions
    else:
      current_questions = Question.query.filter_by(category=str(category)).all()

    current_questions = [questions.format() for questions in current_questions]
    rest_of_questions = []

    for question in current_questions:
      if(question['id'] not in previous_questions):
        rest_of_questions.append(question)

    if(rest_of_questions == 0):
      return jsonify({
        'success': True,
        'message': 'the quiz is completed'
        })
    else:
      next_question = random.choice(rest_of_questions)
      return jsonify({
        'success': True,
        'question': next_question
        })


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500
  
  return app

    