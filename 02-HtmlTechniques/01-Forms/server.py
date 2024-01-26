# To run this application, first you must run:   
#    pip install flask
#    pip install flask_restful

from flask import Flask, request
from flask_restful import Api, Resource

# Create a Flask object and an Api object.
app = Flask(__name__)
api = Api(app)

# Create some sample data.
employees = [
    {
        "id": 0,
        "fullname": "Ola Nordmann",
        "password": "secret",
        "bio": "Born and bred in Norway",
        "salaried": True,
        "emptype": 1,
        "languages": [1, 5]
    },
    {
        "id": 1,
        "fullname": "Kari Nordmann",
        "password": "thatwouldbetelling",
        "bio": "Born and bred in Norway as well",
        "salaried": True,
        "emptype": 3,
        "languages": [1, 4, 8]
    },
]

# Handy counter, useful for generating a new ID every time the user "inserts" a new employee.
nextId = 3

# Define a class that inherits from Resource.
class EmployeeResource(Resource):

    # Define a method to handle GET requests. 
    #   E.g. GET  /employees - Returns all employees.
    #   E.g. GET  /employees/2 - Returns a single employee with specified id, or a 404 error.
    def get(self, id=None):
        if id is None:
            return employees, 200
        else:
            for employee in employees:
                if (id == employee["id"]):
                    return employee, 200
            return "Employee not found", 404
        
    # Define a method to handle POST requests.
    #   E.g. POST /employees    
    # We extract the employee from the incoming HTTP request body (as HTTP form data).
    # Then we add the employee to our list of employees.
    # Then we return the employee, enriched with its newly generated id.
    def post(self):
        global nextId
        formdata = request.form
        print(formdata)           
        employee = {
            "id":  nextId, 
            "fullname": formdata["fullname"],
            "password": formdata["password"],
            "bio": formdata["bio"],
            "salaried": "salaried" in formdata,
            "emptype": formdata["emptype"],
            "languages": formdata.getlist("languages")
        }
        employees.append(employee)
        nextId += 1
        return employee, 201

    # Define a method to handle PUT requests: 
    #   E.g. PUT /employees/2       
    # We extract the updated employee state from the incoming HTTP request body (as HTTP form data).
    # Then we find and modify the existing employee in our list of employees.
    # Then we return the employee.
    def put(self, id):
        formdata = request.form
        for employee in employees:
            if (id == employee["id"]):
                employee["fullname"] = formdata["fullname"]
                employee["password"] = formdata["password"]
                employee["bio"] = formdata["bio"]
                employee["salaried"] = "salaried" in formdata
                employee["emptype"] = formdata["emptype"]
                employee["languages"] = formdata.getlist("languages")
                return employee, 200
        return "Employee not found", 404

    # Define a method to handle DELETE requests: 
    #   E.g. DELETE /employees/2    
    # We find and delete the existing employee in our list of employees.
    def delete(self, id):
        for index, employee in enumerate(employees):
            if (id == employee["id"]):
                employees.pop(index)
                return "Employee deleted", 200
        return "Employee not found", 404

# Register our EmployeeResource class against whatever URL patterns we want to support.      
api.add_resource(EmployeeResource, "/employees", "/employees/<int:id>")

# Start the applictaion in "debug" mode (automatically restarts if you modify this source code).
app.run(debug=True)