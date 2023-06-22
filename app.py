from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

#create an instance of flask
app = Flask(__name__)

#Creating an API object -- to help with URL routing
api = Api(app)

#create a database - SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #why do this? --flask server complains

#SQLALchemy mapper --Help interact with the db
db = SQLAlchemy(app)
app.app_context().push() #solves working out of application context

#define a class Employee  --store and retrieve data from Employee table in db
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} - {self.salary}"

##CREATING THE DB
# db.create_all()

# emp = Employee(firstname="John", lastname="Doe", gender="Male", salary=60000)

# db.session.add(emp)
# db.session.commit()
    
# emp = Employee(firstname="Jane", lastname="Bond", gender="feMale", salary=90000)

# db.session.add(emp)
# db.session.commit()

# print(Employee.query.all())

# END OF CREATING DB

#Creating API Routes Endpoints
