import os

'''
an init file is required for this folder to be considered as a module
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from . import database, user, listing, wallet, review, transaction, booking

from qbay.database import db

db.create_all()
