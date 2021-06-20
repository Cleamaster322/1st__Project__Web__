import os
import sqlite3
from PIL import Image 
from werkzeug.security import check_password_hash,generate_password_hash

print(generate_password_hash("admin"))

