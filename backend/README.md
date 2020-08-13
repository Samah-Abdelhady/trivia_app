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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

### Endpoints

### GET '/api/categories'
* General:
   * Get a dictionary of categories {"id":"Caregory name"}
   * Return an object of keys: categories, which contains a object of id: category_string_name, and total_categories, which contain the total number of existing categories
* Sample: `curl http://localhost:5000/api/categories`
{
'categories': {	
	'1': "Science"
	'2': "Art"
	'3': "Geography"
	'4': "History"
	'5': "Entertainment"
	'6': "Sports"
},
'success': True,
'total_categories': 6
}


### GET '/api/questions'
* General:
   * Get all questions in all trivia categories
   * Paginates results to make only maximum 10 questions per page
   * Add parameter to URL `?page=pageNumber` to see different pages' questions (default page is 1)
   * Return a list of questions, number of total questions, current category, categories
* Samples:
   * `curl http://localhost:5000/api/questions`
   * `curl http://localhost:5000/api/questions?page=2`

{	
'categories': {	
	'1':"Science"
	'2': "Art"
	'3': "Geography"
	'4': "History"
	'5': "Entertainment"
	'6': "Sports"
},
'current_catogery': null,
'questions': {	
	'0':{	
		'answer': "Maya Angelou"
		'category': '4'
		'difficulty': 2
		'id': 5
		'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	    },            
	'1': {	
		'answer': "Muhammad Ali"
		'category': '4'
		'difficulty': 1
		'id': 9
		'question': "What boxer's original name is Cassius Clay?"
	     }
	... There is another 17 question ...
		},

'success': True,
'total_questions': 19
}


### DELETE '/api/questions/<question_id>'
* General
   * Delete a question by its id
   * Return success status and the deleted question's id
* Sample: `curl -X DELETE http://localhost:5000/api/questions/23`

{
    'success': True,
     'deleted': 23
 }


### POST '/api/questions'
* General
   * Here you can do two things:
	1. Create new question via form
	   * Require question data via `application/json`
           * Returns success status, id of the new successful created question and the total number of completely created questions 
	2. Search about existing question via search term form
	   * Require search term data via `application/json`
           * Returns success status and a list of questions which include the search trem in their content

1. {
    'success': True,
    'created': 24,
    'total_questions': 20
  }


2. {
  'questions': [
    {
	'answer': "Muhammad Ali"
	'category': '4'
	'difficulty': 1
	'id': 9
	'question': "What boxer's original name is Cassius Clay?"
    }
  ], 
  'success': True
}


### GET '/api/categories/<category_id>/questions'
* General
   * Get all question of a specific category based on its id
   * Return success status, the number of total questions inside that category aspaginated and category id 
* Sample: `curl http://localhost:5000/api/categories/5/questions`

{
  'categories': {
    'id': 5, 
    'type': "Geography"
  },
  'current_category': 5,
  'questions': {	
	'2': {	
		'answer': "Apollo 13"
		'category': '5'
		'difficulty': 4
		'id': 2
		'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
             },
	'3': {	
		'answer': "Tom Cruise"
		'category': '5'
		'difficulty': 4
		'id': 4
		'question': "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
             },
	'4': {	
		'answer': "Edward Scissorhands"
		'category': '5'
		'difficulty': 3
		'id': 6
		'question': "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
             },

	'success': True,
        'total_questions': 3
}


### POST '/api/quizzes'
* General
   * It requires the category id and a list of prvious asked questions
   * It plays a quiz of questions of a specific category whch were not asked yet
   * Returns success status and a message told user that the quiz is completed if all questions were already asked
   * Returns success status anda random question from a non asked yet questions if all questions were not asked
* Samples: 
    1. sample of no previous questions existed:   `curl -X POST http://localhost:5000/api/quizzes -H "Content-Type: application/json" -d '{previous_questions: [], quiz_category: {type: "click", id: 0}}'`
    2. sample of all previous questions existed:   `curl -X POST http://localhost:5000/api/quizzes -H "Content-Type: application/json" -d '{previous_questions: [2, 4, 6], quiz_category: {type: "History", id: "5"}}'`


1.  {
  'question': {
    	'answer': "Apollo 13"
	'category': '5'
	'difficulty': 4
	'id': 2
	'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }, 
  'success': True
}


2.   {
        'success': True,
        'message': 'the quiz is completed'
     }

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```