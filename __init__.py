from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def get_db_connection():
    # Utilise le chemin absolu pour être sûr de taper dans la bonne base
    conn = sqlite3.connect('/home/ennadifi/www/flask-app/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- AUTHENTIFICATION ---
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM clients WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['authentifie'] = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

@app.route('/')
def index():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    return render_template('read_data.html', data=livres, titre_page="Bibliothèque")

# --- GESTION DES LIVRES (ADMIN) ---
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
    return render_template('formulaire.html') # Réutilise ton formulaire en changeant les labels

@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    if session.get('role') != 'admin':
        return "Accès interdit", 403
    conn = get_db_connection()
    conn.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- RECHERCHE ET EMPRUNT (USER) ---
@app.route('/recherche', methods=['POST'])
def recherche():
    query = request.form.get('query')
    conn = get_db_connection()
    livres = conn.execute("SELECT * FROM livres WHERE titre LIKE ?", ('%' + query + '%',)).fetchall()
    conn.close()
    return render_template('read_data.html', data=livres)

@app.route('/emprunter/<int:id_livre>')
def emprunter(id_livre):
    if not session.get('authentifie'):
        return redirect(url_for('authentification'))
    
    conn = get_db_connection()
    livre = conn.execute('SELECT stock FROM livres WHERE id = ?', (id_livre,)).fetchone()
    
    if livre and livre['stock'] > 0:
        # 1. Créer l'emprunt
        conn.execute('INSERT INTO emprunts (id_client, id_livre) VALUES (?, ?)', (session['user_id'], id_livre))
        # 2. Diminuer le stock
        conn.execute('UPDATE livres SET stock = stock - 1 WHERE id = ?', (id_livre,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
