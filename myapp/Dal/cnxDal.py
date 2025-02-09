import mysql.connector as my

class Database:
    cnx = None

    @staticmethod
    def get_connection():
        if Database.cnx is None:
            try:
                Database.cnx = my.connect(
                    user='root',
                    password='',
                    host='localhost',
                    port='3306',
                    database='db_bank'
                )
                print('Connection Ok')
            except:
                print('Connection Error')
                return None
        return Database.cnx