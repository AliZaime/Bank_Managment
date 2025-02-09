from flask import Flask, render_template, Blueprint
import secrets



from myapp import app

from myapp.Controler.userControler import user
from myapp.Controler.BankAccountControler import bankaccount

app.register_blueprint(user, url_prefix='/utilisateur')
app.register_blueprint(bankaccount, url_prefix='/bankaccount')



if __name__ == '__main__':
    app.secret_key = secrets.token_hex(32)
    app.run(debug=True)

