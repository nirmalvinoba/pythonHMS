from flask import Flask, render_template, request, redirect, url_for,session
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

app.secret_key="Niru1234"

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017')  # Update with your MongoDB connection string
db = client.db #it is used to create database
doc = db.doc #it is used to create collection
# Routes and functionality will go here

#global declare panni irukom ....hidden function
def isloggedin(): 
    return "username" in session #username present ah iruka nu check pandrom


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/patients')
def manage_patients():
        patients = db.patients.find()  # Retrieve patients from MongoDB
        return render_template('index.html', patients=patients)

# Add more routes for doctors, appointments, etc.
@app.route('/add_patient', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        patient_data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'gender':request.form['gender'],
            'phone':request.form['phone'],
            'time':request.form['time'],
            'date':request.form['date']
        }
        db.patients.insert_one(patient_data)
        return redirect(url_for('manage_patients'))
    
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_data(id):
    id_1=ObjectId(id)
    
    data = db.patients.find_one({"_id": id_1})
    if request.method == 'POST':
        updated_data = {
            "name": request.form['name'],
            "age": request.form['age'],
            'gender':request.form['gender'],
            'phone':request.form['phone'],
            'time':request.form['time'],
            'date':request.form['date']
        }
        db.patients.update_one({"_id": id_1}, {"$set": updated_data})
        return redirect(url_for('manage_patients'))
    return render_template('edit.html', data=data)

@app.route('/delete/<id>', methods=["GET",'POST'])
def delete_data(id):
    db.patients.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('manage_patients'))


    
if __name__ == "__main__":
    app.run(debug=True,port=8000)




































