pip install -r login/requirements/dev.txt
cd login
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
