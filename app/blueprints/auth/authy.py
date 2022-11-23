from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from flask import g
from config import Config

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    # This function will return True of False if they are verified
    u=User.query.filter_by(email = email).first()
    # Check if there is a user with that email
    if not u:
        return False
    g.current_user = u
    return u.check_hashed_password(password)

@token_auth.verify_token
def verify_token(token):
    u = User.check_token(token) if token else None
    g.current_user = u
    return u

