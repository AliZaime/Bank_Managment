import mysql.connector as my
from Models import *
from decimal import Decimal

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




class UserDao:
    def __init__(self)->None:
        self.cnx = Database.get_connection()
        
    def getUsers(self)->list[User]:
        users:list[User]=[]
        query = "SELECT * FROM users;"
        if self.cnx != None :
            cursor=self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query)
            rows=cursor.fetchall()
            for row in rows : # type: ignore
                users.append(User(username=row['username'],email=row['email'],password=row['password'],isadmin=row['isadmin'])) # type: ignore
        return users
    
    def auth(self,login:str,password:str)->User|None:
        query = "SELECT * FROM users WHERE email = %s AND password = %s;"
        if self.cnx != None :
            cursor=self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query,(login,password))
            row=cursor.fetchone()
            if row != None:
                return User(username=row['username'],email=row['email'],password=row['password'],isadmin=row['isadmin']) # type: ignore
            return None



class SavingAccountDao:
    def __init__(self) -> None:
        self.cnx = Database.get_connection()

    def create_saving_account(self, balance: float, interestRate: float) -> int:
        query = """
        INSERT INTO saving_accounts (balance, interest_rate)
        VALUES (%s, %s);
        """
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (balance, interestRate))
            self.cnx.commit()
            return cursor.lastrowid  # type: ignore 
        return -1

    def getAllSavingAccounts(self) -> list[SavingAccount]:
        accounts: list[SavingAccount] = []
        query = "SELECT * FROM saving_accounts;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                # S'assurer que le constructeur SavingAccount reçoit les bons arguments
                account=SavingAccount(interestRate=row['interest_rate'],balance=row['balance']) # type: ignore
                account.account_id = row["id"]   # type: ignore # Utiliser les bons attributs
                accounts.append(account)
        return accounts

    def getSavingAccount(self, id: int) -> SavingAccount | None:
        query = "SELECT * FROM saving_accounts WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row:
                # Créer un objet SavingAccount avec les bons arguments
                account = SavingAccount(interestRate=row['interest_rate'],balance=row['balance']) # type: ignore
                account.account_id = row["id"] # type: ignore
                return account
        return None

    def update_balance(self, account_id: int, new_balance: float) -> None:
        query = "UPDATE saving_accounts SET balance = %s WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (new_balance, account_id))
            self.cnx.commit()
            
    def update_account(self, account_id: int, new_balance: float, new_interestRate: float) -> None:
        query = "UPDATE saving_accounts SET balance = %s, interest_rate = %s WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (new_balance, new_interestRate, account_id))  # Corrigé l'ordre des paramètres
            self.cnx.commit()
        

    def delete_saving_account(self, account_id: int) -> None:
        query = "DELETE FROM saving_accounts WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (account_id,))
            self.cnx.commit()

class CheckingAccountDao:
    def __init__(self) -> None:
        self.cnx = Database.get_connection()

    def create_checking_account(self, balance: float) -> int:
        query = "INSERT INTO checking_accounts (balance) VALUES (%s);"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (balance,))
            self.cnx.commit()
            return cursor.lastrowid # type: ignore
        return -1

    def getAllCheckingAccounts(self) -> list[CheckingAccount]:
        accounts: list[CheckingAccount] = []
        query = "SELECT * FROM checking_accounts;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                # Créer un objet CheckingAccount avec les bons arguments
                account = CheckingAccount(balance=row['balance']) # type: ignore
                account.account_id = row["id"] # type: ignore
                accounts.append(account)
        return accounts

    def getCheckingAccount(self, account_id: int) -> CheckingAccount | None:
        query = "SELECT * FROM checking_accounts WHERE id = %s;"
        account = None
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True)
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()
            if result:
                # Créer un objet CheckingAccount avec les bons arguments
                account = CheckingAccount(balance=result['balance']) # type: ignore
                account.account_id = result["id"] # type: ignore
        return account

    def update_balance(self, account_id: int, new_balance: float) -> None:
        query = "UPDATE checking_accounts SET balance = %s WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (new_balance, account_id))
            self.cnx.commit()
            
    def delete_checking_account(self, account_id: int) -> None:
        query = "DELETE FROM checking_accounts WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (account_id,))
            self.cnx.commit()
            
            

class TransactionDao:
    def __init__(self) -> None:
        self.cnx = Database.get_connection()
        
    def create_transaction(self, account_id: int, account_type: str, transaction_type: str, amount: float):
        """Créer une transaction."""
        query = """
                INSERT INTO transactions (account_id, account_type, transaction_type, amount)
                VALUES (%s, %s, %s, %s)
                """
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (account_id, account_type, transaction_type, amount))
            self.cnx.commit()
if __name__ == "__main__":
    database:Database = Database()
    database.get_connection()
            
        
            
            
