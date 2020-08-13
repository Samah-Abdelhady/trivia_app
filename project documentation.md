# Project Documentation:

## Udacity Trivia App
### Trivia app is a bonding experiences for Udacity's employees and students. It is a webpage to manage:
1. Display questions - both all questions and by category.
   * Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2. Delete questions.
3. Add questions
   * require that they include question and answer text.
4. Search for questions 
   * based on a text query string.
5. Play the quiz game
   * randomizing either all questions or within a specific category. 


## Getting Started
### Pre-requisites and Local Development:
To use this project on your local machine, you should alredy have
  * Python3
  * pip
  * install node
### Backend
from the backend folder run: pip install requirements.txt . As all required packagesare included in the requirements file.

To run the application use the following commands:
1. export FLASK_APP=flasker=flasker
2. export FLASK_ENV=development
3. flask run

If you are using Windows OS, then use these commands instead:
1. set FLASK_APP=flasker=flasker
2. set FLASK_ENV=development
3. flask run

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

The application is run on: http://127.0.0.1:5000/  by default and is a proxy in the frontend configuration.


### Frontend
From the frontend folder, run the following commands to start the client:
1. npm install   //only once to install dependencies
2. npm start

By default, the frontend will run on localhost:3000.


### Tests
In order to run tests navigate to the backend folder and run the following commands:
1. dropdb trivia_test
2. createdb trivia_test
3. psql trivia_test < trivia.psql
4. python test_flaskr.py

The first time yourun tests, omit the dropdb command.

All tests are kept in test_flasker.py file and should be maintained as updates are made to app functionality.


## API Reference

### Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/ , which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:

{
	"success": False,
	"error": 4oo,
	"message": "bad request"
}

The API will return four error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 422: Unprocessable
* 500: Internal Server Error

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


## Authors
Udacity Team, and me Samah worked on API


## Acknowledgements
The Team of Udacity

