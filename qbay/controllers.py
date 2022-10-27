from distutils.log import error
from flask import render_template, request, session, redirect
from qbay.user import User
from qbay.listing import Listing
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
    listings = database.Listing



    return render_template('index.html', user=user, listings=listings)


@app.route('/create_listing', methods=['GET'])
def create_listing_get():
    return render_template('create_listing.html', message='')


@app.route('/create_listing', methods=['POST'])
@authenticate
def create_listing_post(user):
    title = request.form.get('title')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    print(price)

    try:
        print(type(price))
        Listing.valid_price(price)
        print("3")
        Listing.valid_seller(user)
        print("4")
        Listing.create_listing(title, description, int(price), user)
        database.db.session.commit()
    except ValueError as e:
        print("no")
        return render_template('create_listing.html', message=str(e))
    except TypeError as e:
        print("nope")
        return render_template('create_listing.html', message=str(e))

    return redirect('/')


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = User.register(username, email, password)
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
def update_informations_get(user : User):
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


@app.route('/listing_update', methods=['GET'])
def update_listing_get(listing : Listing):
    return render_template('/listing_update.html',
                        listing=listing,
                        errors='')


@app.route('/listing_update', methods=['POST'])
def update_listing_post(user : User, listing : Listing):
    
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')

    error_messages = []

    try:
        listing.update_title(title)
        error_messages += [f"Title updated successfully: {title}"]
    except ValueError as e:
        error_messages += [str(e)]

    try:
        listing.update_description(description)
        error_messages += [f"Description updated successfully: {description}"]
    except ValueError as e:
        error_messages += [str(e)]

    try:
        listing.update_price(price)
        error_messages += [
            f"Price updated successfully: {price}"]
    except ValueError as e:
        error_messages += [str(e)]

    database.db.session.commit()

    return render_template('/listing_update.html',
                           listing=listing,
                           errors=error_messages)
