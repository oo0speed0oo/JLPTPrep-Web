import sys
import os

# This tells the server where your files are
sys.path.insert(0, os.path.dirname(__file__))

# This imports your app from your main.py file
# Note: 'application' is the name GoDaddy looks for
from main import QuizMarkerApp as application