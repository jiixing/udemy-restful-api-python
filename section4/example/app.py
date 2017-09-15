from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) # easier to handle Resources

# each Resource needs to be a Class

class Student(Resource): # inheritance
	
	def get(self, name):
		return {"student": name}

# let api access this resource
api.add_resource(Student, "/student/<string:name>") 
# now we can access at http://127.0.0.1:5000/student/student_name

app.run(port=5000)
