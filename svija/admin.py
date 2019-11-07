#---------------------------------------- svija admin

from django.contrib import admin

#---------------------------------------- redirects · no dependencies

from .models import Redirect
class RedirectAdmin(admin.ModelAdmin):

    # display on parent page
    list_filter = ('active', )
    list_display = ('from_url', 'to_prefix', 'to_page', 'active', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('no leading slash',    {'fields': ['from_url','to_prefix', 'to_page','active',], }),
    ]   

admin.site.register(Redirect, RedirectAdmin)

#---------------------------------------- fonts · no dependencies

from .models import Font
class FontAdmin(admin.ModelAdmin):

    # display on parent page
    list_filter = ('active', 'google', 'family', )
    list_display = ('name', 'family', 'style', 'source', 'google', 'active', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('font info',    {'fields': ['name','source', 'family', 'style', 'google', 'active',], }),
    ]   

admin.site.register(Font, FontAdmin)

#---------------------------------------- notes · no dependencies

from .models import Note
class NoteAdmin(admin.ModelAdmin):

    # display on parent page
    list_filter = ('sort1', 'sort2',)
    list_display = ('name', 'sort1', 'sort2',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('meta',    {'fields': ['name','sort1', 'sort2',], }),
        ('contents',    {'fields': ['contents',], }),
    ]   

    class Media:
        js = ('ckeditor.js',) 

admin.site.register(Note, NoteAdmin)

#---------------------------------------- language · no dependencies

from .models import Language
class LanguageAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('name', 'code', 'email',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('name & two-letter code', {'fields': ['name', 'code',],}),
        ('title & touch icon', {'fields': ['title', 'touch',],}),
        ('contact form', {'fields': ['email', 'form_name', 'form_email','form_status','form_send',],}),
        ('email params',   {'fields': ['bcc', 'default', 'no_email', 'subject','mail_frm',], 'classes': ['collapse']}),
        ('form messages', {'fields': ['form_sending', 'form_rcvd','form_alert_rcvd','form_alert_fail',],}),
        ('source comments',              {'fields': ['comment'], 'classes': ['collapse']}),
    ]   

admin.site.register(Language, LanguageAdmin)

#---------------------------------------- robots · no dependencies

from .models import Robots
class RobotsAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('name', 'contents' )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('name & file contents',{'fields': ['name', 'contents', ]}),
    ]   
    verbose_name = "robots.txt"

    verbose_name_plural = "robots.txt"

admin.site.register(Robots, RobotsAdmin)

#---------------------------------------- template · no dependencies

from .models import Template
class TemplateAdmin(admin.ModelAdmin):

    # display on parent template
    list_display = ('name','description', 'filename', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('Name & Filename (in svija/templates)', {'fields': ['name','filename','description', ],}),
    ]   

admin.site.register(Template, TemplateAdmin)

#---------------------------------------- shared scripts · no dependencies

from .models import Shared, SharedScripts
class SharedScriptsInline(admin.TabularInline):
    model = SharedScripts
    extra = 0 
    fields = ('type', 'active', 'order', 'name', 'content',)

class SharedAdmin(admin.ModelAdmin):

    # display on parent scripts
    list_display = ('name', )
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('Scripts Name', {'fields': ['name', ],}),
    ]   
    inlines = [SharedScriptsInline]

admin.site.register(Shared, SharedAdmin)

#---------------------------------------- library scripts · no dependencies

from .models import LibraryScript
class LibraryScriptAdmin(admin.ModelAdmin):

    # display on parent menu
    list_filter = ('type', 'sort1', 'sort2',)
    list_display = ('name', 'sort1', 'sort2', 'type',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('name & sorting', {'fields': ['name', 'type', 'sort1','sort2',],}),
        ('content',        {'fields': ['content',                      ],}),
    ]   

admin.site.register(LibraryScript, LibraryScriptAdmin)

#---------------------------------------- responsive · no dependencies

from .models import Responsive
class ResponsiveAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('name', 'canonical', 'source_dir', 'description')
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('details',{'fields': ['name', 'canonical', 'source_dir', 'meta_tag', 'description']}),
        ('dimensions',{'fields': ['width', 'visible', 'offsetx', 'offsety', ]}),
        ('image quality',{'fields': ['img_multiply', 'img_quality', ]}),
    ]   

