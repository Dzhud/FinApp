# Setting Up REST Api with Flask_Restful


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer, String
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
#from marshmallow_sqlalchemy import SQLAlchemySchema

app = Flask(__name__)
api = Api(app)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:morrky@localhost/finApp_db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)
ma = Marshmallow(app)



# Creating Tables
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

    
class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, primary_key=True)
    

class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, primary_key=True)
    wallet_number = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    currency_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False, nullable=True)
    overdraft =  db.Column(db.Integer, primary_key=True)
    

# Creates Marshmallow schema based on Tables
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "phone_number", "email")
        
class ProfileSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "user_id")   
    
class WalletSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "balance", "wallet_number", "first_name", "last_name", "currency_id", "status", "overdraft")
    
    
users_schema = UserSchema(many=True)
profile_schema = ProfileSchema(many=True)
wallet_schema = WalletSchema(many=True)



# Creates new RESTFUL Resource
class UserListResource(Resource):
    def get(self):
        user = User.query.all()
        return users_schema.dump(user)
    
    def post(self):
        new_user = User(id=request.json['id'], phone_number=request.json['phone_number'], email=request.json['email'])
        db.session.add(new_user)
        db.session.commit()
        return users_schema.dump(new_user)
    
api.add_resource(UserListResource, '/user')



class ProfileListResource(Resource):
    def get(self):
        profile = Profile.query.all()
        return profile_schema.dump(profile)
    
    def post(self):
        new_profile = Profile(id=request.json['id'], first_name=request.json['first_name'], last_name=request.json['last_name'], user_id=request.json['user_id'])
        db.session.add(new_profile)
        db.session.commit()
        return profile_schema.dump(new_profile)
    
api.add_resource(ProfileListResource, '/profile')


class WalletListResource(Resource):
    def get(self):
        wallet = Wallet.query.all()
        return wallet_schema.dump(wallet)
    
    def post(self):
        new_wallet = Wallet(id=request.json['id'], user_id=request.json['user_id'], balance=request.json['balance'], wallet_number=request.json['wallet_number'], first_name=request.json['first_name'], last_name=request.json['last_name'], currency_id=request.json['currency_id'], status=request.json['status'], overdraft=request.json['overdraft'])
        db.session.add(new_wallet)
        db.session.commit()
        return wallet_schema.dump(new_wallet)
    
api.add_resource(WalletListResource, '/wallet')



# Creates new Resource to fetch User/Profile/Wallet details
# Something seem to be wrong here so still working on this
'''
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return users_schema.dump(user)

api.add_resource(UserResource, '/user/<int:user_id>') 


class ProfileResource(Resource):
    def get(self, profile_id):
        profile = Profile.query.get_or_404(profile_id)
        return profile_schema.dump(profile)

api.add_resource(ProfileResource, '/profile/<int:profile_id>') 


class WalletResource(Resource):
    def get(self, wallet_id):
        wallet = Wallet.query.get_or_404(wallet_id)
        return wallet_schema.dump(wallet)

api.add_resource(WalletResource, '/profile/<int:wallet_id>') 

'''

    

if __name__ == "__main__":
    app.run(debug=True)