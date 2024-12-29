from abc import ABC, abstractmethod
import datetime
from typing import Final
from dataclasses import dataclass
from decimal import Decimal

class BankAccount(ABC):
    
    def __init__(self, balance: float = 0.0) -> None:
        self.balance = balance
        self.account_id = None
    
    def deposit(self, amount: float) -> float:
        self.balance += Decimal(str(amount))
        return self.balance  # Retourner le nouveau solde après dépôt
    
    @abstractmethod
    def withdraw(self, amount: float) -> float:
        pass
    
    def transfer(self, amount: float, other: 'BankAccount') -> float:
        withdraw_amount = self.withdraw(amount)
        other.deposit(withdraw_amount)
        return self.balance  # Retourner le solde actuel après transfert


class SavingAccount(BankAccount):
    SAVING_AMOUNT: Final[float] = 100
    
    def __init__(self, interestRate: float, balance: float) -> None:
        if balance >= SavingAccount.SAVING_AMOUNT:
            super().__init__(balance)
            self.interestRate = interestRate
        else:
            print("account not created")
            return None  

    def withdraw(self, amount: float) -> float:
        if self.balance - Decimal(str(amount)) >= SavingAccount.SAVING_AMOUNT:
            self.balance -= Decimal(str(amount))
            return self.balance  # Retourner le solde restant après retrait
        available_amount = self.balance - SavingAccount.SAVING_AMOUNT
        self.balance = SavingAccount.SAVING_AMOUNT
        return available_amount

    def addPeriodicInterest(self) -> float:
        interest: float = self.balance * self.interestRate
        self.balance += Decimal(str(interest))
        return self.balance  # Retourner le solde après ajout des intérêts


class CheckingAccount(BankAccount):
    FREE_TRANSACTIONS: Final[int] = 3
    TRANSACTION_FEE: Final[float] = 0.2
    DRAFT_OVER: Final[float] = 500
    
    def __init__(self, balance: float = 0) -> None:
        super().__init__(balance)
        self.transaction_count = 0
    
    def deposit(self, amount: float) -> float:
        self.transaction_count += 1
        self.balance = super().deposit(amount)
        return self.balance  # Retourner le solde après dépôt
    
    def transfer(self, other: BankAccount, amount: float) -> float:
        self.transaction_count += 1
        self.balance = super().transfer(amount, other)
        return self.balance  # Retourner le solde après transfert
    
    def withdraw(self, amount: float) -> float:
        if self.balance + CheckingAccount.DRAFT_OVER - amount >= 0:
            self.balance -= Decimal(str(amount))
            return self.balance  # Retourner le solde restant après retrait
        available_amount = self.balance + CheckingAccount.DRAFT_OVER
        self.balance = -CheckingAccount.DRAFT_OVER
        self.transaction_count += 1
        return available_amount  # Retourner l'argent disponible
    
    def deductFees(self) -> float:
        fees: float = 0
        if self.transaction_count > CheckingAccount.FREE_TRANSACTIONS:
            fees = (self.transaction_count - CheckingAccount.FREE_TRANSACTIONS) * CheckingAccount.TRANSACTION_FEE
            self.balance -= Decimal(str(fees))
            self.transaction_count = 0
        return self.balance  # Retourner le solde après déduction des frais
      
@dataclass
class User:
    username:str
    email:str
    password:str
    isadmin:bool 
    
    
