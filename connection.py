import mysql.connector as mc

def connect():
    return mc.connect(host="localhost",
                        user="root",
                        passwd="",
                        database="ta")