#———————————————————————————————————————— instructional notes

descSettings     = "Basic settings that affect the entire website."
descLanguages    = "Languages supported by your website."
descScreens      = "You can define the screen sizes you want to support for your website."
descCombinations = "Combination Codes are the first part of the page address. They represent a specific <b>language/screen size combination</b>."
descPages        = "All the settings that are specific to a single page."
descModules      = "Modules are reusable content that can be included via <b><a href='/admin/svija/prefix/'>Combination Codes</a></b> or <b><a href='/admin/svija/page/'>Page Settings</a></b>."
descFonts        = "Fonts will be added automatically <b>the first time the page is loaded</b>. You must either provide a <b>WOFF filename</b> or check \"<b>Google font</b>\"."
descDefault      = "Default scripts are loaded automatically with every page."
descOptional     = "Optional scripts can be added via the settings for each page."
descRobots       = "Directives telling search engines whether or not to index your website — <a href='https://en.wikipedia.org/wiki/Robots_exclusion_standard'>more info</a>."
descRedirects    = "Use redirects to <b>forward</b> an old page address to a new one, or to create <b>shortcuts</b> for pages you visit frequently."
descTemplates    = "A template is the HTML container that displays Illustrator files. Use the debug template to expose the parts of the page separately."
descNotes        = "This is a place where you can leave messages for yourself or your coworkers"
descHelp         = "Articles or useful information to help you with Svija."


from django.contrib import admin

#———————————————————————————————————————— redirects · no dependencies

from .models import Forwards
class ForwardsAdmin(admin.ModelAdmin):

    # display on parent page
    list_filter = ('active', )
    list_display = ('to_page', 'to_prefix', 'from_url', 'active', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('no leading slash',    {'fields': ['from_url','to_prefix', 'to_page','active',], 'description':descRedirects,}),
    ]   

admin.site.register(Forwards, ForwardsAdmin)

#———————————————————————————————————————— fonts · no dependencies

from .models import Font
class FontAdmin(admin.ModelAdmin):

    # display on parent page
    list_filter = ('active', 'google', 'family', )
    list_display = ('css', 'family', 'style', 'source', 'google', 'active', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('font info',    {'fields': ['css', 'family', 'style', 'source', 'google', 'active',], 'description':descFonts,}),

    ]   

admin.site.register(Font, FontAdmin)

#———————————————————————————————————————— help · no dependencies

from .models import Help
class HelpAdmin(admin.ModelAdmin):

    # display on parent page
    list_filter = ('cat1', 'cat2',)
    list_display = ('name', 'cat1', 'cat2','link',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('meta',    {'fields': ['name', 'cat1', 'cat2', 'link',], 'description':descHelp,}),
        ('contents',    {'fields': ['contents',], }),
    ]   

    class Media:
        js = ('ckeditor.js',) 

admin.site.register(Help, HelpAdmin)

#———————————————————————————————————————— notes · no dependencies

from .models import Notes
class NotesAdmin(admin.ModelAdmin):

    # display on parent page
    list_filter = ('category', 'author',)
    list_display = ('name', 'category', 'author',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('meta',    {'fields': ['name','category', 'author',], 'description':descNotes, }),
        ('contents',    {'fields': ['contents',], }),
    ]   

    class Media:
        js = ('ckeditor.js',) 

admin.site.register(Notes, NotesAdmin)

#———————————————————————————————————————— language · no dependencies

from .models import Language
class LanguageAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('name', 'code', 'title', 'email',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('name, two-letter code & flag emoji', {'fields': ['name', 'code','display_order',],'description':descLanguages, }),
        ('title & touch icon', {'fields': ['title', 'touch',],}),
        ('email parameters',   {'fields': ['email', 'subject','mail_frm',], 'classes': ['collapse']}),
        ('contact form labels', {'fields': ['form_name', 'form_business', 'form_email','form_status','form_send',], 'classes': ['collapse'],}),
        ('status messages', {'fields': ['form_sending', 'form_alert_fail','form_rcvd','form_alert_rcvd',], 'classes': ['collapse'],}),
        ('source code message', {'fields': ['comment'], 'classes': ['collapse']}),
    ]   

