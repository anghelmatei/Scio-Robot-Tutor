#!/bin/bash

# PostgreSQL connection information
DB_HOST="ep-sweet-moon-a4zutfgf.us-east-1.aws.neon.tech"
DB_PORT="5432"
DB_NAME="BucharestHackathon2024"
DB_USER="admin"
DB_PASSWORD="D0OG5cvldrMg"
DB_SSL_MODE="require"
ENDPOINT_ID="ep-sweet-moon-a4zutfgf" # Add the Endpoint ID here

# SQL query to select all users and their API keys
QUERY="SELECT username, api_key FROM users;"

# Attempt to connect to the PostgreSQL database and execute the query
result=$(psql "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=${DB_SSL_MODE}&options=endpoint%3D${ENDPOINT_ID}" -t -c "${QUERY}")

# Check the exit code to determine if the connection was successful
if [ $? -eq 0 ]; then
    echo "Connection to the database successful"
    # Display the result
    echo "$result"
else
    echo "Failed to connect to the database"
fi
