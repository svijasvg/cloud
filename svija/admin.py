#———————————————————————————————————————— models.py

#———————————————————————————————————————— import

from django.contrib import admin

#———————————————————————————————————————— redirects · no dependencies

descRedirects = "<b>Forward</b> an old page to a new one, or to create <b>shortcuts</b> for pages you visit frequently."

from .models import Forwards
class ForwardsAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('from_url', 'to_page', 'active', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('redirect settings',    {'fields': ['from_url', 'to_page','active',], 'description':descRedirects,}),
    ]   

admin.site.register(Forwards, ForwardsAdmin)

#———————————————————————————————————————— fonts · no dependencies

descFonts        = "Fonts will be added automatically <b>the first time the page is loaded</b>. You must <i>either</i> provide a <b>WOFF filename</b> or check <b>Google font</b> (<a href=\"https://tech.svija.love/next-steps/fonts/google-fonts\">more info</a>)."

from .models import Font
class FontAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('css', 'family', 'style', 'source', 'google', 'active', )
    list_filter = ('family', 'google', 'active', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('font info',    {'fields': ['css', 'family', 'style', 'source', 'google', 'active',], 'description':descFonts,}),

    ]   

admin.site.register(Font, FontAdmin)

#———————————————————————————————————————— language · no dependencies

descLanguages    = "Supported languages · see also <a href='/admin/svija/responsive/'>screen sizes</a>."

from .models import Language
class LanguageAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('name', 'code', 'display_order', 'default', 'title', 'email',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('name, two-letter code', {'fields': [('name', 'code'),('default','display_order',),],'description':descLanguages, }),
        ('title & touch icon', {'fields': ['title', 'touch',],}),
        ('email settings',   {'fields': ['email', 'bcc', 'subject','mail_frm',], 'classes': ['collapse']}),
        ('contact form labels', {'fields': ['form_name', 'form_business', 'form_email','form_message','form_send',], 'classes': ['collapse'],}),
        ('status messages', {'fields': ['form_status', 'form_sending', 'form_alert_fail','form_rcvd','form_alert_rcvd',], 'classes': ['collapse'],}),
        ('source code message', {'fields': ['comment'], 'classes': ['collapse']}),
    ]   

admin.site.register(Language, LanguageAdmin)

#———————————————————————————————————————— robots · no dependencies

descRobots       = "Directives telling search engines whether or not to index your website — <a href='https://en.wikipedia.org/wiki/Robots_exclusion_standard'>more info</a>."

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

#———————————————————————————————————————— scripts · dependent on responsive

descDefault = "Scripts are included via <a href=\"/admin/svija/page/\">page settings</a>."
descDefaultx = "Link to instructions at <a href=\"https://tech.svija.love\">tech.svija.love</a> and usage notes"

from .models import DefaultScripts, DefaultScriptTypes
class DefaultScriptTypesInline(admin.TabularInline):
    model = DefaultScriptTypes
    extra = 0 
    fields = ('type', 'active', 'order', 'name', 'content',)

class DefaultScriptsAdmin(admin.ModelAdmin):

    # display on parent scripts
    list_display = ('name', 'active', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('Name', {'fields': [('name', 'active',), ],'description':descDefault, }),
        ('Instructions', {'fields': [('url', 'notes'),], 'classes': ['collapse'],'description':descDefaultx, }),
    ]   
    inlines = [DefaultScriptTypesInline]

admin.site.register(DefaultScripts, DefaultScriptsAdmin)

#———————————————————————————————————————— screen size · no dependencies

descScreens      = "Supported screen sizes · maximum pixel width: <b>0 = unlimited</b> · see also <a href='/admin/svija/language/'>languages</a>."

from .models import Responsive
class ResponsiveAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('name', 'code', 'width', 'display_order', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('details',{'fields': [('name', 'limit',),('code',  'display_order'),],'description':descScreens,}),
        ('dimensions',{'fields': [('width', 'offsetx',), ('visible', 'offsety',), ]}),
#       ('image quality',{'fields': ['img_multiply', 'img_quality', ]}),
    ]   

admin.site.register(Responsive, ResponsiveAdmin)

#———————————————————————————————————————— modules · no dependencies

descModules = "Reusable content that can be included here or via <b><a href='/admin/svija/page/'>Page Settings</a></b>."
descDefaultY = "Link to instructions at <a href=\"https://tech.svija.love\">tech.svija.love</a> and usage notes"

from .models import ModuleScripts
class ModuleScriptsInline(admin.TabularInline):
    model = ModuleScripts
    extra = 0 
    fields = ('name', 'active','type', 'order', 'content',)
    verbose_name = "script"
    verbose_name_plural = "scripts"

