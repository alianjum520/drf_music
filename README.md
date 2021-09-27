# drf_music
simple music site in drf

# To run this app create virtual envoirment 

pip3 install virtualenv 

# Create a environment folder 

virtualenv env 

# To activate virtual environment in macos 

source env/bin/activate

# After this intall requirements.txt file

pip3 install -r requirements.txt

# To run App first migrate db

pyhton3 manage.py migrate 

#To have admin access create superuser 

python3 manage.py createsuperuser

# To run apllication on local host 

python3 manage.py runserver
