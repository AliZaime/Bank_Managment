from Models import *
from DAL import *

class SavingAccountService:
    def __init__(self) -> None:
        self.dao = SavingAccountDao()
        self.transaction_dao = TransactionDao()

    def create_account(self, balance: float, interest_rate: float) -> int:
        """Créer un compte d'épargne."""
        if balance < SavingAccount.SAVING_AMOUNT:
            raise ValueError("Le solde doit être supérieur ou égal à 100.")
        
        account_id = self.dao.create_saving_account(balance, interest_rate)
        return account_id
    
    def getAllSavingAccounts(self) -> list[SavingAccount]:
        """
        Récupère tous les comptes épargne.
        """
        try:
            accounts = self.dao.getAllSavingAccounts()
            if accounts:
                # Logique métier supplémentaire si nécessaire
                return accounts
            else:
                print("No saving accounts found.")
                return []
        except Exception as e:
            print(f"Error fetching saving accounts: {e}")
            return []
    
    
    def getSavingAccount(self, account_id: int) -> SavingAccount | None:
        """
        Récupère un compte épargne spécifique en fonction de son ID.
        """
        try:
            account = self.dao.getSavingAccount(account_id)
            if account:
                # Logique métier supplémentaire si nécessaire
                return account
            else:
                print(f"Saving account with ID {account_id} not found.")
                return None
        except Exception as e:
            print(f"Error fetching saving account with ID {account_id}: {e}")
            return None
        
    def update_account_balance(self, account_id: int, new_balance: float, new_interestRate:float) -> None:
        """Mettre à jour le solde du compte courant."""
        if new_balance < 0:
            raise ValueError("Le solde doit être positif.")
        
        # Appel à la méthode DAO pour mettre à jour le compte dans la base de données
        self.dao.update_account(account_id, new_balance, new_interestRate) 
        
    def delete_account(self, account_id: int) -> None:
        """Supprimer un compte courant."""
        self.dao.delete_saving_account(account_id)     

    def deposit(self, account_id: int, amount: float) -> float:
        """Effectuer un dépôt sur un compte d'épargne."""
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être supérieur à 0.")
        
        account = self.dao.getSavingAccount(account_id)
        if not account:
            raise ValueError("Compte d'épargne introuvable.")
        
        new_balance = account.deposit(amount)
        
        # Mettre à jour le solde dans la base de données
        self.dao.update_balance(account_id, new_balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Saving',  # Type de compte
            transaction_type='Deposit',
            amount = amount
        )
        
        return new_balance

    def withdraw(self, account_id: int, amount: float) -> float:
        """Effectuer un retrait sur un compte d'épargne."""
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être supérieur à 0.")
        
        account = self.dao.getSavingAccount(account_id)
        if not account:
            raise ValueError("Compte d'épargne introuvable.")
        
        new_balance = account.withdraw(amount)
        
        # Mettre à jour le solde dans la base de données
        self.dao.update_balance(account_id, new_balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Saving',  # Type de compte
            transaction_type='Withdraw',
            amount= amount
        )
        
        return new_balance

    def add_periodic_interest(self, account_id: int) -> float:
        """Ajouter l'intérêt périodique sur un compte d'épargne."""
        account = self.dao.getSavingAccount(account_id)
        if not account:
            raise ValueError("Compte d'épargne introuvable.")
        
        interest = account.addPeriodicInterest()
        
        # Mettre à jour le solde dans la base de données
        self.dao.update_balance(account_id, account.balance)
        
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Saving',  # Type de compte
            transaction_type='Interest',  # Le type de transaction est 'Interest'
            amount= interest  # Le montant est l'intérêt ajouté
        )
        
        return interest

