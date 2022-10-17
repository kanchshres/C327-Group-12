from qbay import *
from qbay import app
from qbay.controllers import *

"""
This file runs the server at a given port
"""

FLASK_PORT = 8000

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)

