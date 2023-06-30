#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        new_user = User(username= request.get_json()['username'])
        new_user.password_hash = request.get_json()['password']
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return new_user.to_dict(), 201
api.add_resource(Signup, '/signup', endpoint='signup')

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(), 200
        else:
            return {}, 204
api.add_resource(CheckSession, '/check_session', endpoint='check_session')

class Login(Resource):
    def post(self):
        user = User.query.filter(User.username == request.get_json()['username']).first()
        if user.authenticate(request.get_json()['password']):
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {}, 401
api.add_resource(Login, '/login', endpoint='login')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 200
api.add_resource(Logout, '/logout', endpoint='clear')


#api.add_resource(ClearSession, '/clear', endpoint='clear')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
