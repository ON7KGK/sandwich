# Image Python légère
FROM python:3.11-slim

# Répertoire de travail dans le container
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Exposer le port 8080
EXPOSE 8080

# Variable d'environnement pour Flask
ENV FLASK_APP=main.py

# Commande de démarrage
CMD ["python", "main.py"]
