
#:::::::::::::::::::::::::::::::::::::::: create_other_screens.py 

#———————————————————————————————————————— notes
#
#   given a page and a screen code, this method
#   will create versions for other screen codes
#   if they don't exist.
#
#   to do this it is necessary to copy the foreign
#   key models like modules, illustrator files etc.
#
#———————————————————————————————————————— import

from svija.models import Screen, Page, PageModule
from django.db.models import Q


def create_other_screens(page, screen_code):

#———————————————————————————————————————— initialization 

  section_code = page.section.code
  request_slug = page.url
  all_screens  = Screen.objects.all()

#———————————————————————————————————————— ▼ loop through screens & check for missing pages

  for this_screen in all_screens:
    this_code = this_screen.code
    these_screen_pages = Page.objects.filter(Q(section__code=section_code) & Q(screen__code=this_code) & Q(url=request_slug))

    # if there's no page with this code
    if len(these_screen_pages) == 0:

#———————————————————————————————————————— new page with regular fields filled DISABLED

#     #https://stackoverflow.com/a/48015925/72958
#     a_dict = page.__dict__

#     try:
#       del a_dict['_state']
#     except:
#       vide = 'null'

#     del a_dict['id']

#     new_page = Page.objects.create(**a_dict) 

#     # get regular fields
#     new_page.title = page.title

#———————————————————————————————————————— field types DISABLED

#  BigAutoField
#  BooleanField
#  CharField
#  DateTimeField
#  PositiveSmallIntegerField
#  TextField

#———————————————————————————————————————— new page with regular fields filled

      debug=''
      new_page = Page.objects.create(url='aaa') 

      fields = page._meta.get_fields()
      for field in fields:
        if field.name == 'id'    : continue
        if field.name == '_state': continue

        tp = field.get_internal_type()

        if tp == 'ForeignKey':

          # start here
          # https://stackoverflow.com/questions/20235807/how-to-get-foreign-key-values-with-getattr-from-models



#         debug += dup_foreignKey(page, new_page, field)

#         if field.name == 'pagemodule':
#           page_modules = page.pagemodule_set.filter(enabled=True)

#           for this_module in page_modules:
#             new_page.pagemodules.objects.create()

#             out_modules.append(this_module_set.module)

          continue

        elif tp == 'ManyToManyField':
          continue

        # not foreignkey
        else:
          val = getattr(page, field.name)
          setattr(new_page, field.name, val)

#———————————————————————————————————————— correct screen & save new page

      new_page.notes  = debug
      new_page.screen = this_screen
      new_page.save()


  return True

#:::::::::::::::::::::::::::::::::::::::: methods

#———————————————————————————————————————— dup_foreignKey(page, new_page, field):
# given a field from the parent object
# which REFERS to the child object
# but is NOT the child object itself

def dup_foreignKey(page, new_page, field):
  ret_val = ''

  if field.one_to_many:


# maybe I am referring to the STRUCTURE of the models instead of the CONTENT
# I need to get() the value of the pagemodule field, not the details of its structure

    if field.name == 'pagemodule':
      ret_val += 'YAY\n'
#     rel_mods = field.related_model.objects.all() #worked
      ret_val += vid+'\n'

#   attribute list
#
#   ret_val += '\n'.join(str(vars(field)).split(",")[1:])
#   rel_mod = str(field.related_model.pk) # <property object at 0x7f127bbf6070>
#
#    'model': <class 'svija.models.Page'>
#    'related_name': None
#    'related_query_name': None
#    'limit_choices_to': {}
#    'parent_link': False
#    'on_delete': <function CASCADE at 0x7f5b10ca9f30>
#    'symmetrical': False
#    'multiple': True
#    'field_name': 'id'
#    'related_model': <class 'svija.models.PageModule'>
#    'name': 'pagemodule'
#    'one_to_one': False
#    'one_to_many': True
#    'hidden': False}


  elif field.many_to_one:
    xet_val = 'many_to_one: '+field.name+'\n'

  else:
    xet_val = 'none of above: '+field.name+'\n'

  return ret_val

#   one_to_many: pagemodule
#   one_to_many: pagescript
#   one_to_many: illustrator_fk
#   one_to_many: additionalscript
#   many_to_one: screen
#   many_to_one: section


#:::::::::::::::::::::::::::::::::::::::: fin

#       class Page(models.Model): 

#           published = models.BooleanField(default=True, verbose_name='published',)
#           screen    = models.ForeignKey(Screen, default=1, on_delete=models.PROTECT, verbose_name='screen size',)
#           section   = models.ForeignKey(Section, default=get_default_section, on_delete=models.PROTECT, verbose_name='section',)
#           url       = alphaLower(max_length=200, default='', verbose_name='address') 

#       		# to rename
#           category  = models.CharField(max_length=200, default='', verbose_name='tag (optional)', blank=True,)

#           # meta
#           notes     = models.TextField(max_length=2000, default='', blank=True)
#           pub_date  = models.DateTimeField(default=datetime.now, blank=True, verbose_name='publication date',)

#           # used in page construction
#           title  = models.CharField(max_length=200, default='', blank=True)

#           # accessibility
#           accessibility_name = models.CharField(max_length=200, default='', blank=True, verbose_name='link name')
#           accessibility_text = RichTextField(verbose_name='accessibility content', blank=True)

#           incl_modules = models.BooleanField(default=True, verbose_name='default modules',)
#           incl_scripts = models.BooleanField(default=True, verbose_name='default scripts',)

#           module = models.ManyToManyField(Module, through='PageModule')
#           script = models.ManyToManyField(Script, through='PageScript')

#           default_dims = models.BooleanField(default=True, verbose_name='default dimensions',)
#           width    = models.PositiveSmallIntegerField(default=0, verbose_name='artboard width')
#           visible  = models.PositiveSmallIntegerField(default=0, verbose_name='visible width')
#           offsetx  = models.PositiveSmallIntegerField(default=0, verbose_name='offset x')
#           offsety  = models.PositiveSmallIntegerField(default=0, verbose_name='offset y')

#           def __unicode__(self):
#               return self.name
#           def __str__(self):
#               return self.url
#           class Meta:
#               ordering = ['-published', 'url', 'section', 'screen', '-pub_date', ]
#               verbose_name_plural = "2.2 · Pages"
#           eache_reset   = models.BooleanField(default=False, verbose_name='delete cache (or visit example.com/c)',)

