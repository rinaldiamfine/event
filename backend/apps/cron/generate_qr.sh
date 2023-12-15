## // For every day at 00:00
# 0 0 * * * (COMMAND TO RUN ex: python3 manage.py xxxx

## This script below need to paste on bash (dont forget to add script to activate the virtualenv)
python3 manage.py generate_qr 1

# Pleasse check the .env path to run the python script