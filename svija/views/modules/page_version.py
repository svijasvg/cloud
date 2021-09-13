#————————————————————————————————————————  redirect if it's a default page (path not shown)
#
#   called by views/PageView to redirect urls that
#   are invisible:
#
#   /en      » /
#   /en/home » /
#   /fr/home » /fr
#
#   if this returns '', nothing is done
#   if this returns an address, the correct http redirect
#   is issued by PageView and the page loading process
#   starts over
#
#———————————————————————————————————————— imports

from svija.models import Responsive

#———————————————————————————————————————— page_version( ...

def page_version(request_cookies, request_path, settings, prefix_default):

    # in system_js

    # setCookie('wiw', window.innerWidth,   7);
    # setCookie('wow', window.outerWidth,   7);
    # setCookie('nua', navigator.userAgent, 7);

    wiw = request_cookies.get('wiw')
    wow = request_cookies.get('wow')
    nua = request_cookies.get('nua')

    ret_val  = 'wiw: ' + wiw + '\n'
    ret_val += 'wow: ' + wiw + '\n'
    ret_val += 'nua: ' + nua + '\n'

#———————————————————————————————————————— get upper limits from screens

#   responsive = Responsive.objects.filter(width > 0).first()

#   ret_val += responsive[0]setting.width + '\n'
    # Responsive.objects.filter(name=prefix.responsive.name).first()


#lass Responsive(models.Model):
#   name = models.CharField(max_length=200, default='')
#   code = models.CharField(max_length=2, default='', blank=True, verbose_name='two-letter code',)
#   display_order = models.PositiveSmallIntegerField(default=0, verbose_name='display order')

#   source_dir = models.CharField(max_length=200, default='', blank=True, verbose_name='folder in /sync',)
#   meta_tag = models.CharField(max_length=200, default='', blank=True)
#   description = models.CharField(max_length=200, default='', blank=True)
#   canonical = models.BooleanField(default=False, verbose_name='canonical page for search engines',)

#   width   = models.PositiveSmallIntegerField(default=0, verbose_name='pixel width in Illustrator',blank=True,)
#   visible = models.PositiveSmallIntegerField(default=0, verbose_name='visible width in pixels')
#   offsetx = models.PositiveSmallIntegerField(default=0, verbose_name='offset x in pixels')
#   offsety = models.PositiveSmallIntegerField(default=0, verbose_name='offset y in pixels')

#   # not currently implemented, so hidden
#   img_multiply = models.DecimalField(default=2.4, max_digits=2, decimal_places=1, verbose_name='resolution multiple')
#   img_quality  = models.PositiveSmallIntegerField(default=0, verbose_name='JPG quality (0-100)')

#   def __str__(self):
#       return self.name
#   class Meta:
#       ordering = ['display_order']
#       verbose_name = "screen size"
#       verbose_name_plural = "1.3 · Screen Sizes"

#———————————————————————————————————————— return the value

    return ret_val







#———————————————————————————————————————— previous javascript

#   // redirects to desktop  if window is not in portrait mode
#   // mobile & desktop scripts are the same except for the first and last lines
#   
#   var cutoff = 0.9;
#   var ratio  = window.innerWidth / window.innerHeight;
#   var portrait = ratio < cutoff;
#   
#   // get url information
#   
#   var parts = page_url.split('/');
#   var pge   = parts[4].replace('#', '');
#   
#   // supplied by system: var responsives = {'desktop':'fr', 'mobile':'fm'};
#   
#   //if    (portrait) location.href = '/' + responsives['Mobile' ] + '/' + pge;
#   if (!portrait) location.href = '/' + responsives['Computer'] + '/' + pge;

#———————————————————————————————————————— fin
