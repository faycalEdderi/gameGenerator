@echo off

REM Crée un environnement virtuel
python -m venv GameGenerator
call GameGenerator\Scripts\activate

REM Crée un fichier .env avec des variables vides
(
  echo HUGGINGFACE_API_KEY=
  echo DB_PASSWORD=
  echo DB_USER=
  echo DB_HOST=
  echo DB_PORT=
  echo DB_NAME=
  echo HUGGINGFACE_API_URL=
  echo SECRET_KEY=
  echo DEBUG=
) > .env

REM Installe les dépendances
pip install -r requirements.txt
