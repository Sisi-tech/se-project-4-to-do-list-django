import mysql.connector 
import os 
from dotenv import load_dotenv

load_dotenv()


try:
    mydb = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
    )

    mycursor = mydb.cursor()
    mycursor.execute('CREATE DATABASE ToDoList')
    print("Database created successfully")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'mydb' in locals() and mydb.is_connected():
        mydb.close()
        print('Connection closed')
        