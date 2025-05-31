from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse,marshal_with, fields,abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
api = Api(app)


# Define a simple model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    

    def __repr__(self):
        return f'User(name = {self.username},email = {self.email})'

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, help='Username of the user', required=True)
user_args.add_argument('email', type=str, help='Email of the user', required=True)

# // Define the fields for marshalling
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args['username'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return user, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user
    
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        user.username = args['username']
        user.email = args['email']
        db.session.commit()
        return user, 200
    
    @marshal_with(user_fields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return '', 200
            
            
            
            
            
            
            
            
api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:id>')
@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)