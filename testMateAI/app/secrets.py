from cryptography.fernet import Fernet
import os
key = ""
# Set the environment variable
os.environ['SECRET_KEY'] = key