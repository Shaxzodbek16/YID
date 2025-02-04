#!/bin/bash

echo ' '

black .
echo ' '
echo ' '
sleep 2
alembic upgrade head
echo ' '
echo ' '
pip freeze > requirements.txt
echo ' '
echo ' '
export PYTHONPATH=/Users/shaxzodbek/Developer/yid

python app/server/main.py
echo ' '
echo ' '
echo ' '
echo ' '