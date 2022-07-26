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
