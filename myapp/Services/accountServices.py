from myapp.Dal.accountsDal import *



class SavingAccountService:
    def __init__(self) -> None:
        self.dao = SavingAccountDao()
        self.transaction_dao = TransactionDao()

    def create_account(self, balance: float, interest_rate: float,userID:int) -> int:
        """Créer un compte d'épargne."""
        if balance < SavingAccount.SAVING_AMOUNT:
            raise ValueError("Le solde doit être supérieur ou égal à 100.")
        
        account_id = self.dao.create_saving_account(balance, interest_rate,userID)
        if(account_id == -1):
            return -1    
        return account_id
    
    def getAllSavingAccounts(self) -> list[SavingAccount]:
        """
        Récupère tous les comptes épargne.
        """
        try:
            accounts = self.dao.getAllSavingAccounts()
            if accounts:
                return accounts
            else:
                print("No saving accounts found.")
                return []
        except Exception as e:
            print(f"Error fetching saving accounts: {e}")
            return []
    
    
    def getSavingAccount(self, account_id: int) -> SavingAccount | None:
        try:
            account = self.dao.getSavingAccount(account_id)
            if account:
                return account
            else:
                print(f"Saving account with ID {account_id} not found.")
                return None
        except Exception as e:
            print(f"Error fetching saving account with ID {account_id}: {e}")
            return None
        
    def update_account_balance(self, account_id: int, new_balance: float, new_interestRate:float) -> None:
        if new_balance < 0:
            raise ValueError("Le solde doit être positif.")
        
        self.dao.update_account(account_id, new_balance, new_interestRate) 
        
    def delete_account(self, account_id: int) -> None:
        self.dao.delete_saving_account(account_id)     

    def deposit(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être supérieur à 0.")
        
        account = self.dao.getSavingAccount(account_id)
        if not account:
            raise ValueError("Compte d'épargne introuvable.")
        
        new_balance = account.deposit(amount)
        
        self.dao.update_balance(account_id, new_balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Saving',
            transaction_type='Deposit',
            amount = amount
        )
        
        return new_balance

    def withdraw(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être supérieur à 0.")
        
        account = self.dao.getSavingAccount(account_id)
        if not account:
            raise ValueError("Compte d'épargne introuvable.")
        
        new_balance = account.withdraw(amount)
        
        self.dao.update_balance(account_id, new_balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Saving',
            transaction_type='Withdraw',
            amount= amount
        )
        
        return new_balance
    
    def transfer(self, source_account_id: int, target_account_id: int, amount: float):
        
        if amount <= 0:
            raise ValueError("Le montant du transfert doit être supérieur à 0.")
        
        source_account = self.dao.getSavingAccount(source_account_id)
        target_account = self.dao.getSavingAccount(target_account_id)
        
        if not source_account:
            raise ValueError("Compte source d'épargne introuvable.")
        
        if not target_account:
            raise ValueError("Compte destinataire d'épargne introuvable.")
        
        
        source_account.transfer(amount,target_account)
        print("from services",amount)
        self.dao.update_balance(source_account_id, source_account.balance)
        self.dao.update_balance(target_account_id, target_account.balance)
        
        self.transaction_dao.create_transaction(
            account_id=source_account_id,
            account_type='Saving',
            transaction_type='Transfer Out',
            amount=amount
        )
        
        self.transaction_dao.create_transaction(
            account_id=target_account_id,
            account_type='Saving',
            transaction_type='Transfer In',
            amount=amount
        )
        


    def add_periodic_interest(self, account_id: int) -> float:
        account = self.dao.getSavingAccount(account_id)
        if not account:
            raise ValueError("Compte d'épargne introuvable.")
        
        interest = account.addPeriodicInterest()
        
        self.dao.update_balance(account_id, account.balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Saving',
            transaction_type='Interest',
            amount= interest
        )
        
        return interest
    
    
    def log_account(self, account_id:int)->list:
        try:
            accounts = self.transaction_dao.log_saving_transaction(account_id)
            return accounts
        except Exception as e:
            print(f"Error fetching checking accounts: {e}")
            return []

class CheckingAccountService:
    def __init__(self) -> None:
        self.dao = CheckingAccountDao()
        self.transaction_dao = TransactionDao()

    def create_account(self, balance: float,userID:int) -> int:
        if balance < 0:
            raise ValueError("Le solde initial doit être positif.")
        
        account_id = self.dao.create_checking_account(balance,userID)
        if(account_id == -1):
            return -1  
        return account_id
    
    def getAllCheckingAccounts(self) -> list[CheckingAccount]:
        try:
            accounts = self.dao.getAllCheckingAccounts()
            return accounts
        except Exception as e:
            print(f"Error fetching checking accounts: {e}")
            return []
    
    def getCheckingAccount(self, account_id: int) -> CheckingAccount | None:
        try:
            account = self.dao.getCheckingAccount(account_id)
            if account:
                return account
            else:
                print(f"Account with ID {account_id} not found.")
                return None
        except Exception as e:
            print(f"Error fetching account with ID {account_id}: {e}")
            return None 
        
    def update_account_balance(self, account_id: int, new_balance: float) -> None:
        if new_balance < 0:
            raise ValueError("Le solde doit être positif.")
        
        self.dao.update_balance(account_id, new_balance) 
        
    def delete_account(self, account_id: int) -> None:
        self.dao.delete_checking_account(account_id)          

    def deposit(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être supérieur à 0.")
        
        account = self.dao.getCheckingAccount(account_id)
        if not account:
            raise ValueError("Compte courant introuvable.")
        
        new_balance = account.deposit(amount)
        
        self.dao.update_balance(account_id, new_balance)
        self.dao.update_transaction_count(account_id, account.transaction_count)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Checking',
            transaction_type='Deposit',
            amount= amount
        )
        
        return new_balance

    def withdraw(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être supérieur à 0.")
        
        account = self.dao.getCheckingAccount(account_id)
        if not account:
            raise ValueError("Compte courant introuvable.")
        
        new_balance = account.withdraw(amount)
        
        self.dao.update_balance(account_id, new_balance)
        self.dao.update_transaction_count(account_id, account.transaction_count)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Checking',
            transaction_type='Withdraw',
            amount= amount
        )
        
        return new_balance

    def transfer(self, account_id_from: int, account_id_to: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Le montant du virement doit être supérieur à 0.")
        
        account_from = self.dao.getCheckingAccount(account_id_from)
        account_to = self.dao.getCheckingAccount(account_id_to)
        
        if not account_from or not account_to:
            raise ValueError("L'un des comptes n'a pas été trouvé.")
        
        withdrawn_amount = account_from.transfer(account_to, amount)
        
        self.dao.update_balance(account_id_from, account_from.balance)
        self.dao.update_transaction_count(account_id_from, account_from.transaction_count)
        self.dao.update_balance(account_id_to, account_to.balance)
        self.dao.update_transaction_count(account_id_to, account_to.transaction_count)
        
        self.transaction_dao.create_transaction(
            account_id=account_id_from,
            account_type='Checking',  # Type de compte
            transaction_type='transfer out',
            amount= amount
        )
        
        self.transaction_dao.create_transaction(
            account_id=account_id_to,
            account_type='Checking',  # Type de compte
            transaction_type='transfer in',
            amount= amount
        )
        
        return withdrawn_amount

    def deduct_fees(self, account_id: int) -> float:
        account = self.dao.getCheckingAccount(account_id)
        if not account:
            raise ValueError("Compte courant introuvable.")
        
        if(account.transaction_count > CheckingAccount.FREE_TRANSACTIONS):
            fees = account.deductFees()
        
            self.dao.update_balance(account_id, account.balance)
        
            self.transaction_dao.create_transaction(
                account_id=account_id,
                account_type='Checking',
                transaction_type='Fee',
                amount= fees
            )
            
            return fees
        return -1
    
    def log_account(self, account_id:int)->list:
        try:
            accounts = self.transaction_dao.log_checking_transaction(account_id)
            return accounts
        except Exception as e:
            print(f"Error fetching checking accounts: {e}")
            return []
        
