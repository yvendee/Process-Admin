from flask import Flask, request, redirect, url_for, session, render_template, jsonify
from flask_cors import CORS
from functools import wraps
import subprocess

app = Flask("ProcessAdmin")

# Enable CORS
CORS(app)

# Secret key for session management
app.secret_key = 'unique_secret_key_for_processadmin'  # Change this to a secure secret key

# Hardcoded username and password (for demo purposes)
USERNAME = "searchmaid"
PASSWORD = "maidasia"

# Decorator to require login for certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Route to display the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login/login-page.html', error='Invalid username or password.')
    return render_template('login/login-page.html')

# Route to log out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Route to handle root URL redirection
@app.route('/')
def index():
    return redirect(url_for('login'))

# Home route that requires login
@app.route('/home')
@login_required
def home():
    return render_template('home/home-page.html')

@app.route('/run_flask2', methods=['GET'])
@login_required
def run_flask():
    try:
        # Define the command to change directory and run Flask
        command = (
            "cd /home/PDFHarvest2 && "
            "nohup /home/PDFHarvest2/env/bin/python -m flask run -h 0.0.0.0 -p 5000 > ph.logs 2>&1 &"
        )
        
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        
        return jsonify({"status": "success", "message": "Flask application started on port 5000."})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/run_flask3', methods=['GET'])
@login_required
def run_flask2():
    try:
        # Define the command to change directory and run Flask
        command = (
            "cd /home/PDFHarvest3 && "
            "nohup /home/PDFHarvest3/env/bin/python -m flask run -h 0.0.0.0 -p 3000 > ph2.logs 2>&1 &"
        )
        
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        
        return jsonify({"status": "success", "message": "Flask application started on port 3000."})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
