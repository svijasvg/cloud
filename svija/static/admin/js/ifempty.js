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

        // if there are "ifempty" elements on the page
        const fieldsets = document.querySelectorAll('fieldset.ifempty');

        // check if there are filled-out entries
        for (const [i, elem] of fieldsets.entries()) {
            var bits = elem.querySelectorAll('tr.form-row.has_original')
            if (bits.length > 0) {
                elem.classList.remove('collapse');
            }
        }
    });
}
