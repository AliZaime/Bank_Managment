from myapp.Models.accountModel import * 
from myapp.Dal.cnxDal import Database
from myapp.Dal.userDal import UserDao 

class SavingAccountDao:
    def __init__(self) -> None:
        self.cnx = Database.get_connection()
        

    def create_saving_account(self, balance: float, interestRate: float,userID:int) -> int:
        query = """
        INSERT INTO saving_accounts (balance, interest_rate, userid) 
        VALUES (%s, %s, %s);
        """
        lst_user = UserDao().getusers()
        if(any(user['id'] == userID  and user['isadmin'] != 1 for user in lst_user)):# type: ignore
            if self.cnx is not None:
                cursor = self.cnx.cursor()
                cursor.execute(query, (balance, interestRate, userID))
                self.cnx.commit()
                return cursor.lastrowid  # type: ignore 
        return -1

    def getAllSavingAccounts(self) -> list[SavingAccount]:
        accounts: list[SavingAccount] = []
        query = "SELECT * FROM saving_accounts;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows: # type: ignore
                account=SavingAccount(interestRate=row['interest_rate'],balance=row['balance']) # type: ignore
                account.account_id = row['id']   # type: ignore # Utiliser les bons attributs
                accounts.append(account)
        return accounts

    def getSavingAccount(self, id: int) -> SavingAccount | None:
        query = "SELECT * FROM saving_accounts WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row:
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

    def create_checking_account(self, balance: float,userID:int) -> int:
        query = "INSERT INTO checking_accounts (balance, userID) VALUES (%s, %s);"
        
        lst_user = UserDao().getusers()
        if(any(user['id'] == userID  and user['isadmin'] != 1 for user in lst_user)):# type: ignore
            if self.cnx is not None:
                cursor = self.cnx.cursor()
                cursor.execute(query, (balance,userID))
                self.cnx.commit()
                return cursor.lastrowid # type: ignore
        return -1

    def getAllCheckingAccounts(self) -> list[CheckingAccount]:
        accounts: list[CheckingAccount] = []
        query = "SELECT * FROM checking_accounts;"
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows: # type: ignore
                account = CheckingAccount(balance=row['balance']) # type: ignore
                account.account_id = row["id"] # type: ignore
                account.transaction_count = row["transaction_count"]# type: ignore
                accounts.append(account)
        return accounts

    def getCheckingAccount(self, account_id: int) -> CheckingAccount | None:
        query = "SELECT * FROM checking_accounts WHERE id = %s;"
        account = None
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()
            if result:
                account = CheckingAccount(balance=result['balance']) # type: ignore
                account.account_id = result["id"] # type: ignore
                account.transaction_count = result["transaction_count"]# type: ignore
        return account

    def update_balance(self, account_id: int, new_balance: float) -> None:
        query = "UPDATE checking_accounts SET balance = %s WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            cursor.execute(query, (new_balance, account_id))
            self.cnx.commit()
    
    
    def update_transaction_count(self, account_id: int, new_transaction_count: int) -> None:
        query = "UPDATE checking_accounts SET transaction_count = %s WHERE id = %s;"
        if self.cnx is not None:
            cursor = self.cnx.cursor()
            try:
                cursor.execute(query, (new_transaction_count, account_id))
                self.cnx.commit()  # Validation des modifications
            except Exception as e:
                print(f"Erreur lors de la mise à jour de transaction_count : {e}")
                self.cnx.rollback()  # Annule les modifications en cas d'erreur
    
    
            
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
            
    def log_saving_transaction(self, account_id: int):
        query = """
                SELECT * FROM transactions WHERE account_id = %s AND account_type = %s
                """
        transactionss = []        
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query, (account_id, "Saving"))
            
            transactions = cursor.fetchall()
            
            for transaction in transactions: # type: ignore
                transactionn = Transactions(id=transaction['id'], account_id=transaction['account_id'], account_type=transaction['account_type'], transaction_type=transaction['transaction_type'], amount=transaction['amount'], transaction_date=transaction['transaction_date'])# type: ignore
                transactionss.append(transactionn)
        return transactionss       
                    
    def log_checking_transaction(self, account_id: int):
        query = """
                SELECT * FROM transactions WHERE account_id = %s AND account_type = %s
                """
        transactionss = []        
        if self.cnx is not None:
            cursor = self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query, (account_id, "Checking"))
            
            # Récupère toutes les transactions qui correspondent à la requête
            transactions = cursor.fetchall()
            
            for transaction in transactions: # type: ignore
                # Créer un objet CheckingAccount avec les bons arguments
                transactionn = Transactions(id=transaction['id'], account_id=transaction['account_id'], account_type=transaction['account_type'], transaction_type=transaction['transaction_type'], amount=transaction['amount'], transaction_date=transaction['transaction_date'])# type: ignore
                transactionss.append(transactionn)
        return transactionss
            

                   
if __name__ == "__main__":
    database:Database = Database()
    database.get_connection()
    savingaccount = SavingAccountDao()
    print(savingaccount.getAllSavingAccounts())   
        
             
            
