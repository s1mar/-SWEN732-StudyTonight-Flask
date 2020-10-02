from validate_email import validate_email
from models import Base,User
from flask import Flask, jsonify, request, url_for, abort,_app_ctx_stack
from database import SessionLocal,engine
from models import Base
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
#constants
BASE_ROUTE_V1 = '/api/v1/'

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

# CORS(app)

#app.session = scoped_session(SessionLocal,scopefunc=_app_ctx_stack.__ident_func__)
app.session = SessionLocal()

@app.route(BASE_ROUTE_V1+'users',methods=['POST'])
def register_user():
    
        full_name = request.json.get('fullname')
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        date_birth = request.json.get('dob')

        if full_name is None or username is None or email is None or password is None or date_birth is None:
            abort(400,error_message="Missing arguments") #missing arguments

        if app.session.query(User).filter_by(username = username).first() is not None:
            abort(400,error_message="User with this username already exists")

        if validate_email(email) is False:
            abort(400,error_message="Invalid email address entered")


        user = User(fullname = full_name,username=username,email=email,date_of_birth=date_birth)
        user.gen_password_hash(password)
        app.session.add(user)
        app.session.commit()
    
        return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.user_id, _external = True)} 


@app.route(BASE_ROUTE_V1+'users'+'/<int:id>')
def get_user(id):
    user = app.session.query(User).filter_by(user_id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

if __name__ =='__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=2692)