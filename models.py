"""Models for User"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db =  SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connecting the database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Creating User Model"""

    __tablename__ = "users"

    username = db.Column(
        db.String(20), 
        primary_key=True, 
        unique=True, 
        nullable=False,)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback', backref = 'user', cascade='all,delete')
    
    @property
    def get_full_name(self):
        """Return users fullname"""

        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        """Show info"""

        u = self
        return f"<User {u.first_name} {u.last_name} with {u.id}id >"
    

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register users with hashed password and return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username = username,
            password = hashed_utf8, 
            email = email,
            first_name = first_name,
            last_name = last_name
        )
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validates user exists and pwd is correct, return user or False"""

        user = User.query.filter_by(username = username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        
class Feedback(db.Model):
    """Creating Feedback Model"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20), 
        db.ForeignKey('users.username'), 
        nullable=False,
    )

    

