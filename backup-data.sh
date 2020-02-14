#!/bin/bash
# backup-data.sh
source Env/djangoEnv/bin/activate

#———————————————————————————————————————— version number

version="2.1.1"

#———————————————————————————————————————— list of sites on this server

    # antretoise/
    # manik/
    # onecutstudio/
    # ozake/
    # staffeur/
    # svijasvg/

#———————————————————————————————————————— other sites

cd antretoise
./manage.py dumpdata > "svija-$version.json"
cd ../manik
./manage.py dumpdata > "svija-$version.json"
cd ../onecutstudio
./manage.py dumpdata > "svija-$version.json"
cd ../ozake
./manage.py dumpdata > "svija-$version.json"
cd ../staffeur
./manage.py dumpdata > "svija-$version.json"
cd ../svijasvg
./manage.py dumpdata > "svija-$version.json"

#———————————————————————————————————————— finish

printf "\n   data export finished\n\n"

#———————————————————————————————————————— fin
