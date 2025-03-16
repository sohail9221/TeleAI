# from flask import Flask, render_template, request, redirect, url_for
# import mysql.connector

# app = Flask(__name__)

# # MySQL Database Connection
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Passw0rd!",
#     database="DamaSquinoDB"
# )
# cursor = conn.cursor()

# # Route for Home Page
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Route for Login Page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         username = request.form['email']
#         password = request.form['password']
        
#         # Check user in database
#         cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (username, password))
#         user = cursor.fetchone()
        
#         if user:
#             return redirect(url_for('dashboard'))
#         else:
#             error = "Invalid credentials, please try again."
    
#     return render_template('login.html', error=error)

# # Route for Dashboard Page
# @app.route('/dashboard')
# def dashboard():
#     return render_template('admin_dashboard.html')

# # Route for Orders Page
# @app.route('/orders')
# def orders():
#     cursor.execute("SELECT * FROM Orders")
#     orders_data = cursor.fetchall()
#     return render_template('orders.html', orders=orders_data)

# # Route for Reservations Page
# @app.route('/reservations')
# def reservations():
#     return render_template('reservations.html')

# # Route for Customers Page
# @app.route('/customers')
# def customers():
#     return render_template('customers.html')


# # Route for Signup Page
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     error = None
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         role  = request.form['role']
#         # Check if email already exists
#         cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
#         existing_user = cursor.fetchone()
        
#         if existing_user:
#             error = "Email already exists! Please log in."
#         else:
#             # Insert new user into database
#             cursor.execute("INSERT INTO Users (name, email, password,role) VALUES (%s, %s, %s,%s)", (name, email, password,role))
#             conn.commit()
#             return redirect(url_for('login'))
    
#     return render_template('admin_signup.html', error=error)

# # Route for Feedback Page
# @app.route('/feedback')
# def feedback():
#     return render_template('feedback.html')

# @app.route('/menu')
# def menu():
#     return render_template('menu.html')

# @app.route('/settings')
# def settings():
#     return render_template('settings.html')

# if __name__ == '__main__':
#     app.run(debug=True)







from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Passw0rd!",
    database="CulinaryAI"
)
cursor = conn.cursor()

# Route for Home Page
@app.route('/')
def home():
    return render_template('index.html')


## Twillio Api Calls


   
@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming calls with a prompt for speech input."""
    response = VoiceResponse()

    # Create a Gather verb to collect speech input
    gather = Gather(
        input='speech',
        action='/process_speech',
        method='POST',
        speechTimeout='auto',
        speechModel='experimental_conversations',
        enhanced=True
    )

    # Prompt the user to say something
    gather.say("Hello! Please say something, and I will repeat it back to you.")

    # Append the Gather verb to the response
    response.append(gather)

    # If no speech input is detected, provide a fallback message
    response.say("We didn't receive any input. Goodbye!")

    return str(response)

@app.route("/process_speech", methods=['POST'])
def process_speech():
    """Process the user's speech input and repeat it back."""
    # Retrieve the speech input from the request
    user_speech = request.form.get('SpeechResult')

    response = VoiceResponse()

    if user_speech:
        # Repeat back the user's speech
        response.say(f"You said: {user_speech}")
    else:
        # Inform the user that no speech was detected
        response.say("Sorry, I didn't catch that.")

    return str(response)


##  twillio code ends here 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role  = request.form['role']
        phone = request.form['phone']
        # Check if email already exists
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            error = "Email already exists! Please log in."
        else:
            # Insert new user into database
            cursor.execute("INSERT INTO Users (name, email, password,role,phone) VALUES (%s, %s, %s,%s,%s)", (name, email, password,role,phone))
            conn.commit()
            return redirect(url_for('dashboard'))
    
    return render_template('admin_signup.html', error=error)
# # Route for Customers Page
@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Route for Login Page (Kept unchanged)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        
        # Check user in database
        cursor.execute("SELECT * FROM Users WHERE email = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        if user:
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid credentials, please try again."
    
    return render_template('login.html', error=error)

# Route for Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('admin_dashboard.html')

# Route for Orders Page (Fetching data)
@app.route('/orders')
def orders():
    cursor.execute("SELECT o.id, u.name, o.status, o.total_price, o.payment_method FROM Orders o JOIN Users u ON o.user_id = u.id")
    orders_data = cursor.fetchall()
    return render_template('orders.html', orders=orders_data)

# Route for Reservations Page (Fetching data)
@app.route('/reservations')
def reservations():
    cursor.execute("SELECT r.id, u.name, r.reservation_time, r.guests, r.table_number, r.status FROM Reservations r JOIN Users u ON r.user_id = u.id")
    reservations_data = cursor.fetchall()
    return render_template('reservations.html', reservations=reservations_data)

# Route for Menu Page (Fetching data)
@app.route('/menu')
def menu():
    cursor.execute("SELECT id, name, description, price, category, availability FROM Menu")
    menu_data = cursor.fetchall()
    return render_template('menu.html', menu=menu_data)

if __name__ == '__main__':
    app.run(debug=True)
