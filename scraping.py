import pymysql 
import os 
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host= os.getenv("HOST"),
    user= os.getenv("USER"),
    password= os.getenv("PASSWORD"),
    db=os.getenv("DB"),
    cursorclass=pymysql.cursors.DictCursor
)