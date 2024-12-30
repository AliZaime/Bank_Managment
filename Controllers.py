from flask import (Flask,
                   request,
                   render_template,
                   jsonify,
                   abort,
                   session,
                   redirect,
                   url_for
                   )

from Services import *
from Models import *
from werkzeug.exceptions import HTTPException
import secrets
from decimal import Decimal

#werkzeug : serveur web de FlaskS
#Express  : serveur web de dot.js
app = Flask(__name__)
app.secret_key=secrets.token_hex(32)
userService:UserManage=UserManage()
saving_account_dao:SavingAccountService = SavingAccountService()
checking_account_dao:CheckingAccountService = CheckingAccountService()

"""
CRUD in Rest

C : CREATE => POST
R : READ => GET (dafault behavior in browser)
U : UPDATE => PUT
D : DELETE => DELETE

REST-CLIENT : testeur d'API

"""

#Flask permet de serialiser automatiquement 
@app.errorhandler(HTTPException)
def error(e:HTTPException):
    return{
        "ip":request.remote_addr,
        "methode":request.method,
        "user-agent":request.headers.get('user-agent'),
        "error":str(e),
        "status":e.code
    }

@app.route("/error")
def check_error():
    #raise Exception("Error found!!")
    abort(500)
    
@app.route("/users",methods=["GET"])
def users():
    if session.get("email"):
        return userService.listUsers()
    return redirect(url_for('index'))

@app.route("/auth",methods=["POST"])
def auth():
    login = request.form.get("login")
    password = request.form.get("password")
    user:User|None =  userService.auth(login, password) # type: ignore
    if user == None:
        return render_template("authentication.html",error="Login or password incorrect")
    session["email"]=login
    listUsers = userService.listUsers()
    return render_template('Home.html',users=listUsers)


@app.route('/create_saving_account', methods=['POST'])
def create_saving_account():
    balance = request.form['balance']
    interest_rate = request.form['interestRate']
    saving_account_dao.create_account(float(balance),float(interest_rate))
    return redirect(url_for('get_all_saving_accounts'))

@app.route('/saving_accounts', methods=['GET'])
def get_all_saving_accounts():
    """Get all saving accounts."""
    accounts = saving_account_dao.getAllSavingAccounts()
    return render_template('saving_accounts.html',saving_accounts=accounts)


@app.route('/get_saving_account', methods=['GET'])
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

@app.route('/edit_saving_account', methods=['POST'])
def edit_saving_account():
    account_id = request.form['account_id']
    new_balance = float(request.form['balance'])
    new_interestRate = float(request.form['interestRate'])
    
    saving_account_dao.update_account_balance(int(account_id), new_balance, new_interestRate)

    return redirect(url_for('get_all_saving_accounts'))

@app.route('/delete_saving_account/<int:account_id>', methods=['POST'])
def delete_saving_account(account_id):
    saving_account_dao.delete_account(account_id)
    return redirect(url_for('get_all_saving_accounts'))  # Redirection vers la liste des comptes 

@app.route('/log_saving_account', methods=['POST'])
def log_saving_account():
    try:
        account_id = int(request.form['account_id'])
        accounts = saving_account_dao.log_account(account_id)
        print(accounts)
        return render_template('transactions_saving_log.html', transactions=accounts)
    except ValueError:
        return "Invalid account ID provided", 400


@app.route('/transactions_saving_account', methods=['POST'])
def transactions_saving_account():
    transaction_type = request.form['transaction_type']

    if transaction_type == 'deposit':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        saving_account_dao.deposit(account_id,amount)
        return redirect(url_for('get_all_saving_accounts'))
    
    if transaction_type == 'withdraw':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        saving_account_dao.withdraw(account_id,amount)
        return redirect(url_for('get_all_saving_accounts'))
    
    if transaction_type == 'transfer':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        recipient_account = int(request.form['recipient_account'])
        saving_account_dao.transfer(account_id,recipient_account,amount)
        return redirect(url_for('get_all_saving_accounts'))
    
    if transaction_type == 'add_interest':
        account_id = int(request.form['account_id'])
        saving_account_dao.add_periodic_interest(account_id)
        return redirect(url_for('get_all_saving_accounts'))
    
    return "Invalid transaction type", 400
    

    



