from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "ugahacks_secret"

# Mock database to store "applications"
applications = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        flash(f"Account created for {email}!", "success")
        return redirect(url_for('apply'))
    return render_template('signup.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # Collect all form data
        data = request.form.to_dict()
        applications.append(data)
        return redirect(url_for('success'))
    return render_template('apply.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    print("🚀 Demo site running at http://localhost:5000")
    app.run(port=5000, debug=True)
