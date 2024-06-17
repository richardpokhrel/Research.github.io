from flask import Flask, request, render_template_string, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open('form.html').read())

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    firstname = data['firstName']
    lastname = data['lastName']
    email = data['emailaddress']
    highSchoolName = data['highSchoolName']
    highSchoolLocation = data['highSchoolLocation']
    currentFaculty = data['currentFaculty']
    referralSource = data['referralSource']
    source = data['source']
    
    # Connect to the database and check for existing email
    conn = sqlite3.connect('university_applications.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName TEXT,
            lastName TEXT,
            emailaddress TEXT UNIQUE,
            highSchoolName TEXT,
            highSchoolLocation TEXT,
            currentFaculty TEXT,
            referralSource TEXT,
            source TEXT
        )
    ''')

    c.execute('SELECT * FROM applications WHERE emailaddress = ?', (email,))
    existing_email = c.fetchone()

    if existing_email:
        conn.close()
        return jsonify({"error": "Email address already exists!"}), 400

    c.execute('''
        INSERT INTO applications (
            firstName, lastName, emailaddress, highSchoolName, highSchoolLocation, currentFaculty, referralSource, source 
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (firstname, lastname, email, highSchoolName, highSchoolLocation, currentFaculty, referralSource, source))

    conn.commit()
    conn.close()

    return jsonify({"message": "Application submitted successfully!"})

@app.route('/applications')
def applications():
    conn = sqlite3.connect('university_applications.db')
    c = conn.cursor()
    c.execute("SELECT * FROM applications")
    rows = c.fetchall()
    conn.close()

    return '<br>'.join([f"First Name: {row[1]}, Last Name: {row[2]}, Email Address: {row[3]}, High School Name: {row[4]}, High School Location: {row[5]}, Current Faculty: {row[6]}, Referral Source: {row[7]}, Source: {row[8]} " for row in rows])

if __name__ == '__main__':
    app.run(port=55002, debug=True)
