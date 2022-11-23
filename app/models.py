from unicodedata import category
from app import db, login
from flask_login import UserMixin #####  THIS IS ONLY FOR THE USER MODEL
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    token = db.Column(db.String, unique=True, index=True)
    token_exp = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)


    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        # If their is a token and it is valid we willtreturn the token
        if self.token and self.token_exp > current_time+timedelta(seconds=60):
            return self.token
        # There was no token or It was expired, so make a new token
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=60)
    
    @staticmethod
    def check_token(token):
        # u=User.query.filter(User.token == token).first()
        u = User.query.filter_by(token = token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u


    
    #should return a unique identifying string (for computer to read)
    def __repr__(self):
        return f'<User: {self.email} | {self.id} >'
    
    # Human Readable
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name} >'
    
    #salt and hash our password to make it harder to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    #Check the hashed password(self.password) to the password they are using at login
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)


    def save(self):
        db.session.add(self) #add the user to our session
        db.session.commit() #saves the session
    
    def to_dict(self):
        return {
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'created_on' :self.created_on,
            'token':self.token,
            'is_admin':self.is_admin
        }
    def from_dict(self,data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
 