admin.site.register(Language, LanguageAdmin)

#———————————————————————————————————————— robots · no dependencies

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

#———————————————————————————————————————— template · no dependencies

from .models import Template
class TemplateAdmin(admin.ModelAdmin):

    # display on parent template
    list_display = ('name', 'display_order', 'active', 'description', 'filename', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('Name & Filename (in svija/templates)', {'fields': ['name', 'display_order', 'active', 'filename','description', ],'description':descTemplates,}),
    ]   

admin.site.register(Template, TemplateAdmin)

#———————————————————————————————————————— default scripts · dependent on responsive

from .models import DefaultScripts, DefaultScriptTypes
class DefaultScriptTypesInline(admin.TabularInline):
    model = DefaultScriptTypes
    extra = 0 
    fields = ('type', 'active', 'order', 'name', 'content',)

class DefaultScriptsAdmin(admin.ModelAdmin):

    # display on parent scripts
    list_display = ('name', 'active', 'responsive', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('Scripts Name', {'fields': ['name', 'active', 'responsive', ],'description':descDefault, }),
    ]   
    inlines = [DefaultScriptTypesInline]

admin.site.register(DefaultScripts, DefaultScriptsAdmin)

#———————————————————————————————————————— optional scripts · no dependencies

from .models import OptionalScript
class OptionalScriptAdmin(admin.ModelAdmin):

    # display on parent menu
    list_filter = ('type', 'sort1', 'sort2','active',)
    list_display = ('name', 'sort1', 'sort2', 'type','active',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('name & sorting', {'fields': ['name', 'active', 'type', 'sort1','sort2',],'description':descOptional,}),
        ('content',        {'fields': ['content',                      ],}),
    ]   

admin.site.register(OptionalScript, OptionalScriptAdmin)

#———————————————————————————————————————— screen size · no dependencies

from .models import Responsive
class ResponsiveAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('name', 'code', 'display_order', 'canonical', 'source_dir', 'description')
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('details',{'fields': ['name', 'code', 'display_order', 'canonical', 'source_dir', 'meta_tag', 'description'],'description':descScreens,}),
        ('dimensions',{'fields': ['width', 'visible', 'offsetx', 'offsety', ]}),
#       ('image quality',{'fields': ['img_multiply', 'img_quality', ]}),
    ]   

admin.site.register(Responsive, ResponsiveAdmin)

#———————————————————————————————————————— modules · no dependencies

from .models import ModuleScripts
class ModuleScriptsInline(admin.TabularInline):
    model = ModuleScripts
    extra = 0 
    fields = ('type', 'active', 'order', 'name', 'content',)
    verbose_name = "script"
    verbose_name_plural = "scripts"

# https://stackoverflow.com/questions/5852540/django-admin-display-multiple-fields-on-the-same-line
#   position = models.CharField(max_length=255, default='absolute', choices=Choices(*positions), verbose_name='placement')
#   corner = models.CharField(max_length=255, default='top left', choices=Choices(*corners), verbose_name='reference corner')
#   horz_offset = models.PositiveSmallIntegerField(default=0, verbose_name='horizontal offset (px)',)
#   vert_offset = models.PositiveSmallIntegerField(default=0, verbose_name='vertical offset (px)',)

positdesc = 'Superimposed on the page · negative = move up/left · positive = move down/right'

