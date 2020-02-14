#!/bin/bash
# version-update.sh
source Env/djangoEnv/bin/activate

#———————————————————————————————————————— list of sites on this server

    # antretoise
    # manik
    # onecutstudio
    # ozake
    # staffeur
    # svijasvg

#———————————————————————————————————————— update svija

pip install git+https://github.com/svijasvg/django-svija.git@master#egg=django-svija --upgrade

#———————————————————————————————————————— all sites

cd antretoise
./manage.py makemigrations svija
./manage.py migrate
./manage.py collectstatic --noinput
cd ../manik
./manage.py migrate
./manage.py collectstatic --noinput
cd ../onecutstudio
./manage.py migrate
./manage.py collectstatic --noinput
cd ../ozake
./manage.py migrate
./manage.py collectstatic --noinput
cd ../staffeur
./manage.py migrate
./manage.py collectstatic --noinput
cd ../svijasvg
./manage.py migrate
./manage.py collectstatic --noinput

#———————————————————————————————————————— finish 

printf "\n   restarting uwsgi..."
sudo service uwsgi restart
printf "\n   finished\n\n"

#———————————————————————————————————————— fin
