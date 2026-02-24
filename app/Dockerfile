# Usa un'immagine leggera di Python
FROM python:3.9-slim

# Installa le dipendenze di sistema per PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Crea una cartella di lavoro
WORKDIR /app

# Copia i file dei requisiti e installali
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice e i template
COPY . .

# Esponi la porta 5000 (quella di Flask)
EXPOSE 5000

# Comando per avviare l'app
CMD ["python", "main.py"]
