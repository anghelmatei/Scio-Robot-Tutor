
#!/bin/bash

# FILEPATH pt env
ENV_FILE="/home/mateisebastian/Documents/BucharestHackathon2024/scripts/.env"

# Verificam daca fisierul exista in locatia respectiva
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found"
    exit 1
fi

# Aici preluam valorile pentru noul nume de var si valoarea efectiva
VARIABLE_NAME="OPENAI_API_KEY"
NEW_VALUE="$1"
echo "??????";
echo "$NEW_VALUE";
echo "!!!!!";
# Modificam in env file
sed -i "s/^$VARIABLE_NAME=.*/$VARIABLE_NAME=$NEW_VALUE/" "$ENV_FILE"
echo "Variable $VARIABLE_NAME updated with value $NEW_VALUE in $ENV_FILE"
