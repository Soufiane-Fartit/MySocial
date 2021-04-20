from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.String(1000), nullable=True)
    picture_path = db.Column(db.String(1000), nullable=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    text = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    total_views = db.Column(db.Integer)
    total_likes = db.Column(db.Integer)
    total_comments = db.Column(db.Integer)
    total_shares = db.Column(db.Integer)

    def __init__(self, user_id, text):
        from datetime import date, datetime
        self.user_id = user_id
        self.text = text
        self.date = date.today().strftime("%d/%m/%Y")
        self.time = datetime.now().strftime("%H:%M:%S")
        self.total_views = 0
        self.total_likes = 0
        self.total_comments = 0
        self.total_shares = 0

class Relations(db.Model):
    user1_id = db.Column(db.Integer, primary_key=True)
    user2_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10))

    def __init__(self, user1_id, user2_id, status):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.status = status

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    text = db.Column(db.String(1000))

    def __init__(self, post_id, user_id, text):
        self.post_id = post_id
        self.user_id = user_id
        self.text = text

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer)
    user2_id = db.Column(db.Integer)

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer)
    user1_id = db.Column(db.Integer)
    user2_id = db.Column(db.Integer)
    text = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))

    def __init__(self, user1_id, user2_id, text):
        from datetime import date, datetime
        from sqlalchemy import or_, and_
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.text = text
        self.date = date.today().strftime("%d/%m/%Y")
        self.time = datetime.now().strftime("%H:%M:%S")
        conv = Conversation.query.filter(or_(Conversation.user1_id==user1_id, 
                                            Conversation.user1_id==user2_id))\
                                .first()
        if conv:
            self.conversation_id = conv.id
        else:
            new_conv = Conversation(user1_id, user2_id)
            db.session.add(new_conv)
            db.session.commit()
            conv = Conversation.query.filter(or_(Conversation.user1_id==user1_id, 
                                                Conversation.user1_id==user2_id))\
                                    .first()
            self.conversation_id = conv.id

# from . import create_app
# db.create_all(app=create_app())
