#———————————————————————————————————————— models.py

#———————————————————————————————————————— import

from django.contrib import admin
from urllib.parse import quote

#———————————————————————————————————————— Control · no dependencies

from .models import Control
class ControlAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('limit', 'used', 'cached',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('site settings',   {'fields': [('limit', 'cached'), ('used', 'password',),],}),
  ]   

admin.site.register(Control, ControlAdmin)

#———————————————————————————————————————— Redirect · no dependencies

descRedirect = "<b>Forward</b> an old page to a new one, or to create <b>shortcuts</b> for pages you visit frequently."

from .models import Redirect
class RedirectAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('from_url', 'to_url', 'active', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('redirect settings',  {'fields': ['from_url', 'to_url','active',], 'description':descRedirect,}),
  ]   

admin.site.register(Redirect, RedirectAdmin)

#———————————————————————————————————————— Font · no dependencies

descFonts    = "Fonts will be added automatically <b>the first time the page is loaded</b>. You must <i>either</i> provide a <b>WOFF filename</b> or check <b>Google font</b> (<a href=\"https://tech.svija.love/next-steps/fonts/google-fonts\">more info</a>)."

from .models import Font
class FontAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('svg_ref', 'family', 'style', 'woff', 'google', 'active', 'category',)
  list_filter = ('category', 'google', 'active', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('font information',  {'fields': [('svg_ref', 'category',), ('family', 'style',), ('woff', 'google',), 'active',], 'description':descFonts,}),

  ]   

admin.site.register(Font, FontAdmin)

#———————————————————————————————————————— Section · no dependencies

descSection  = " Website sections · see also <a href='/admin/svija/responsive/'>screen sizes</a>."

from .models import Section
class SectionAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('name', 'code', 'order', 'default_page', 'title', 'email',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('name, two-letter code', {'fields': [('name', 'code'),('default_page','order',),],'description':descSection, }),
    ('title & touch icon', {'fields': ['title', 'touch',],}),
    ('email settings',   {'fields': ['email', 'bcc', 'subject','mail_frm',], 'classes': ['collapse']}),
    ('contact form fields', {'fields': ['form_name', 'form_business', 'form_email','form_message','form_send',], 'classes': ['collapse'],}),
    ('status message & alerts', {'fields': ['form_status', 'form_sending','form_rcvd','form_alert_rcvd', 'form_alert_fail',], 'classes': ['collapse'],}),
    ('source code message', {'fields': ['comment'], 'classes': ['collapse']}),
  ]   

admin.site.register(Section, SectionAdmin)

#———————————————————————————————————————— Screen · no dependencies

descScreens    = "Supported screen sizes · maximum pixel width: <b>0 = unlimited</b> · see also <a href='/admin/svija/section/'>sections</a>."

from .models import Screen
class ScreenAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('name', 'code', 'width', 'order', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('details',{'fields': [('name', 'pixels',),('code',  'order'),],'description':descScreens,}),
    ('dimensions',{'fields': [('width', 'offsetx',), ('visible', 'offsety',), ]}),
#     ('image quality',{'fields': ['img_multiply', 'img_quality', ]}),
  ]   

admin.site.register(Screen, ScreenAdmin)

#———————————————————————————————————————— Robots · no dependencies

descRobots     = "Directives telling search engines whether or not to index your website — <a href='https://en.wikipedia.org/wiki/Robots_exclusion_standard'>more info</a>."

from .models import Robots
class RobotsAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('name', 'contents' )
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('name & file contents',{'fields': ['name', 'contents', ], 'description':descRobots, }),
  ]   
  verbose_name = "robots.txt"

  verbose_name_plural = "robots.txt"

admin.site.register(Robots, RobotsAdmin)

#———————————————————————————————————————— Script Set · no dependencies

descScript0 = "Script Sets can also be included via <a href=\"/admin/svija/page/\">page settings</a>."
descScript1 = "Link to instructions at <a href=\"https://tech.svija.love\">tech.svija.love</a> and usage notes"

from .models import ScriptScripts
class ScriptScriptsInline(admin.TabularInline):
  model = ScriptScripts
  extra = 0 
  fields = ('active', 'name', 'type', 'order', 'content',)
  verbose_name = "script"
  verbose_name_plural = "scripts"

from .models import Script
class ScriptAdmin(admin.ModelAdmin):

  # display on parent script
  list_display = ('name', 'category', 'active','always',)
  list_filter = ('category', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
     ('NAME & FILENAME', {'fields': [('name', 'active',),('category', 'always',), ], 'description':descScript0, }),
     ('INSTRUCTIONS'   , {'fields': [('url', 'instructions'),], 'classes': ['collapse'],'description':descScript1, }),
  ]   

  inlines = [ScriptScriptsInline]

admin.site.register(Script, ScriptAdmin)

#———————————————————————————————————————— Module · no dependencies

#———————————————————————————————————————— Module inline

from .models import ModuleScript
class ModuleScriptInline(admin.TabularInline):
  model = ModuleScript
  extra = 0 
  fields = ('active', 'name', 'type', 'order', 'content',)
  verbose_name = "script"
  verbose_name_plural = "scripts"
  classes = ['collapse', 'ifempty',]


descModules = "Reusable content that can be included here or via <b><a href='/admin/svija/page/'>Page Settings</a></b>."
descDefaultY = "Link to instructions at <a href=\"https://tech.svija.love\">tech.svija.love</a> and usage notes"
positdesc = 'Superimposed on the Illustrator page · negative: up ↖ left · positive: down ↘ right'

