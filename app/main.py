from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Connessione al database (usa il nome del service K8s)
def get_db_connection():
    conn = psycopg2.connect(
        host='postgres',
        database='fabbricadati',
        user='postgres',
        password='PasswordSegreta123'
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salva', methods=['POST'])
def salva_dati():
    dato = request.form['dato']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO messaggi (testo) VALUES (%s)', (dato,))
    conn.commit()
    cur.close()
    conn.close()
    return "Dato salvato con successo nel cluster RKE2!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
