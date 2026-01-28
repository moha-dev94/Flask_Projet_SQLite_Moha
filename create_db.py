import sqlite3
import os

# On s'assure d'être dans le bon dossier
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Comptes par défaut (Admin et Utilisateur)
cur.execute("INSERT INTO clients (nom, prenom, username, password, role, adresse) VALUES (?, ?, ?, ?, ?, ?)",
            ('Admin', 'System', 'admin', 'password', 'admin', 'Bureau Central'))
cur.execute("INSERT INTO clients (nom, prenom, username, password, role, adresse) VALUES (?, ?, ?, ?, ?, ?)",
            ('Dupont', 'Jean', 'user', '12345', 'user', '10 Rue de la Paix'))

# Catalogue initial
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Le Petit Prince', 'Saint-Exupéry', 5))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('1984', 'George Orwell', 2))

connection.commit()
connection.close()
print("Base de données initialisée avec succès.")
