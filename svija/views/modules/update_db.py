
#:::::::::::::::::::::::::::::::::::::::: update_db.py
#
#   will check and add data as necessary for various
#   improvements

#———————————————————————————————————————— import

from svija.models import Module, Screen, Script, Section, Settings
from django.db.models import Q
from django.utils.translation import gettext as _

#:::::::::::::::::::::::::::::::::::::::: get_accessibility(content):

def update_db():

#———————————————————————————————————————— 2.3.3 reorder sections

  sections = Section.objects.filter(Q(order=0)).exclude(code='*')

  if len(sections) != 0:
    sections = Section.objects.all()
    for section in sections:
      section.order += 1
      section.save()

#———————————————————————————————————————— 2.3.3 add * section

  sections = Section.objects.filter(Q(code='*'))

  if len(sections) == 0:
    source_section = Settings.objects.first().section

    destination_section = Section.objects.get(pk=source_section.pk)  # new copy of source

    destination_section.pk       = None  # creates a new object
    destination_section.code     = '*'
    destination_section.name     = _('All Sections')
    destination_section.order    = 0
    destination_section.language = False
    destination_section.save()
  
#———————————————————————————————————————— 2.3.3 reorder screens

  screens = Screen.objects.filter(Q(order=0)).exclude(code='*')

  if len(screens) != 0:
    screens = Screen.objects.all()
    for screen in screens:
      screen.order += 1
      screen.save()

#———————————————————————————————————————— 2.3.3 add * screen

  screens = Screen.objects.filter(Q(code='*'))

  if len(screens) == 0:
    screens = Screen.objects.filter(Q(pixels=0)) # copy from computer screen

    if len(screens) == 0:
      source_scr = Screen.objects.first()
    else:
      source_scr = screens[0]
   
    destination_scr = Screen.objects.get(pk=source_scr.pk)  # new copy of source

    destination_scr.pk      = None  # creates a new object
    destination_scr.code    = '*'
    destination_scr.name    = _('All Screens')
    destination_scr.order   = 0
    destination_scr.pixels  = 0
    destination_scr.width   = 0
    destination_scr.visible = 0
    destination_scr.offsetx = 0
    destination_scr.offsety = 0

    destination_scr.save()

#———————————————————————————————————————— 2.3.3 remove vibe script libraries 
#
#   delete any scripts containing "cloud"
#   that also have scripts

  # get relevant scripts
  scripts = Script.objects.filter(
    Q(name__icontains='vibe'),
    scriptscripts__isnull=False
  ).distinct()

  scripts_deleted = str(len(scripts))

  # collect primary keys first
  script_ids = scripts.values_list('id', flat=True)

  # delete in bulk
  Script.objects.filter(id__in=script_ids).delete()

#———————————————————————————————————————— 2.3.3 remove cloud modules
#
#   delete any modules containing "cloud"
#   that also have scripts

  # get relevant modules
  modules = Module.objects.filter(
    Q(name__icontains='cloud'),
    modulescript__isnull=False
  ).distinct()

  modules_deleted = str(len(modules))

  # collect primary keys first
  module_ids = modules.values_list('id', flat=True)

  # delete in bulk
  Module.objects.filter(id__in=module_ids).delete()


  return False

#:::::::::::::::::::::::::::::::::::::::: fin

