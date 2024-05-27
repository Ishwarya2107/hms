from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import connect, Error
import random
app = Flask(__name__)
app.secret_key = 'sculptyourself'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_data', methods=['POST'])
def register_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            age = request.form['age']
            address = request.form['address']
            gender = request.form['gender']
            occupation = request.form['occupation']
            contact = request.form['contact']
            med_rec = request.files['medical_record']
            city = request.form['city']
            
            pdf_data = med_rec.read()
                
        
        
            
            with connect(
                host="localhost",
                user="root",
                password="ish21072004#",
                database = "hms"
            ) as connection:
                insert_table_query = """
                
        INSERT INTO details_of_users (name,age,address,occupation,city,contact,password,gender) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)

        """
                data = (username,age,address,occupation,city,contact,password,gender)
                with connection.cursor() as cursor:
                    cursor.execute(insert_table_query,data)
                    connection.commit()

        except Error as e:
            print(e)
        with connect(
                host="localhost",
                user="root",
                password="ish21072004#",
                database = "hms"
            ) as connection:
            display_table_query = """
    SELECT * FROM details_of_users

    """
            
            with connection.cursor() as cursor:
                cursor.execute(display_table_query)
                data = cursor.fetchall()
                print(data)
    
    

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/doctor')
def doc():
    username = request.args.get('username', 'Guest')
    
    try:
        with connect(
            host="localhost",
            user="root",
            password="ish21072004#",
            database="hms"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                        #display to that particular doctor
                        'select name,age,gender,description from appointments_requests where doc_name = %s',(username,)
                    )
                patients = cursor.fetchall()
                print(patients)
                return render_template('doctor.html',appointments = patients)
    except Error as e:
        print(e)
        return jsonify({'message': 'An error occurred'})
    
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/searchProblem', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
       
        search_query = request.form['search_query']
        print("Search Query:", search_query)
        ml_model(search_query)
        return render_template('home.html', search_query=search_query)
    return render_template('index.html')
@app.route('/details')
def index():
    return render_template('details.html')
@app.route('/accept', methods=['GET', 'POST'])
def accept():
    
    if request.method == 'POST':
       
        date = request.form['dates']
        timing = request.form['times']
        print(date)
        print(timing)
        update_query = """
        UPDATE appointments_requests
        SET timings = %s, dates = %s

        WHERE id = (SELECT max_id FROM (SELECT MAX(id) AS max_id FROM appointments_requests) AS subquery)
        """
        try:
            with connect(
                host="localhost",
                user="root",
                password="ish21072004#",
                database="hms"
            ) as connection:
                with connection.cursor() as cursor:
                    # Retrieve user details using the password provided
                    cursor.execute(update_query, (timing,date))
                    connection.commit()
        except Error as e:
            print(e)
            return jsonify({'message': 'An error occurred'})
        return render_template('doctor.html')
@app.route('/submit', methods=['POST'])
def submit():
    description = request.form['description']
    body_part = request.form['body_part']
    location = request.form['location']
    password = request.form['password']
    
    try:
        with connect(
            host="localhost",
            user="root",
            password="ish21072004#",
            database="hms"
        ) as connection:
            with connection.cursor() as cursor:
                
                # Retrieve user details using the password provided
                cursor.execute("SELECT name, age, gender FROM details_of_users WHERE password = %s", (password,))
                user_data = cursor.fetchone()
                print(user_data)
                if user_data:
                    # Insert appointment request using user details and form data
                    cursor.execute(
                        "INSERT INTO appointments_requests (user_id, name, age, gender, description, bodypart, location) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (password,user_data[0], user_data[1], user_data[2], description, body_part, location)
                    )
                    connection.commit()
                    cursor.execute(
                       'select name from hospitals where location = %s',(location,)
                    )
                    hospital_data = cursor.fetchall()
                    hospital = random.choice(hospital_data[0])
                    print(hospital)
                    cursor.execute(
                        
                        'select doc_name from doctors where hospital = %s and body_part = %s', (hospital,body_part)
                    )
                    doctors = cursor.fetchall()
                    print(random.choice(hospital_data[0]))
                    doctor = random.choice(doctors[0])
                    print(doctor)
                    #leg specialist display leg related appointment requests
                    #same hospital
                   

                    update_query = """
        UPDATE appointments_requests
        SET doc_name = %s, hos_name = %s
        WHERE id = (SELECT max_id FROM (SELECT MAX(id) AS max_id FROM appointments_requests) AS subquery)
        """
                    cursor.execute(
                        update_query,(doctor,hospital)
                       
                    )
                    connection.commit()

                    return jsonify({'message': 'Appointment request submitted successfully'})
                else:
                    return jsonify({'message': 'User not found'})
    except Error as e:
        print(e)
        return jsonify({'message': 'An error occurred'})
    
