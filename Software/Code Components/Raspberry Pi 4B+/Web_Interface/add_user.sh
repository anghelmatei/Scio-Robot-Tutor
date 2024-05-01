#!/bin/bash
username=$1
apiKey=$2
DB_HOST="ep-sweet-moon-a4zutfgf.us-east-1.aws.neon.tech"
DB_PORT="5432"
DB_NAME="BucharestHackathon2024"
DB_USER="admin"
echo "$username"
echo "$apiKey"
DB_PASSWORD="D0OG5cvldrMg"
DB_SSL_MODE="require"
ENDPOINT_ID="ep-sweet-moon-a4zutfgf" 
query="INSERT INTO users (username, api_key) VALUES ('$username', '$apiKey');"
result=$(PGPASSWORD="$DB_PASSWORD" psql "postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME?sslmode=$DB_SSL_MODE&options=endpoint%3D$ENDPOINT_ID" -c "$query")
if [ $? -eq 0 ]; then
    echo "User added successfully."
else
    echo "Failed to add user."
fi
