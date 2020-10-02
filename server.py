from validate_email import validate_email
from models import User
from flask import Flask, jsonify, request, url_for, abort
from database import db_session

#constants
BASE_ROUTE_V1 = '/api/v1/'

app = Flask(__name__)


@app.route(BASE_ROUTE_V1+'users',methods=['POST'])
def register_user():
    
        full_name = request.json.get('fullname')
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        date_birth = request.json.get('dob')

        if full_name is None or username is None or email is None or password is None or date_birth is None:
            abort(400,"Missing arguments") #missing arguments

        if db_session.query(User).filter_by(username = username).first() is not None:
            abort(406,"User with this username already exists")

        if db_session.query(User).filter_by(email = email).first() is not None:
            abort(406,"User with this email already exists")

        if validate_email(email) is False:
            abort(406,"Invalid email address entered")


        user = User(fullname = full_name,username=username,email=email,date_of_birth=date_birth)
        user.gen_password_hash(password)
        db_session.add(user)
        db_session.commit()
    
        return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.user_id, _external = True)} 


@app.route(BASE_ROUTE_V1+'users'+'/<int:id>')
def get_user(id):
    user = db_session.query(User).filter_by(user_id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})




@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ =='__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=2692)