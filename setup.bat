@echo off
pip install venv
python -m venv GameGenerator
source ./
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
) > %~dp0.env
pip install -r requirements.txt