# https://stackoverflow.com/questions/5852540/django-admin-display-multiple-fields-on-the-same-line
#   position = models.CharField(max_length=255, default='absolute', choices=Choices(*positions), verbose_name='placement')
#   corner = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='reference corner')
#   horz_offset = models.PositiveSmallIntegerField(default=0, verbose_name='horizontal offset (px)',)
#   vert_offset = models.PositiveSmallIntegerField(default=0, verbose_name='vertical offset (px)',)

positdesc = 'Superimposed on the Illustrator page · negative: up ↖ left · positive: down ↘ right'

from .models import Module
class ModuleAdmin(admin.ModelAdmin):

    # display on parent module
    list_display = ('name', 'screen', 'language', 'optional', 'display_order', 'css_id',  'sort1', 'published',)
    list_filter = ('screen', 'language', 'optional', 'sort1', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
       ('NAME & FILENAME', {'fields': [('name', 'published','optional'),('sort1', 'screen'), ('css_id', 'language',), ('filename','display_order', ),], 'description':descModules, }),
       ('INSTRUCTIONS'   , {'fields': [('url', 'instructions'),], 'classes': ['collapse'],'description':descDefaultY, }),
       ('PLACEMENT'      , {'fields': [('horz_offset', 'position', ), ( 'vert_offset', 'corner', ),],'description': positdesc,}),
    ]   

    inlines = [ModuleScriptsInline]

admin.site.register(Module, ModuleAdmin)

#———————————————————————————————————————— settings · depends on robots & prefix

from urllib.parse import quote

mailLink     = "mailto:support@svija.love?subject=custom domain request&body="
mailBody     = quote("I would like to change the address of my Svija website:\n\n    from:\n    to:\n\nThank you,\n")
descSettings = "To change the address of your website just email <a href='" + mailLink + mailBody + "'>support@svija.love</a>."

from .models import Settings
class SettingsAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('url', 'active', 'language', 'robots',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('main settings',   {'fields': [('url', 'active', 'p3_color',), ('analytics_id','tracking_on', ), ('language',), 'robots',],'description': descSettings,}),
        ('mail settings', {'fields': ['mail_id', 'mail_pass', 'mail_srv','mail_port','mail_tls',], 'classes': ['collapse']}),
#       ('backup preferences', {'fields': ['backup_interval', 'backup_next', ], 'classes': ['collapse']}),
    ]   

admin.site.register(Settings, SettingsAdmin)

#———————————————————————————————————————— page inlines

from .models import Page, Svg

class SvgInline(admin.TabularInline):
    model = Svg
    extra = 0 
    #fields = ('zindex', 'filename',)
    fields = ('filename','active','zindex',)
    verbose_name_plural = 'Illustrator files'

class DefaultScriptsInline(admin.TabularInline):
    model = Page.default_scripts.through
    extra = 0 
    verbose_name = "script"
    verbose_name_plural = "scripts"
    classes = ['collapse']

class ModuleInlinePage(admin.TabularInline):
    model = Page.module.through
    extra = 0 
    fields = ('module', 'active', 'zindex', )
    verbose_name = "module"
    verbose_name_plural = "modules"
    classes = ['collapse']

from .models import PageScripts
class PageScriptsInline(admin.TabularInline):
    model = PageScripts
    extra = 0 
    fields = ('name', 'active', 'type', 'order', 'content',)
    verbose_name = "script"
    verbose_name_plural = "additional scripts"
#   classes = ['collapse']

#———————————————————————————————————————— page

descPages  = "Settings that are specific to a single page · see also <a href='/admin/svija/module/'>modules</a>."
descPixels = "Values are in pixels · Check \"Override default dimensions\" to activate"


class PageAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('url', 'screen', 'language', 'title', 'visitable', 'suppress_modules', 'pub_date', )
    list_filter = ('screen', 'language', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('setup',        {'fields': ['visitable', ('url', 'screen'),('title', 'language'),],'description':descPages, }),
        ('page info',            {'fields': ['pub_date','notes',], 'classes': ['collapse'],}),
        ('accessibility',      {'fields': ['accessibility_name','accessibility_text'], 'classes': ['collapse'],}),
        ('overrides',          {'fields': [('suppress_modules','override_dims',), ],}),
        ('new dimensions',     {'fields': [('width', 'offsetx'), ('visible', 'offsety'), ], 'classes': ['collapse'], 'description':descPixels,}),
    ]   

    inlines = [SvgInline, DefaultScriptsInline, ModuleInlinePage, PageScriptsInline]
#   inlines = [SvgInline, ModuleInlinePage, OptionalScriptInline, PageScriptsInline]
#   inlines = [SvgInline, ModuleInlinePage, PageScriptsInline]

admin.site.register(Page, PageAdmin)


#———————————————————————————————————————— fin
