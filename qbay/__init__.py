import os

'''
an init file is required for this folder to be considered as a module
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from qbay.database import db