admin.site.register(Responsive, ResponsiveAdmin)

#---------------------------------------- modules · no dependencies

from .models import ModuleScripts
class ModuleScriptsInline(admin.TabularInline):
    model = ModuleScripts
    extra = 0 
    fields = ('type', 'active', 'order', 'name', 'content',)
    verbose_name = "script"
    verbose_name_plural = "scripts"

from .models import Module
class ModuleAdmin(admin.ModelAdmin):

    # display on parent module
    list_filter = ('active', 'sort1', 'sort2', )
    list_display = ('name', 'active', 'sort1', 'sort2', 'filename',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
       ('NAME & FILENAME', {'fields': ['name', 'active', 'filename', 'sort1', 'sort2'],}),
    ]   

    inlines = [ModuleScriptsInline]

admin.site.register(Module, ModuleAdmin)

#---------------------------------------- prefix · depends on responsive & language

from .models import Prefix
class ModuleInlinePrefix(admin.TabularInline):
    model = Prefix.module.through
    extra = 0 
    fields = ('module', 'prefix', 'order', 'active',)
    verbose_name = "module"
    verbose_name_plural = "modules"

class PrefixAdmin(admin.ModelAdmin):

    # display on parent menu
    list_display = ('path', 'default', 'responsive', 'language')
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('display name', {'fields': ['path', 'responsive', 'language','default',],}),
    ]   

    inlines = [ModuleInlinePrefix, ]

admin.site.register(Prefix, PrefixAdmin)

#---------------------------------------- settings · depends on robots & prefix

from .models import Settings
class SettingsAdmin(admin.ModelAdmin):

    # display on parent page
    list_display = ('url', 'active', 'robots', 'prefix', 'cached', 'pub_date',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('main settings',   {'fields': ['robots', 'active', 'secure', 'url', 'cached', 'cache_reset', 'prefix', 'analytics_id', 'pub_date', 'maps_api_key',]}),
        ('mail parameters', {'fields': ['mail_id', 'mail_pass', 'mail_srv','mail_port','mail_tls',], 'classes': ['collapse']}),
        ('backup preferences', {'fields': ['backup_interval', 'backup_next', ], 'classes': ['collapse']}),
    ]   

admin.site.register(Settings, SettingsAdmin)

#---------------------------------------- page

from .models import Svg
class SvgInline(admin.TabularInline):
    model = Svg
    extra = 0 
    #fields = ('order', 'filename',)
    fields = ('filename','order','active',)

from .models import Page
class LibraryScriptInline(admin.TabularInline):
    model = Page.library_script.through
    extra = 0 
    verbose_name = "library script"
    verbose_name_plural = "library scripts"
    classes = ['collapse']

from .models import PageScripts
class PageScriptsInline(admin.TabularInline):
    model = PageScripts
    extra = 0 
    fields = ('type', 'active', 'order', 'name', 'content',)
    verbose_name = "user script"
    verbose_name_plural = "user scripts"
    classes = ['collapse']

class ModuleInlinePage(admin.TabularInline):
    model = Page.module.through
    extra = 0 
    fields = ('module', 'order', 'active',)
    verbose_name = "module"
    verbose_name_plural = "modules"

class PageAdmin(admin.ModelAdmin):
    list_filter = ('prefix', 'visitable','template', )

    # display on parent page
    list_display = ('url', 'prefix', 'title', 'template', 'visitable', 'suppress_modules', 'pub_date',)
    save_on_top = True
    save_as = True

    fieldsets = [ 
        ('BASIC SETUP',        {'fields': ['visitable', 'prefix','url','suppress_modules',],                            }),
        ('setup & details',    {'fields': ['title','pub_date','notes','template','shared'], 'classes': ['collapse']}),
        ('dimensions',         {'fields': ['override_dims', 'width', 'visible', 'offsetx', 'offsety',       ], 'classes': ['collapse']}),
        ('accessibility/SEO',  {'fields': ['access_name','access_text'],                    'classes': ['collapse']}),
    ]   

    inlines = [ModuleInlinePage, SvgInline, LibraryScriptInline, PageScriptsInline]

admin.site.register(Page, PageAdmin)

#---------------------------------------- fin
