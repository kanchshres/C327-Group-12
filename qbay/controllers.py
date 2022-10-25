from flask import render_template, request, session, redirect
from qbay.user import User
from qbay import database
from qbay.database import app
import sys

from functools import wraps


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    @wraps(inner_function)
    def wrapped_inner():
        # check did we store the key in the session
        if 'logged_in' in session:
            id = session['logged_in']
            try:
                # This generates a new User object that can interact with
                # the database via some tethering.
                # You want to use this object to pass around the program as it
                # has the needed functions for actually managing the database
                user = User.query_user(id)
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
                return redirect('/login')
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = User.login(email, password)
    except ValueError as err:
        return render_template('login.html', message=err)

    if user:
        session['logged_in'] = user.id
        """
        Session is an object that contains sharing information 
        between a user's browser and the end server. 
        Typically it is packed and stored in the browser cookies. 
        They will be past along between every request the browser made 
        to this services. Here we store the user object into the 
        session, so we can tell if the client has already login 
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # Fetch listings from database
    # Fake listings for now
    listings = [
        {'name': 'listing 1', 'price': 10},
        {'name': 'listing 2', 'price': 20},
        {'name': 'listing 3', 'price': 30}
    ]

    return render_template('index.html', user=user, listings=listings)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = User.register(name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/user_update', methods=['GET'])
@authenticate
def update_informations_get(user):
    return render_template('/user_update.html',
                           user=user,
                           errors='')


@app.route('/user_update', methods=['POST'])
@authenticate
def update_informations_post(user: User):
    """Update the user information from the HTML page
    and push it onto the database
    """
    username = request.form.get('username')
    email = request.form.get('email')
    billing_address = request.form.get('billing_address')
    postal_code = request.form.get('postal_code')

    error_messages = []

    try:
        user.update_username(username)
        error_messages += [f"Username updated successfully: {username}"]
    except ValueError as e:
        error_messages += [str(e)]

    try:
        user.update_email(email)
        error_messages += [f"Email updated successfully: {email}"]
    except ValueError as e:
        error_messages += [str(e)]

    try:
        user.update_billing_address(billing_address)
        error_messages += [
            f"Billing address updated successfully: {billing_address}"]
    except ValueError as e:
        error_messages += [str(e)]

    try:
        user.update_postal_code(postal_code)
        error_messages += [f"Postal code updated successfully: {postal_code}"]
    except ValueError as e:
        error_messages += [str(e)]
    database.db.session.commit()

    return render_template('/user_update.html',
                           user=user,
                           errors=error_messages)
