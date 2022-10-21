from qbay import *
from qbay.database import app
from qbay.controllers import *

FLASK_PORT = 8000

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)