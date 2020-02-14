#!/bin/bash
# backup-data.sh
source Env/djangoEnv/bin/activate

#———————————————————————————————————————— list of sites on this server

    # antretoise/
    # manik/
    # onecutstudio/
    # ozake/
    # staffeur/
    # svijasvg/

#———————————————————————————————————————— other sites

cd antretoise
./manage.py dumpdata > svija-2.1.1.json
cd ../manik
./manage.py dumpdata > svija-2.1.1.json
cd ../onecutstudio
./manage.py dumpdata > svija-2.1.1.json
cd ../ozake
./manage.py dumpdata > svija-2.1.1.json
cd ../staffeur
./manage.py dumpdata > svija-2.1.1.json
cd ../svijasvg
./manage.py dumpdata > svija-2.1.1.json

#———————————————————————————————————————— finish

printf "\n   data export finished\n\n"

#———————————————————————————————————————— fin
