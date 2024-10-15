import os
from dotenv import load_dotenv

load_dotenv()

dbname=os.getenv("dbname")
user=os.getenv("user")
password=os.getenv("password")
host=os.getenv("host")
port=os.getenv("port")