import mysql. connector

dataBase = mysql.connector.connect(
    host="localhost", 
    user="Dennis",
    passwd="Dennis_999.com",
    )

#cursor object
cursorObject = dataBase.cursor()

#create a database
cursorObject.execute("CREATE DATABASE attend")

print ("database created")