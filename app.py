from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson import ObjectId
import os

app = Flask(__name__)

# ✅ Step 1: Connect to MongoDB Atlas
app.config["MONGO_URI"] = "mongodb+srv://clinic_sync_user:<password>@cluster0.mongodb.net/Clinic_sync?retryWrites=true&w=majority"
mongo = PyMongo(app)

# ✅ Step 2: Web UI Route
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Step 3: API Route for Booking Appointments
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    appointment = {
        "name": data.get("name"),
        "email": data.get("email"),
        "appointment_date": data.get("appointment_date"),
    }
    
    # Store in MongoDB
    mongo.db.appointment_details.insert_one(appointment)
    
    return jsonify({"message": "Appointment successfully booked!"})

# ✅ Step 4: Retrieve Appointments (Optional Admin Feature)
@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = list(mongo.db.appointment_details.find())
    for appointment in appointments:
        appointment["_id"] = str(appointment["_id"])  # Convert ObjectId to string
    return jsonify(appointments)

# ✅ Step 5: Run the App Locally (for testing)
if __name__ == '__main__':
    app.run(debug=True)
