from flask import (Flask,
                   request,
                   render_template,
                   jsonify,
                   abort,
                   session,
                   redirect,
                   url_for,
                   send_file,
                   after_this_request,
                   Blueprint
                   )

bankaccount=Blueprint('bankaccount',__name__)
from myapp.Models.accountModel import *
from myapp.Services.accountServices import *
saving_account_dao:SavingAccountService = SavingAccountService()
checking_account_dao:CheckingAccountService = CheckingAccountService()
from decimal import Decimal
from fpdf import FPDF
from datetime import datetime
import os

@bankaccount.route('/create_saving_account', methods=['POST'])
def create_saving_account():
    balance = request.form['balance']
    interest_rate = request.form['interestRate']
    userID = request.form['userID']
    if(saving_account_dao.create_account(float(balance),float(interest_rate),int(userID))!= -1):
        return redirect(url_for('bankaccount.get_all_saving_accounts'))
    return "Erreur lors de la création du compte", 400
@bankaccount.route('/saving_accounts', methods=['GET'])
def get_all_saving_accounts():
    """Get all saving accounts."""
    accounts = saving_account_dao.getAllSavingAccounts()
    return render_template('saving_accounts.html',saving_accounts=accounts)


@bankaccount.route('/get_saving_account', methods=['GET'])
def get_saving_account():
    account_id = request.args.get('account_id')
    if account_id:
        try:
            account_id = int(account_id)
            account = saving_account_dao.getSavingAccount(account_id)
            if account:
                return render_template('saving_accounts.html', saving_accounts=[account])
            else:
                return render_template('saving_accounts.html', error="Aucun compte trouvé avec cet ID.")
        except ValueError:
            return render_template('saving_accounts.html', error="ID invalide.")
    return render_template('saving_accounts.html', error="Veuillez fournir un ID de compte.")

@bankaccount.route('/edit_saving_account', methods=['POST'])
def edit_saving_account():
    account_id = request.form['account_id']
    new_balance = float(request.form['balance'])
    new_interestRate = float(request.form['interestRate'])
    
    saving_account_dao.update_account_balance(int(account_id), new_balance, new_interestRate)

    return redirect(url_for('bankaccount.get_all_saving_accounts'))

@bankaccount.route('/delete_saving_account/<int:account_id>', methods=['POST'])
def delete_saving_account(account_id):
    saving_account_dao.delete_account(account_id)
    return redirect(url_for('bankaccount.get_all_saving_accounts'))  # Redirection vers la liste des comptes 

@bankaccount.route('/log_saving_account', methods=['POST'])
def log_saving_account():
    try:
        account_id = int(request.form['account_id'])
        accounts = saving_account_dao.log_account(account_id)
        print(accounts)
        return render_template('transactions_saving_log.html', transactions=accounts)
    except ValueError:
        return "Invalid account ID provided", 400


@bankaccount.route('/transactions_saving_account', methods=['POST'])
def transactions_saving_account():
    transaction_type = request.form['transaction_type']

    if transaction_type == 'deposit':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        saving_account_dao.deposit(account_id,amount)
        return redirect(url_for('bankaccount.get_all_saving_accounts'))
    
    if transaction_type == 'withdraw':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        saving_account_dao.withdraw(account_id,amount)
        return redirect(url_for('bankaccount.get_all_saving_accounts'))
    
    if transaction_type == 'transfer':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        print("from controler + ",amount)
        recipient_account = int(request.form['recipient_account'])
        saving_account_dao.transfer(account_id,recipient_account,amount)
        return redirect(url_for('bankaccount.get_all_saving_accounts'))
    
    if transaction_type == 'add_interest':
        account_id = int(request.form['account_id'])
        saving_account_dao.add_periodic_interest(account_id)
        return redirect(url_for('bankaccount.get_all_saving_accounts'))
    
    return "Invalid transaction type", 400
    

    



