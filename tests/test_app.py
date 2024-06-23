import unittest
from app import app, db, SudokuGame

class SudokuTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_start_game(self):
        response = self.app.post('/start', json={'username': 'test_user', 'difficulty': 'easy'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('grid', response.get_json())

    def test_validate_solution(self):
        # This would be an example with a correct solution for an easy game
        response = self.app.post('/validate', json={'grid': [[0] * 9 for _ in range(9)], 'solution': [[0] * 9 for _ in range(9)]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('correct', response.get_json())

if __name__ == '__main__':
    unittest.main()