@app.route('/login_data', methods=['POST'])
def login_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            with connect(
            host="localhost",
            user="root",
            password="ish21072004#",
            database="hms"
        ) as connection:
                with connection.cursor() as cursor:
                # Retrieve user details using the password provided
                    cursor.execute("SELECT doc_name FROM doctors")
                    doctors = cursor.fetchall()
                    print(doctors)
                    for name_tuple in doctors:
                        name = name_tuple[0]
                        if username==name:
                            return redirect(url_for('doc',username=username))
                   
                        
            return render_template('dummy.html')
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('dashboard.html')
@app.route('/home')
def h():
    return render_template('dummy.html')
@app.route('/dashboard')
def dashboard():
    try:
            with connect(
                host="localhost",
                user="root",
                password="ish21072004#",
                database="hms"
            ) as connection:
                with connection.cursor() as cursor:
                    
                    # Retrieve user details using the password provided
                    cursor.execute('SELECT timings, dates, hos_name, doc_name FROM appointments_requests WHERE id = (SELECT max_id FROM (SELECT MAX(id) AS max_id FROM appointments_requests) AS subquery)')
                    app_data = cursor.fetchall()
                    print(app_data)
                    import datetime
                    

                   

                    formatted_time = (datetime.datetime.min + app_data[0][0]).time().strftime('%H:%M:%S')
                    formatted_date = app_data[0][1].strftime('%Y-%m-%d')
                    data = (formatted_time, formatted_date, app_data[0][2], app_data[0][3])

                   

                    # data = [(datetime.datetime.min + app_data[0][0]).time().strftime('%H:%M:%S'), app_data[0][1].strftime('%Y-%m-%d'), app_data[0][2], app_data[0][3]]

                    

                    print(data)
                    
    except Error as e:
            print(e)
            return jsonify({'message': 'An error occurred'})
        
    return render_template('dashboard.html',appointments = data)


@app.route('/submitData', methods=['POST'])
def submit_data():
        
    try:
        expenses = request.form['expenses']
        profit = request.form['profit']
        with connect(
            host="host",
            user="user",
            password="password",
            database = "database"
        ) as connection:
            insert_table_query = """
    INSERT INTO shop_data (expenses, profit) VALUES (%s, %s)

    """
            data = (expenses, profit)
            with connection.cursor() as cursor:
                cursor.execute(insert_table_query,data)
                connection.commit()
    except Error as e:
        print(e)
    
    

    return jsonify({'message': 'Data inserted successfully'})

@app.route('/getData', methods=['GET'])
def get_data():
        
    try:
       
        with connect(
            host="host",
            user="user",
            password="password",
            database = "database"
        ) as connection:
            display_table_query = """
    SELECT * FROM shop_data

    """
            
            with connection.cursor() as cursor:
                cursor.execute(display_table_query)
                data = cursor.fetchall()
                print(data)
    except Error as e:
        print(e)
    return jsonify({'data': data})

def ml_model(query):
    import spacy
    from textblob import TextBlob

    # Load spaCy's English model
    nlp = spacy.load('en_core_web_sm')

    # Sample text
    text = query

    # Process the text with spaCy
    doc = nlp(text)

    # Extract relevant keywords (e.g., body parts and conditions)
    keywords = []
    for ent in doc.ents:
        if ent.label_ in ('BODY_PART', 'SYMPTOM', 'DISEASE', 'CONDITION'):
            keywords.append(ent.text)

    # Analyze sentiment to infer severity score
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    # Define severity based on sentiment score
    # This is a simple heuristic; you can adjust the thresholds as needed
    if sentiment_score < -0.5:
        severity = 'high'
    elif sentiment_score < 0:
        severity = 'moderate'
    else:
        severity = 'low'

    # Output the result
    if 'knee' in keywords and 'pain' in text:
        print(f"Keyword: knee pain, Severity: {severity}")
    else:
        print("No relevant keywords found.")


    #your ml code goes here
    #you can pass the 'data' fetched from the above table as an input argument by defining parameters in the declaration
    pass

if __name__ == '__main__':
    app.run(debug=True)