@bankaccount.route('/create_checking_account', methods=['POST'])
def create_checking_account():
    balance = request.form['balance']
    userID = request.form['userID']
    if(checking_account_dao.create_account(balance=float(balance),userID=int(userID))!= -1):
        return redirect(url_for('bankaccount.get_all_checking_accounts'))
    return "Erreur lors de la création du compte", 400

@bankaccount.route('/checking_accounts', methods=['GET'])
def get_all_checking_accounts():
    """Get all saving accounts."""
    accounts = checking_account_dao.getAllCheckingAccounts()
    return render_template('checking_accounts.html',checking_accounts=accounts)


@bankaccount.route('/get_checking_account', methods=['GET'])
def get_checking_account():
    account_id = request.args.get('account_id')
    if account_id:
        try:
            account_id = int(account_id)
            account = checking_account_dao.getCheckingAccount(account_id)
            if account:
                return render_template('checking_accounts.html', checking_accounts=[account])
            else:
                return render_template('checking_accounts.html', error="Aucun compte trouvé avec cet ID.")
        except ValueError:
            return render_template('checking_accounts.html', error="ID invalide.")
    return render_template('checking_accounts.html', error="Veuillez fournir un ID de compte.")

@bankaccount.route('/edit_checking_account', methods=['POST'])
def edit_checking_account():
    account_id = request.form['account_id']
    new_balance = float(request.form['balance'])
    
    checking_account_dao.update_account_balance(int(account_id), new_balance)

    return redirect(url_for('bankaccount.get_all_checking_accounts'))

@bankaccount.route('/delete_checking_account/<int:account_id>', methods=['POST'])
def delete_checking_account(account_id):
    checking_account_dao.delete_account(account_id)
    return redirect(url_for('bankaccount.get_all_checking_accounts'))

@bankaccount.route('/log_checking_account', methods=['POST'])
def log_checking_account():
    try:
        account_id = int(request.form['account_id'])
        accounts = checking_account_dao.log_account(account_id)
        print(accounts)
        return render_template('transactions_checking_log.html', transactions=accounts)
    except ValueError:
        return "Invalid account ID provided", 400


@bankaccount.route('/transactions_checking_account', methods=['POST'])
def transactions_checking_account():
    transaction_type = request.form['transaction_type']

    if transaction_type == 'deposit':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        checking_account_dao.deposit(account_id,amount)
        checking_account_dao.deduct_fees(account_id)
        return redirect(url_for('bankaccount.get_all_checking_accounts'))
    
    if transaction_type == 'withdraw':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        checking_account_dao.withdraw(account_id,amount)
        checking_account_dao.deduct_fees(account_id)
        return redirect(url_for('bankaccount.get_all_checking_accounts'))
    
    if transaction_type == 'transfer':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        recipient_account = int(request.form['recipient_account'])
        checking_account_dao.transfer(account_id,recipient_account,amount)
        checking_account_dao.deduct_fees(account_id)
        checking_account_dao.deduct_fees(recipient_account)
        return redirect(url_for('bankaccount.get_all_checking_accounts'))
    
    return "Invalid transaction type", 400


