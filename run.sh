#!/bin/bash

echo ' '

black .

sleep 2

alembic upgrade head

pip freeze > requirements.txt

export PYTHONPATH=/Users/shaxzodbek/Developer/bot_structure

python app/server/main.py
