from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)


class User(db.Model):
    
    __tablename__='users'
    
    username = db.Column(db.String, primary_key=True, unique=True)
    password=db.Column(db.String, nullable=False)
    email=db.Column(db.String,nullable=False, unique=True)
    first_name=db.Column(db.String,nullable=False)
    last_name=db.Column(db.String,nullable=False)
    feedback = db.relationship('Feedback', backref='user',cascade='all,delete')
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        
        hashed= bcrypt.generate_password_hash(password)
        hashed_utf8=hashed.decode('utf8')
        user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
            )
        
        db.session.add(user)
        return user
        
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            False
        
    
class Feedback(db.Model):
    
    __tablename__='feedbacks'
    
    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    username=db.Column(db.String, db.ForeignKey('users.username'),nullable=False)