systemctl start mongodb
cd ~/scripts/lomb/src; source /home/charlie/scripts/lomb/venv/bin/activate; FLASK_APP=app.py FLASK_ENV=development flask run --host=0.0.0.0 
