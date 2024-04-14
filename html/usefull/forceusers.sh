#!/bin/bash

# PostgreSQL connection information
DB_HOST="ep-sweet-moon-a4zutfgf.us-east-1.aws.neon.tech"
DB_PORT="5432"
DB_NAME="BucharestHackathon2024"
DB_USER="admin"
DB_PASSWORD="D0OG5cvldrMg"
DB_SSL_MODE="require"
ENDPOINT_ID="ep-sweet-moon-a4zutfgf" # Add the Endpoint ID here

# Prompt user to enter username
read -p "Enter username: " username

# Prompt user to enter API key
read -p "Enter API key: " api_key

# SQL query to insert username and API key into 'users' table
QUERY="INSERT INTO users (username, api_key) VALUES ('$username', '$api_key');"

# Attempt to connect to the PostgreSQL database and execute the query
psql "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=${DB_SSL_MODE}&options=endpoint%3D${ENDPOINT_ID}" -c "${QUERY}"

# Check the exit code to determine if the query execution was successful
if [ $? -eq 0 ]; then
    echo "Inserted username '$username' with API key '$api_key' into the 'users' table"
else
    echo "Failed to insert username and API key into the 'users' table"
fi
