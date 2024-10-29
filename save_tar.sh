#!/bin/bash
source /opt/venv/djangoEnv/bin/activate
python setup.py sdist
git add dist/django-svija-2.3.2.tar.gz
git commit -m "added tar.gz for version 2.3.2" -a
git push origin master
