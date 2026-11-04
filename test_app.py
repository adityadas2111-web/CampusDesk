import tempfile
import unittest
from pathlib import Path
from app import create_app

class CampusDeskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.app = create_app(Path(self.tmp.name) / 'test.db')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.client.get('/')
        with self.client.session_transaction() as s:
            self.token = s['csrf']
    def tearDown(self):
        self.tmp.cleanup()
    def post(self, path, **data):
        return self.client.post(path, data={'csrf': self.token, **data})
    def add(self, **changes):
        fields = dict(title='Broken fan',location='Room 204',category='Electrical',priority='High',description='Fan does not turn.')
        fields.update(changes)
        return self.post('/add', **fields)
    def test_lifecycle(self):
        self.assertEqual(self.add().status_code, 302)
        self.assertIn(b'Broken fan', self.client.get('/?q=204').data)
        self.assertEqual(self.post('/update/1', status='Resolved').status_code,302)
        self.assertNotIn(b'Broken fan',self.client.get('/?status=Open').data)
        self.assertIn(b'Broken fan',self.client.get('/?status=Resolved').data)
        self.assertEqual(self.post('/delete/1').status_code,302)
        self.assertNotIn(b'Broken fan',self.client.get('/').data)
    def test_validation(self):
        for changes in ({'title':' '},{'location':''},{'description':''},{'priority':'Urgent'},{'category':'Bad'},{'title':'x'*101}):
            self.assertEqual(self.add(**changes).status_code,400)
    def test_csrf_and_missing(self):
        self.assertEqual(self.client.post('/delete/1').status_code,400)
        self.assertEqual(self.post('/delete/999').status_code,404)
        self.assertEqual(self.post('/update/999',status='Open').status_code,404)
    def test_escape_and_search(self):
        self.add(title='<script>alert(1)</script>')
        self.assertIn(b'&lt;script&gt;', self.client.get('/').data)
        self.assertNotIn(b'<script>alert(1)</script>',self.client.get('/').data)
        self.assertEqual(self.client.get('/?q=%27%20OR%201=1--').status_code,200)
        self.assertEqual(self.client.get('/?status=invalid').status_code,400)
    def test_persistence(self):
        self.add()
        second = create_app(self.app.config['DATABASE']).test_client()
        self.assertIn(b'Broken fan',second.get('/').data)

if __name__ == '__main__':
    unittest.main()
