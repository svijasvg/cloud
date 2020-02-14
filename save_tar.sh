#source ../Env/djangoEnv/bin/activate
workon djangoEnv
setup.py sdist
git add dist/django-svija-2.1.2.tar.gz
git commit -m "added version 2.1.2" -a
git push origin master
