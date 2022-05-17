#!/bin/bash
source /opt/venv/djangoEnv/bin/activate
python setup.py sdist
git add dist/django-svija-2.2.17.tar.gz
git commit -m "added tar.gz for version 2.2.17" -a
git push origin master
