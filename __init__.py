from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est connecté
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # EXERCICE 2 : Gestion des deux types de comptes
        if (username == 'admin' and password == 'password') or \
           (username == 'user' and password == '12345'):
            
            session['authentifie'] = True
            session['username'] = username
            
            # Redirection selon le rôle
            if username == 'admin':
                return redirect(url_for('ReadBDD')) # Admin voit tout
            else:
                return redirect(url_for('hello_world')) # User va à l'accueil
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# EXERCICE 1 : Recherche par nom
@app.route('/fiche_nom/<nom>')
def fiche_nom(nom):
    if not est_authentifie():
        return redirect(url_for('authentification'))
    
    # EXERCICE 2 : Restriction d'accès (seul 'user' peut chercher par nom)
    if session.get('username') != 'user':
        return "Accès refusé : Cette zone est réservée à l'utilisateur 'user'.", 403

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
    data = cursor.fetchall()
    conn.close()
    
    return render_template('read_data.html', data=data)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET', 'POST'])
def enregistrer_client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Insertion simplifiée
        cursor.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, "Adresse par défaut"))
        conn.commit()
        conn.close()
        return redirect(url_for('ReadBDD'))
    return render_template('formulaire.html')

if __name__ == "__main__":
    app.run(debug=True)
