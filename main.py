from flask import Flask, render_template, Blueprint, request
import logging
import os
import secrets
from myapp import app
from myapp.Controler.userControler import user
from myapp.Controler.BankAccountControler import bankaccount

# 🔹 Configuration du logger intégré de Flask
if not os.path.exists("logs"):
    os.makedirs("logs")

app.logger.setLevel(logging.DEBUG)  # Capture tous les niveaux de logs

# Création d'un fichier de logs
file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Ajout du handler au logger Flask
app.logger.addHandler(file_handler)

# 🔹 Enregistrement des Blueprints
app.register_blueprint(user, url_prefix='/utilisateur')
app.register_blueprint(bankaccount, url_prefix='/bankaccount')

# 🔹 Gestion des erreurs avec le logger
@app.errorhandler(500)
def internal_error(error):
    app.logger.exception("Erreur interne détectée")
    return "Erreur interne du serveur", 500

@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f"Page non trouver : {request.url}")
    return "Page non trouvée", 404

if __name__ == '__main__':
    app.secret_key = secrets.token_hex(32)
    app.run(debug=True)
