/*———————————————————————————————————————— static/admin/js/ifempty.js

    removes "collapse" class for fieldsets that contain data
    so that users won't run into problems because scripts
    or modules aren't initially visible in page admin

    based on collapse code in InlineModelAdmin.py

    loaded by PageAdmin class in admin.py

————————————————————————————————————————*/

/* global gettext */
'use strict';
{
    window.addEventListener('load', function() {

        const fieldsets = document.querySelectorAll('fieldset.ifempty');

        for (const [i, elem] of fieldsets.entries()) {
            if (elem.querySelectorAll('div.related-widget-wrapper').length > 1) {
                elem.classList.remove('collapse');
            }
        }
    });
}
