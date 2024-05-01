#!/bin/bash

# PostgreSQL connection information
DB_HOST="ep-sweet-moon-a4zutfgf.us-east-1.aws.neon.tech"
DB_PORT="5432"
DB_NAME="BucharestHackathon2024"
DB_USER="admin"
DB_PASSWORD="D0OG5cvldrMg"
DB_SSL_MODE="require"
ENDPOINT_ID="ep-sweet-moon-a4zutfgf"

# Preia din argumente
username="$1"

# sterge conform usernamului
QUERY="DELETE FROM users WHERE username = '$username';"

# Incearca conexiunea la PostgreSql si executa querry
psql "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=${DB_SSL_MODE}&options=endpoint%3D${ENDPOINT_ID}" -c "${QUERY}"

# verifica codul de iesire si fa debug
if [ $? -eq 0 ]; then
    echo "Deleted entry with username '$username' from the 'users' table"
else
    echo "Failed to delete entry from the 'users' table"
fi
