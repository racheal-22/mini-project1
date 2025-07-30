import unittest
from app import app, db
from models import RequestRecord
import json

class TestSmartSum(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_valid_sum(self):
        response = self.client.post('/compute', data={'numbers': '10, 20'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sum Result', response.data)

    def test_invalid_sum(self):
        response = self.client.post('/compute', data={'numbers': '10, abc'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid input', response.data)

    def test_empty_input(self):
        response = self.client.post('/compute', data={'numbers': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter some numbers.', response.data)  

    def test_transaction_lookup(self):
        with app.app_context(): 
            record = RequestRecord(numbers=json.dumps([10, 20]), result=30)
            db.session.add(record)
            db.session.commit()

            response = self.client.post('/transaction', data={'txn_id': record.id})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sum Result', response.data)

if __name__ == '__main__':
    unittest.main()
