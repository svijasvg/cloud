#!/bin/bash
source /opt/venv/djangoEnv/bin/activate
python setup.py sdist
git add dist/django-svija-2.2.21.tar.gz
git commit -m "added tar.gz for version 2.2.21" -a
git push origin master
