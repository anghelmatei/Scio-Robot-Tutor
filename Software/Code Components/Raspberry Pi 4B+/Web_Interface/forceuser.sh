#!/bin/bash

# PostgreSQL connection information
DB_HOST="ep-sweet-moon-a4zutfgf.us-east-1.aws.neon.tech"
DB_PORT="5432"
DB_NAME="BucharestHackathon2024"
DB_USER="admin"
DB_PASSWORD="D0OG5cvldrMg"
DB_SSL_MODE="require"
ENDPOINT_ID="ep-sweet-moon-a4zutfgf" # Add the Endpoint ID here

# Extrage datele din formularul HTML și le salvează în variabile
username=$(echo "$QUERY_STRING" | grep -oP 'username=\K[^&]*' | sed 's/%20/ /g')
api_key=$(echo "$QUERY_STRING" | grep -oP 'apiKey=\K[^&]*' | sed 's/%20/ /g')

# Verifică dacă username-ul și API Key-ul sunt goale
if [[ -z "$username" || -z "$api_key" ]]; then
    echo "Username or API Key cannot be empty."
    exit 1
fi

# SQL query pentru a insera username-ul și API Key-ul în tabelul 'users'
QUERY="INSERT INTO users (username, api_key) VALUES ('$username', '$api_key');"

# Conectare la baza de date și executare interogare SQL
psql "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=${DB_SSL_MODE}" -c "$QUERY"
