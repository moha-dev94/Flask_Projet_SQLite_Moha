import sqlite3
import os

# On force le travail dans le bon répertoire
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Comptes par défaut
cur.execute("INSERT INTO clients (nom, prenom, username, password, role, adresse) VALUES (?, ?, ?, ?, ?, ?)",
            ('Admin', 'System', 'admin', 'password', 'admin', 'Local Admin'))
cur.execute("INSERT INTO clients (nom, prenom, username, password, role, adresse) VALUES (?, ?, ?, ?, ?, ?)",
            ('Dupont', 'Jean', 'user', '12345', 'user', '123 Rue de Paris'))

# Stock initial de livres
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Le Petit Prince', 'Saint-Exupéry', 5))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('1984', 'George Orwell', 2))
cur.execute("INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)", ('Le Cid', 'Corneille', 1))

connection.commit()
connection.close()
print(f"Base de données créée avec succès dans {path}")
