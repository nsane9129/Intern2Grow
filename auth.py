from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = '' 


users = [
    {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
    {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
]

@app.route('/')
def index():
    return 'Welcome to the Home Page'


# Check if the user is logged in for certain routes
def login_required(route_function):
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return route_function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username is unique
        if any(user['username'] == username for user in users):
            return render_template('signup.html', error='Username is already taken.')

        # Add the new user to the list (in a production scenario, you would hash the password)
        users.append({'username': username, 'email': email, 'password': password})

        # Redirect to login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        if user:
            # Set session variable to indicate user is logged in
            session['username'] = username
            return render_template('profile.html',user=user)
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

@app.route('/profile', endpoint='profile')
@login_required
def profile():
    # Fetch user data from session
    username = session['username']
    user = next((user for user in users if user['username'] == username), None)
    return render_template('profile.html', user=user)


@app.route('/logout')
@login_required
def logout():
    # Clear the session to log out the user
    session.clear()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
