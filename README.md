Projet de Gestion des Comptes Bancaires Ce projet vise à réaliser un programme de gestion complète des comptes bancaires, en intégrant les principales fonctionnalités et concepts clés liés au domaine bancaire.

Conception et Fonctionnalités Le projet est réalisé en Python, utilisant le framework Flask pour la gestion des API. Une intégration avec une base de données MySQL via XAMPP est mise en place pour la gestion des données. À terme, l'objectif est de migrer vers SQL Server, qui est plus largement utilisé et reconnu pour des applications professionnelles. La partie frontend est développée avec HTML5 et CSS3, offrant une interface utilisateur de base pour s'entraîner à l'intégration entre Flask et Python.

Structure du Projet 1-models.py

* Ce fichier contient la classe abstraite BankAccount, qui est la classe mère. Cette abstraction est nécessaire car elle définit une méthode abstraite withdraw (le retrait d'argent), qui dépend du type de compte bancaire.
* SavingAccount : Représente le compte d'épargne. Cette classe hérite de BankAccount et implémente la méthode withdraw de manière à ne pas dépasser la marge minimale requise sur un compte d'épargne, tout en incluant une méthode pour calculer les intérêts sur les dépôts.
* CheckingAccount : Représente le compte courant standard. Cette classe hérite également de BankAccount et implémente la méthode withdraw en s'assurant que le montant retiré ne dépasse pas la limite autorisée (draft over), tout en ajoutant une méthode pour calculer les frais sur chaque transaction après un certain nombre de transactions gratuites.
2-BankAccount.py

* Ce fichier contient les méthodes pour la gestion des comptes bancaires, telles que la création, la modification, la suppression, etc.
3-dal.py

* Ce fichier s'occupe de la gestion de la base de données. Il inclut la création des tables : BankAccount, Transaction, et User. Ces tables stockent les informations relatives aux comptes, aux transactions et aux utilisateurs.
4-app.py

* Ce fichier constitue le point d'entrée principal du projet. Il gère le menu pour la gestion des comptes bancaires via le terminal. Cette partie est encore en mode terminal uniquement, sans intégration directe de Flask ou du frontend.
5-controller.py

* Ce fichier contient la gestion des API avec Flask, y compris la gestion des routes, des requêtes et des réponses. Il assure également la gestion des endpoints, la vérification des requêtes sécurisées (login, sign-in) et l'utilisation d'un secret token pour prévenir les attaques de type CSRF ou XSRF.
6-Dossiers static et templates

* Le dossier static contient les fichiers CSS pour l'interface utilisateur.
* Le dossier templates contient les fichiers HTML pour la partie frontend, qui interagit avec le backend via Flask et Python.
Objectifs et Utilisation

* Ce projet vise à fournir un cadre d'apprentissage pour la gestion des comptes bancaires en utilisant des concepts clés tels que l'abstraction, les relations de données, la gestion des transactions et la sécurité avec Flask. La combinaison de Python, Flask, et SQL (MySQL avec XAMPP, et à long terme SQL Server) permet de créer une application bancaire complète, tant du point de vue backend que frontend.
