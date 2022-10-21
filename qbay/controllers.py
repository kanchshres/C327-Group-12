from flask import render_template, request, session, redirect
from qbay.user import User
from qbay import database
from qbay.database import app


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

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = database.User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/')
@authenticate
def home(user):
    products = [
        {'name': 'product 1', 'price': 10},
        {'name': 'product 2', 'price': 20}
    ]
    return render_template('index.html', user=user, products=products)


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
    error_msg = None

    if password != password2:
        error_msg = "The passwords do not match, please retry."
    elif len(database.User.query.filter_by(email=email).all()):
        error_msg = "Email already exists."
    else:
        # Create using backend api where it'll create only after checking if
        # each parameter is valid
        user = User.register(name, email, password)
        if not user:
            error_msg = "Registration failed!"
            if (not User.valid_email(email)):
                error_msg += " Incorrect email."
            if (not User.valid_password(password)):
                error_msg += " Incorrect password."
            if (not User.valid_username(name)):
                error_msg += " Incorrect username."
    # If any error messages are encountered registering new user
    # then go back to the register page.
    if error_msg:
        return render_template('register.html', message=error_msg)
    else:
        return redirect('/login')
