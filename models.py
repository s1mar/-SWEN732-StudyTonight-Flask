from sqlalchemy import Column, Integer,String
from passlib.apps import custom_app_context as pass_context
from sqlalchemy.sql.schema import Index
from database import Base

class User(Base):
    __tablename__ = 'user'
    fullname = Column(String(64))
    username = Column(String(32), index = True)
    email = Column(String(32))
    date_of_birth = Column(String(32))
    user_id = Column(Integer, primary_key = True)
    password_hash = Column(String(64))

    #Good practice to store password as a hash in the db
    def gen_password_hash(self,password):
        self.password_hash = pass_context.encrypt(password)

    #Generate and verify the hashes to find out if the user entered the correct password
    def verify_password(self,password):
        return pass_context.verify(password,self.password_hash)

