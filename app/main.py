from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Configurazione Database: legge dalle variabili d'ambiente di K8s
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
    # Recupera il nome del POD assegnato da Kubernetes
    pod_id = os.getenv('HOSTNAME', 'Sviluppo-Locale')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Recupera tutti i messaggi dal database
        cur.execute('SELECT testo FROM messaggi ORDER BY id DESC;')
        messaggi = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Errore nel recupero dati: {e}")
    
    # Passa i dati e il nome del pod al template index.html
    return render_template('index.html', messaggi=messaggi, pod_id=pod_id)

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
            # Torna alla home per vedere il nuovo dato nella lista
            return redirect(url_for('index'))
        except Exception as e:
            return f"Errore durante il salvataggio: {e}", 500
    return "Nessun dato inviato", 400

if __name__ == '__main__':
    # Inizializzazione automatica della tabella se non esiste
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS messaggi (id SERIAL PRIMARY KEY, testo TEXT NOT NULL);')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database non ancora pronto: {e}")
    
    # Avvio server Flask sulla porta 5000
    app.run(host='0.0.0.0', port=5000)