@bankaccount.route('/facture_saving/<int:account_id>', methods=['GET'])
def download_invoice_saving(account_id):
    transactions = saving_account_dao.log_account(account_id)
    account = saving_account_dao.getSavingAccount(account_id)
    
    if not transactions:
        return "Aucune transaction trouvée pour cet ID", 404

    # Création du PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Définition de la police
    pdf.set_font('Arial', 'B', 16)

    # Titre de la facture
    pdf.cell(200, 10, f'Facture - Saving Account {account_id}', ln=True, align='C')
    
    # Ajout d'un saut de ligne
    pdf.ln(10)
    
    # Infos du client et date actuelle
    pdf.set_font('Arial', '', 12)
    pdf.cell(100, 10, 'Client: John Doe', ln=True)
    pdf.cell(100, 10, f'Date: {datetime.now().strftime("%d-%m-%Y")}', ln=True)
    
    pdf.ln(5)  # Saut de ligne
    
    # Tableau des transactions
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, 'Date', 1)
    pdf.cell(50, 10, 'Type', 1)
    pdf.cell(50, 10, 'Montant (USD)', 1)
    pdf.ln()
    
    # Transactions
    pdf.set_font('Arial', '', 12)
    for transaction in transactions:
        pdf.cell(50, 10, str(transaction.transaction_date), 1)
        pdf.cell(50, 10, transaction.transaction_type, 1)
        pdf.cell(50, 10, str(transaction.amount), 1)
        pdf.ln()

    # Affichage du total
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 10, 'Balance', 1)
    pdf.cell(50, 10, str(account.balance), 1) # type: ignore
    pdf.ln(10)
    
    # Nom du fichier PDF
    file_path = f"c:\\Users\\pc\\Desktop\\Bank_Managment\\myapp\\invoice_saving_account_{account_id}.pdf"
    
    # Sauvegarde temporaire du fichier PDF
    pdf.output(file_path)

    # Supprimer le fichier après téléchargement
    @after_this_request
    def cleanup(response):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier: {e}")
        return response

    # Envoyer le fichier au client
    return send_file(file_path, as_attachment=True)

@bankaccount.route('/facture_checking/<int:account_id>', methods=['GET'])
def download_invoice_checking(account_id):
    transactions = checking_account_dao.log_account(account_id)
    account = checking_account_dao.getCheckingAccount(account_id)
    
    if not transactions:
        return "Aucune transaction trouvée pour cet ID", 404

    # Création du PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Définition de la police
    pdf.set_font('Arial', 'B', 16)

    # Titre de la facture
    pdf.cell(200, 10, f'Facture - Checking Account {account_id}', ln=True, align='C')
    
    # Ajout d'un saut de ligne
    pdf.ln(10)
    
    # Infos du client et date actuelle
    pdf.set_font('Arial', '', 12)
    pdf.cell(100, 10, 'Client: John Doe', ln=True)
    pdf.cell(100, 10, f'Date: {datetime.now().strftime("%d-%m-%Y")}', ln=True)
    
    pdf.ln(5)  # Saut de ligne
    
    # Tableau des transactions
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, 'Date', 1)
    pdf.cell(50, 10, 'Type', 1)
    pdf.cell(50, 10, 'Montant (USD)', 1)
    pdf.ln()
    
    # Transactions
    pdf.set_font('Arial', '', 12)
    for transaction in transactions:
        pdf.cell(50, 10, str(transaction.transaction_date), 1)
        pdf.cell(50, 10, transaction.transaction_type, 1)
        pdf.cell(50, 10, str(transaction.amount), 1)
        pdf.ln()

    # Affichage du total
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 10, 'Balance', 1)
    pdf.cell(50, 10, str(account.balance), 1) # type: ignore
    pdf.ln(10)
    
    # Nom du fichier PDF
    file_path = f"c:\\Users\\pc\\Desktop\\Bank_Managment\\myapp\\invoice_saving_account_{account_id}.pdf"
    
    # Sauvegarde temporaire du fichier PDF
    pdf.output(file_path)

    # Supprimer le fichier après téléchargement
    @after_this_request
    def cleanup(response):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier: {e}")
        return response

    # Envoyer le fichier au client
    return send_file(file_path, as_attachment=True)

@bankaccount.route("/transactions/saving", methods=["GET", "POST"])
def saving_transactions():
    return render_template("transactions_saving.html")

@bankaccount.route("/transactions/checking", methods=["GET", "POST"])
def checking_transactions():
    return render_template("transactions_checking.html")

@bankaccount.route("/transactions-saving/historique", methods=["GET", "POST"])
def transactions_saving_historique():
    return render_template("transactions_saving_log.html")

@bankaccount.route("/transactions-checking/historique", methods=["GET", "POST"])
def transactions_checking_historique():
    return render_template("transactions_checking_log.html")

