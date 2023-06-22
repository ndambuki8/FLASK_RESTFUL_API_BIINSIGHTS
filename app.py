from distutils.debug import DEBUG
from distutils.log import debug
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
# app.app_context().push() #solves working out of application context

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



#--For GET request to http://localhost:5000/
class GetEmployee(Resource):
    def get(self):
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            emp_data = {'Id':emp.id, 'FirstName':emp.firstname, 'LastName':emp.lastname, 'Gender':emp.gender,
                        'Salary':emp.salary}
            emp_list.append(emp_data)
        return {"Employees":emp_list}, 200


#--For Post request to http://localhost:5000/employee
class AddEmployee(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(firstname=request.json['FirstName'], lastname=request.json['LastName'],
                    gender=request.json['Gender'], salary=request.json['Salary'])
            db.session.add(emp)
            db.session.commit()

            #return a json response
            return make_response(jsonify({'Id':emp.id, 'First Name': emp.firstname, 'Last Name': emp.lastname,
                                    'Gender':emp.gender, 'Salary':emp.salary}), 201)
        else:
            return {'error':'Request must be JSON'}, 400

#--For Put request to http://localhost:5000/update/? --takes user id to update
class UpdateEmployee(Resource):
    def put(self, id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'error':'not found'}, 404
            else:
                emp.firstname = request.json['FirstName']
                emp.lastname = request.json['LastName']
                emp.gender = request.json['Gender']
                emp.salary = request.json['Salary']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error':'Request must be JSON'}, 400

#--For Delete request to http://localhost:5000/delete? -- takes an id of user to delete
class DeleteEmployee(Resource):
    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error':'not found'}, 404
        
        db.session.delete(emp)
        db.session.commit()
        return f'{id} is deleted', 200 

#use add_Resource function to register a route to one of the classes above
api.add_resource(GetEmployee, '/')
api.add_resource(AddEmployee, '/add')
api.add_resource(UpdateEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)