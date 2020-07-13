#!/bin/bash
source /opt/venv/djangoEnv/bin/activate
python setup.py sdist
git add dist/django-svija-2.1.5.tar.gz
git commit -m "added version 2.1.5" -a
git push origin master
