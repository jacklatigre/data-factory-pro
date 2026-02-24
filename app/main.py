from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Configurazione Database: prova a leggere da K8s, altrimenti usa i valori che funzionano ora
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'fabbricadati')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'PasswordSegreta123')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/')
def index():
    messaggi = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Recupera tutti i messaggi dal più recente al più vecchio
        cur.execute('SELECT testo FROM messaggi ORDER BY id DESC;')
        messaggi = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Errore nel recupero dati: {e}")
    
    # Passa la lista dei messaggi al template index.html
    return render_template('index.html', messaggi=messaggi)

@app.route('/salva', methods=['POST'])
def salva_dati():
    dato = request.form.get('dato')
    if dato:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO messaggi (testo) VALUES (%s)', (dato,))
            conn.commit()
            cur.close()
            conn.close()
            # Invece di una scritta bianca, torniamo alla home per vedere il dato inserito
            return redirect(url_for('index'))
        except Exception as e:
            return f"Errore durante il salvataggio: {e}", 500
    return "Nessun dato inviato", 400

if __name__ == '__main__':
    # Creazione tabella automatica all'avvio se non esiste
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS messaggi (id SERIAL PRIMARY KEY, testo TEXT NOT NULL);')
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass
    
    app.run(host='0.0.0.0', port=5000)
