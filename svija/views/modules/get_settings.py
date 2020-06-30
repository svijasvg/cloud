#———————————————————————————————————————— main settings

from svija.models import Settings

def get_settings():
    try: 
        settings = Settings.objects.get(active=True)
        return True, settings
    except:
        return False, '''<html><body style="width:100%;text-align:center;">
                      <a href="/admin/svija/settings/">
                      <img src=http://files.svija.com/github/readme-logo.jpg></a>'''