class CheckingAccountService:
    def __init__(self) -> None:
        self.dao = CheckingAccountDao()
        self.transaction_dao = TransactionDao()  # DAO pour enregistrer les transactions

    def create_account(self, balance: float) -> int:
        """Créer un compte courant."""
        if balance < 0:
            raise ValueError("Le solde initial doit être positif.")
        
        account_id = self.dao.create_checking_account(balance)
        return account_id
    
    def getAllCheckingAccounts(self) -> list[CheckingAccount]:
        """
        Récupère tous les comptes courants depuis le DAO et applique une logique métier si nécessaire.
        """
        try:
            accounts = self.dao.getAllCheckingAccounts()
            return accounts
        except Exception as e:
            print(f"Error fetching checking accounts: {e}")
            return []
    
    def getCheckingAccount(self, account_id: int) -> CheckingAccount | None:
        """
        Récupère un compte courant spécifique en fonction de son ID.
        """
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
        """Mettre à jour le solde du compte courant."""
        if new_balance < 0:
            raise ValueError("Le solde doit être positif.")
        
        # Appel à la méthode DAO pour mettre à jour le compte dans la base de données
        self.dao.update_balance(account_id, new_balance) 
        
    def delete_account(self, account_id: int) -> None:
        """Supprimer un compte courant."""
        self.dao.delete_checking_account(account_id)          

    def deposit(self, account_id: int, amount: float) -> float:
        """Effectuer un dépôt sur un compte courant."""
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être supérieur à 0.")
        
        account = self.dao.getCheckingAccount(account_id)
        if not account:
            raise ValueError("Compte courant introuvable.")
        
        new_balance = account.deposit(amount)
        
        # Mettre à jour le solde dans la base de données
        self.dao.update_balance(account_id, new_balance)
        
        # Enregistrer la transaction
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Checking',  # Type de compte
            transaction_type='Deposit',
            amount= amount
        )
        
        return new_balance

    def withdraw(self, account_id: int, amount: float) -> float:
        """Effectuer un retrait sur un compte courant."""
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être supérieur à 0.")
        
        account = self.dao.getCheckingAccount(account_id)
        if not account:
            raise ValueError("Compte courant introuvable.")
        
        new_balance = account.withdraw(amount)
        
        # Mettre à jour le solde dans la base de données
        self.dao.update_balance(account_id, new_balance)
        
        # Enregistrer la transaction
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Checking',  # Type de compte
            transaction_type='Withdraw',
            amount= amount
        )
        
        return new_balance

    def transfer(self, account_id_from: int, account_id_to: int, amount: float) -> float:
        """Effectuer un virement entre deux comptes courants."""
        if amount <= 0:
            raise ValueError("Le montant du virement doit être supérieur à 0.")
        
        account_from = self.dao.getCheckingAccount(account_id_from)
        account_to = self.dao.getCheckingAccount(account_id_to)
        
        if not account_from or not account_to:
            raise ValueError("L'un des comptes n'a pas été trouvé.")
        
        withdrawn_amount = account_from.transfer(account_to, amount)
        
        # Mettre à jour les soldes dans la base de données
        self.dao.update_balance(account_id_from, account_from.balance)
        self.dao.update_balance(account_id_to, account_to.balance)
        
        # Enregistrer les transactions de virement
        self.transaction_dao.create_transaction(
            account_id=account_id_from,
            account_type='Checking',  # Type de compte
            transaction_type='Withdraw',
            amount= amount
        )
        
        self.transaction_dao.create_transaction(
            account_id=account_id_to,
            account_type='Checking',  # Type de compte
            transaction_type='Deposit',
            amount= amount
        )
        
        return withdrawn_amount

    def deduct_fees(self, account_id: int) -> float:
        """Appliquer les frais de transaction sur un compte courant."""
        account = self.dao.getCheckingAccount(account_id)
        if not account:
            raise ValueError("Compte courant introuvable.")
        
        fees = account.deductFees()
        
        # Mettre à jour le solde dans la base de données
        self.dao.update_balance(account_id, account.balance)
        
        # Enregistrer la transaction des frais
        self.transaction_dao.create_transaction(
            account_id=account_id,
            account_type='Checking',  # Type de compte
            transaction_type='Fee',
            amount= fees
        )
        
        return fees

    
class UserManage:
    def __init__(self)->None:
        self.userDao=UserDao()
        
    def listUsers(self)->list[User]:
        return self.userDao.getUsers()
    
    def auth(self,login:str,password:str)->User|None:
        return self.userDao.auth(login,password)    
    


if __name__ == "__main__":
    # Tester SavingAccountService
    print("Test SavingAccountService")
    
    saving_service = SavingAccountService()
    print(saving_service.getSavingAccount(1))
    
    # Créer un compte d'épargne
    try:
        account_id_saving = saving_service.create_account(200, 0.05)
        print(f"Compte d'épargne créé avec l'ID: {account_id_saving}")
    except ValueError as e:
        print(f"Erreur: {e}")

    # Effectuer un dépôt sur le compte d'épargne
    try:
        new_balance = saving_service.deposit(1, 250)
        print(f"Solde après  : {new_balance}")
    except ValueError as e:
        print(f"Erreur: {e}")

    # Effectuer un retrait sur le compte d'épargne
    try:
        new_balance = saving_service.withdraw(1, 250)
        print(f"Solde après retrait: {new_balance}")
    except ValueError as e:
        print(f"Erreur: {e}")

    # Ajouter l'intérêt périodique sur le compte d'épargne
    try:
        interest = saving_service.add_periodic_interest(1)
        print(f"Solde après Intérêt: {interest}")
    except ValueError as e:
        print(f"Erreur: {e}")
        
    """ # Tester CheckingAccountService
    print("\nTest CheckingAccountService")

    checking_service = CheckingAccountService()

    # Créer un compte courant
    try:
        account_id_checking = checking_service.create_account(500)
        print(f"Compte courant créé avec l'ID: {account_id_checking}")
    except ValueError as e:
        print(f"Erreur: {e}")

    # Effectuer un dépôt sur le compte courant
    try:
        new_balance = checking_service.deposit(account_id_checking, 100)
        print(f"Solde après dépôt: {new_balance}")
    except ValueError as e:
        print(f"Erreur: {e}")

    # Effectuer un retrait sur le compte courant
    try:
        new_balance = checking_service.withdraw(account_id_checking, 150)
        print(f"Solde après retrait: {new_balance}")
    except ValueError as e:
        print(f"Erreur: {e}")

    # Effectuer un virement entre deux comptes courants
    try:
        account_id_checking2 = checking_service.create_account(300)
        print(f"Compte courant 2 créé avec l'ID: {account_id_checking2}")

        transferred_amount = checking_service.transfer(account_id_checking, account_id_checking2, 200)
        print(f"Montant transféré: {transferred_amount}")
    except ValueError as e:
        print(f"Erreur: {e}")

    # Appliquer les frais sur un compte courant
    try:
        fees = checking_service.deduct_fees(account_id_checking)
        print(f"Frais appliqués: {fees}")
    except ValueError as e:
        print(f"Erreur: {e}") """


