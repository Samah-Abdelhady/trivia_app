import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://{}:{}@{}/{}'.format('postgres','postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        self.new_question = {
            'question': 'how many oceans in the earth',
            'answer': 'five',
            'category': '5',
            'difficulty': 3
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(len(data['categories']), 6)
        # self.assertTrue(data['total_categories'])


    def test_get_all_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        # self.assertEqual(len(data['categories']), 6)

    def test_paginate_questions(self):
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 9)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['categories']), 6)


    def test_404_sent_invalid_page_number(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_question(self):
        res = self.client().delete('/api/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        # self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)


    def test_404_invalid_delete(self):
        res = self.client().delete('/api/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_write_new_question(self):
        all_questions = Question.query.all()
        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], len(all_questions)+1)


    def test_write_new_empty_question(self):
        new_empty_question = {
            "question": " ",
            "answer": "   ",
            "category": "5",
            "difficulty": 3
        }
        res = self.client().post('/api/questions', json=new_empty_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_search_by_question_term(self):
        res = self.client().post('/api/questions', json={"searchTerm": "the ancient Egyptians"}) 
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(data['questions'][0]['id'], 23)


    def test_get_questions_of_specific_category(self):
        res = self.client().get('/api/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 3)


    def test_404_invalid_categorys(self):
        res = self.client().get('/api/categories/9/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_play_complete_quiz(self):
        res = self.client().post('/api/quizzes', json={"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)                 
        self.assertTrue(data['question'])                  
        self.assertEqual(data['question']['category'], 1)       


    def test_play_quiz_with_one_pervious_question(self):
        res = self.client().post('/api/quizzes', json={"previous_questions": [20], "quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 


    def test_play_quiz_with_two_pervious_question(self):
        res = self.client().post('/api/quizzes', json={"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)                
        self.assertEqual(data['question']['id'], 22) 


    def test_play_quiz_after_finishing(self):
        """Tests out the quiz playing functionality"""
        # Test Quiz when no questions are left in category
        res = self.client().post('/api/quizzes', json={"previous_questions": [20, 21, 22], "quiz_category": {"type": "Science", "id": "1"}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'the quiz is completed')
    

    def test_bad_request_for_play_quiz(self):
        res = self.client().post('/api/quizzes', json={"previous_questions": [13], "quiz_category": {"type": "Science"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)     
        self.assertEqual(data['message'], 'bad request')
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()