from .models import Module
class ModuleAdmin(admin.ModelAdmin):

    # display on parent module
    list_filter = ('active', 'sort1', 'sort2', )
    list_display = ('name', 'css_id', 'active', 'display_order', 'sort1', 'sort2', 'filename',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
       ('NAME & FILENAME', {'fields': ['name', 'active', 'display_order', ('sort1', 'sort2',), ('css_id', 'filename', ),], 'description':descModules, }),
       ('Notes', {'fields': ['notes', ], 'classes': ['collapse'],}), 
       ('PLACEMENT', {'fields': [('position', 'corner',), ('horz_offset', 'vert_offset',),],'description': positdesc,}),
    ]   

    inlines = [ModuleScriptsInline]

admin.site.register(Module, ModuleAdmin)

#———————————————————————————————————————— prefix · depends on responsive & language

from .models import Prefix
class ModuleInlinePrefix(admin.TabularInline):
    model = Prefix.module.through
    extra = 0 
    fields = ('module', 'prefix', 'zindex', 'active',)
    verbose_name = "module"
    verbose_name_plural = "modules"

class PrefixAdmin(admin.ModelAdmin):

    # display on parent menu
    list_display = ('path', 'language', 'responsive', 'default', 'display_order',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('display name', {'fields': ['path', 'default', 'language', 'responsive', 'display_order', ],'description':descCombinations,}),
    ]   

    inlines = [ModuleInlinePrefix, ]

admin.site.register(Prefix, PrefixAdmin)

#———————————————————————————————————————— settings · depends on robots & prefix

from .models import Settings
class SettingsAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('url', 'active', 'robots', 'prefix',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('main settings',   {'fields': ['robots', 'active', 'url', 'secure', 'p3_color', 'prefix', 'analytics_id', 'tracking_on',],'description': descSettings,}),
        ('mail parameters', {'fields': ['mail_id', 'mail_pass', 'mail_srv','mail_port','mail_tls',], 'classes': ['collapse']}),
#       ('backup preferences', {'fields': ['backup_interval', 'backup_next', ], 'classes': ['collapse']}),
    ]   

admin.site.register(Settings, SettingsAdmin)

#———————————————————————————————————————— page

from .models import Svg
class SvgInline(admin.TabularInline):
    model = Svg
    extra = 0 
    #fields = ('zindex', 'filename',)
    fields = ('filename','zindex','active',)
    verbose_name_plural = 'Illustrator svg files'

from .models import Page
class OptionalScriptInline(admin.TabularInline):
    model = Page.optional_script.through
    extra = 0 
    verbose_name = "optional script"
    verbose_name_plural = "optional scripts"
    classes = ['collapse']

from .models import PageScripts
class PageScriptsInline(admin.TabularInline):
    model = PageScripts
    extra = 0 
    fields = ('type', 'active', 'order', 'name', 'content',)
    verbose_name = "script"
    verbose_name_plural = "additional scripts"
    classes = ['collapse']

class ModuleInlinePage(admin.TabularInline):
    model = Page.module.through
    extra = 0 
    fields = ('module', 'zindex', 'active',)
    verbose_name = "module"
    verbose_name_plural = "modules"

class PageAdmin(admin.ModelAdmin):
    list_filter = ('prefix', 'visitable', 'suppress_modules', 'override_dims', 'template', )

    # display on parent page
    list_display = ('url', 'prefix', 'display_order', 'title', 'visitable', 'suppress_modules', 'pub_date',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('BASIC SETUP',        {'fields': ['display_order', 'visitable', 'prefix','url',],'description':descPages, }),
        ('setup & details',    {'fields': ['title','pub_date','notes','template',], 'classes': ['collapse'],}),
        ('accessibility text', {'fields': ['accessibility_name','accessibility_text'], 'classes': ['collapse'],}),
        ('OVERRIDES',          {'fields': ['suppress_modules','override_dims', ],}),
        ('dimensions',         {'fields': ['width', 'visible', 'offsetx', 'offsety', ], 'classes': ['collapse'],}),
    ]   

    inlines = [SvgInline, ModuleInlinePage, OptionalScriptInline, PageScriptsInline]

admin.site.register(Page, PageAdmin)


#———————————————————————————————————————— fin
