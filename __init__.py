from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    return render_template('read_data.html', data=livres)

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM clients WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session.clear()
            session['authentifie'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

@app.route('/deconnexion')
def deconnexion():
    session.clear()
    return redirect(url_for('index'))

# --- GESTION ADMIN ---

@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if session.get('role') != 'admin':
        return "Accès interdit", 403
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        stock = request.form['stock']
        conn = get_db_connection()
        conn.execute('INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)', (titre, auteur, stock))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('formulaire_livre.html')

@app.route('/utilisateurs')
def liste_utilisateurs():
    if session.get('role') != 'admin':
        return "Accès interdit", 403
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return render_template('gestion_users.html', users=users)

# --- ACTIONS UTILISATEUR ---

@app.route('/emprunter/<int:id_livre>')
def emprunter(id_livre):
    if not session.get('authentifie'):
        return redirect(url_for('authentification'))
    conn = get_db_connection()
    livre = conn.execute('SELECT stock FROM livres WHERE id = ?', (id_livre,)).fetchone()
    if livre and livre['stock'] > 0:
        conn.execute('INSERT INTO emprunts (id_client, id_livre) VALUES (?, ?)', (session['user_id'], id_livre))
        conn.execute('UPDATE livres SET stock = stock - 1 WHERE id = ?', (id_livre,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
