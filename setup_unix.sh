#!/bin/bash

# Crée un env virtuel
python3 -m venv GameGenerator
source GameGenerator/bin/activate

# Crée un fichier .env vide avec les variables
cat <<EOF > .env
HUGGINGFACE_API_KEY=
DB_PASSWORD=
DB_USER=
DB_HOST=
DB_PORT=
DB_NAME=
HUGGINGFACE_API_URL=
SECRET_KEY=
DEBUG=
EOF
 # install les dependances
pip install -r requirements.txt
