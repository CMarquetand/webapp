
# Verwenden Sie das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setzen Sie das Arbeitsverzeichnis innerhalb des Containers
WORKDIR /app

# Kopieren Sie die Abhängigkeiten in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren Sie die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den restlichen Anwendungscode in das Arbeitsverzeichnis
COPY . .

# Setzen Sie den Befehl, um die Flask-Anwendung auszuführen
CMD ["python", "app.py"]
