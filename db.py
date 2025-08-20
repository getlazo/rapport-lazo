import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="tempted-db-usa.ckdg6yuue48n.us-east-1.rds.amazonaws.com",
        port=3306,
        user="tempted",
        password=os.getenv("MYSQL_PASSWORD"),
        database="production"
    )
