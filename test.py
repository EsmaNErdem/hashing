from unittest import TestCase
from app import app
from models import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

db.drop_all()
db.create_all()

user = {
    "username": "SmokeyB",
    "password": "Test123",
    "email": "random@email.com",
    "first_name": "Smokey",
    "last_name": "Baker"
}
class FeedbackUserTestCase(TestCase):
    """Test for views feedback app"""

    def test_register_user(self):
        with app.test_client() as client:
            resp = client.post("/register", data=user)
            
            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            import pdb
            pdb.set_trace()
            # self.assertIn('<h1 class="display-1">Smokey Baker</h1>', html)