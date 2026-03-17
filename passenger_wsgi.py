import sys
import os

# Tell the server where your project files are
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app — GoDaddy Passenger looks for 'application'
from app import app as application
