
#:::::::::::::::::::::::::::::::::::::::: create_other_screens.py 
#———————————————————————————————————————— notes
#———————————————————————————————————————— import

def create_other_screens(request_slug, section_code, screen_code):
  return True

#   all_screen_codes = Screen.objects.all()
#   for this_code in all_screen_codes:
#     actual_code = this_code.code
#     these_screen_pages = Page.objects.filter(Q(section__code=section_code) & Q(screen__code=actual_code) & Q(url=request_slug))
#     if len(these_screen_pages) == 0:
#       page.pk = None
#       page.screen = this_code
#       page.published = False
#       page.save()
#       return HttpResponse("creating a page for "+request_slug+" for screen code "+actual_code)


#   doesn't copy other models, so no scripts, modules or illustrator files
#:::::::::::::::::::::::::::::::::::::::: fin