from .models import Module
class ModuleAdmin(admin.ModelAdmin):

  class Media:
    js = ( 'admin/js/ifempty.js', )

  # display on parent module
  list_display = ('name', 'section', 'screen', 'filename', 'always', 'order', 'active', 'category',)
  list_filter = ('section', 'screen', 'active', 'always', 'category', )
  save_on_top = True
  save_as = True

  fieldsets = [ 
     ('Name & Filename', {'fields': [('name', 'active','always'),('category', 'screen'), ('css_id', 'section',), ('filename','order', ),], 'description':descModules, }),
     ('Instructions'   , {'fields': [('url', 'instructions'),], 'classes': ['collapse'],'description':descDefaultY, }),
     ('Placement'    , {'fields': [('offsetx', 'position', ), ( 'offsety', 'corner', ),],'description': positdesc,}),
  ]   

  inlines = [ModuleScriptInline]

admin.site.register(Module, ModuleAdmin)

#———————————————————————————————————————— Settings · depends on robots


mailLink   = "mailto:support@svija.love?subject=custom domain request&body="
mailBody   = quote("I would like to change the address of my Svija website:\n\n  from:\n  to:\n\nThank you,\n")
descSettings = "To request a different website address, please visit <a href='https://tech.svija.love/url' target='_blank'>tech.svija.love/url</a>."

from .models import Settings
class SettingsAdmin(admin.ModelAdmin):

  # display on parent page
  list_display = ('url', 'active', 'section', 'robots',)
  save_on_top = True
  save_as = True

  fieldsets = [ 
    ('main settings',   {'fields': [('url', 'active', 'p3_color',), ('analytics_id','tracking_on', ), ('section',), 'robots',],'description': descSettings,}),
    ('mail settings', {'fields': ['mail_id', 'mail_pass', 'mail_srv','mail_port','mail_tls',], 'classes': ['collapse']}),
#     ('backup preferences', {'fields': ['backup_interval', 'backup_next', ], 'classes': ['collapse']}),
  ]   

admin.site.register(Settings, SettingsAdmin)

#———————————————————————————————————————— Page

#———————————————————————————————————————— Page inlines

from .models import Page, Illustrator
from .models import PageScript
from .models import AdditionalScript

class ModuleInlinePage(admin.TabularInline):
  model = Page.module.through
  extra = 0 
  fields = ('active', 'module', 'zindex', )
  verbose_name = "module"
  verbose_name_plural = "modules"
  classes = ['collapse', 'ifempty',]

class ScriptInlinePage(admin.TabularInline):
  model = Page.script.through
  extra = 0 
  fields = ('active', 'script', 'order', )
  verbose_name = "script set"
  verbose_name_plural = "script sets"
  classes = ['collapse', 'ifempty',]

class IllustratorInlinePage(admin.TabularInline):
  model = Illustrator
  extra = 0 
  #fields = ('zindex', 'filename',)
  fields = ('active','filename','zindex',)
  verbose_name_plural = 'Illustrator files'

class AdditionalScriptInline(admin.TabularInline):
  model = AdditionalScript
  extra = 0 
  fields = ('active', 'name', 'type', 'order', 'content',)
  verbose_name = "script"
  verbose_name_plural = "additional scripts"
#   classes = ['collapse']


descPages  = "Settings that are specific to a single page · see also <a href='/admin/svija/module/'>modules</a>."
descPixels = "Values are in pixels · Check \"Override default dimensions\" to activate"

# https://stackoverflow.com/questions/16014719/adding-a-jquery-script-to-the-django-admin-interface

class PageAdmin(admin.ModelAdmin):

  class Media:
    js = ( 'admin/js/ifempty.js', )

  # display on parent page
  list_display = ('url', 'section', 'screen', 'title', 'illustrator_file', 'published', 'incl_modules', 'category',)
  list_filter = ('section', 'screen', 'published', 'category', )
  save_on_top = True
  save_as = True

# https://stackoverflow.com/questions/38827608/get-list-display-in-django-admin-to-display-the-many-end-of-a-many-to-one-rela

  def get_queryset(self, obj):
    qs = super(PageAdmin, self).get_queryset(obj)
    return qs.prefetch_related('illustrator_fk')

  def illustrator_file(self,obj):
    return obj.illustrator_fk.filter(active=True).first()

  fieldsets = [ 
    ('setup',      {'fields': [
                     'published',
                     ('url', 'screen'),
                     ('title', 'section'),
                    ],'description':descPages, }),
    ('More Settings',  {'fields': [
                 ('category','incl_modules','incl_scripts',),
                 ('width', 'offsetx', 'default_dims',),
                 ('visible', 'offsety',),
                 'accessibility_name',
                 'accessibility_text',
                 'notes', 'pub_date',
               ], 'classes': ['collapse'],}),

#     ('page info',    {'fields': [], 'classes': ['collapse'],}),
#     ('new dimensions', {'fields': [ ], 'classes': ['collapse'], 'description':descPixels,}),
  ]   

  inlines = [IllustratorInlinePage, AdditionalScriptInline, ModuleInlinePage, ScriptInlinePage, ]

admin.site.register(Page, PageAdmin)


#———————————————————————————————————————— fin