@app.route('/create_checking_account', methods=['POST'])
def create_checking_account():
    balance = request.form['balance']
    checking_account_dao.create_account(balance=float(balance))
    return redirect(url_for('get_all_checking_accounts'))

@app.route('/checking_accounts', methods=['GET'])
def get_all_checking_accounts():
    """Get all saving accounts."""
    accounts = checking_account_dao.getAllCheckingAccounts()
    return render_template('checking_accounts.html',checking_accounts=accounts)


@app.route('/get_checking_account', methods=['GET'])
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

@app.route('/edit_checking_account', methods=['POST'])
def edit_checking_account():
    account_id = request.form['account_id']
    new_balance = float(request.form['balance'])
    
    checking_account_dao.update_account_balance(int(account_id), new_balance)

    return redirect(url_for('get_all_checking_accounts'))

@app.route('/delete_checking_account/<int:account_id>', methods=['POST'])
def delete_checking_account(account_id):
    checking_account_dao.delete_account(account_id)
    return redirect(url_for('get_all_checking_accounts'))

@app.route('/log_checking_account', methods=['POST'])
def log_checking_account():
    try:
        account_id = int(request.form['account_id'])
        accounts = checking_account_dao.log_account(account_id)
        print(accounts)
        return render_template('transactions_checking_log.html', transactions=accounts)
    except ValueError:
        return "Invalid account ID provided", 400


@app.route('/transactions_checking_account', methods=['POST'])
def transactions_checking_account():
    transaction_type = request.form['transaction_type']

    if transaction_type == 'deposit':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        checking_account_dao.deposit(account_id,amount)
        return redirect(url_for('get_all_checking_accounts'))
    
    if transaction_type == 'withdraw':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        checking_account_dao.withdraw(account_id,amount)
        return redirect(url_for('get_all_checking_accounts'))
    
    if transaction_type == 'transfer':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        recipient_account = int(request.form['recipient_account'])
        checking_account_dao.transfer(account_id,recipient_account,amount)
        return redirect(url_for('get_all_checking_accounts'))
    
    if transaction_type == 'deduct_fee':
        account_id = int(request.form['account_id'])
        checking_account_dao.deduct_fees(account_id)
        return redirect(url_for('get_all_checking_accounts'))
    
    return "Invalid transaction type", 400


@app.route("/")
def index():
    return render_template("authentication.html")

@app.route("/accounts")
def accounts():
    return render_template("accounts.html")

@app.route("/logout")
def logout():
    return render_template("authentication.html")

@app.route("/Home")
def Home():
    return render_template("Home.html")

@app.route("/transactions/saving", methods=["GET", "POST"])
def saving_transactions():
    return render_template("transactions_saving.html")

@app.route("/transactions/checking", methods=["GET", "POST"])
def checking_transactions():
    return render_template("transactions_checking.html")

@app.route("/transactions-saving/historique", methods=["GET", "POST"])
def transactions_saving_historique():
    return render_template("transactions_saving_log.html")

@app.route("/transactions-checking/historique", methods=["GET", "POST"])
def transactions_checking_historique():
    return render_template("transactions_checking_log.html")



# il ya 3 methode de transfert de parametres : Path-parameter ; Request-parameter ; form-parameter
# <.....> : Path Parameter
# ?q : Request Parameter


#request Parameter
#request : represente le client
#response : represente le serveur

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')  #on peut specifier le port comme ceci : app.run(port=8000)
                                        #debug=True : pour que le serveur se recompile automatiquement autrement dit lancer le serveur en mode development