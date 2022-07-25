/* global gettext */

/* must have correct name in admin.py for this file to be loaded

it's easy to see that this is being loaded too early, because the 
text THIS ONE is before the show/hide links */

'use strict';
{
    window.addEventListener('load', function() {

        // Add anchor tag for Show/Hide link
        const fieldsets = document.querySelectorAll('fieldset.ifempty');
        for (const [i, elem] of fieldsets.entries()) {

/* problem is that this is loaded BEFORE the collapse.js */

            //  DON'T HIDE IF THERE IS A VALUE
            if (elem.querySelectorAll('div.related-widget-wrapper').length > 0) {
                elem.classList.remove('collapsed');
                const h2 = elem.querySelector('h2');
                h2.appendChild(document.createTextNode(' THIS ONE '));
            }
        }

/*        // Add toggle to hide/show anchor tag
        const toggleFunc = function(ev) {
            if (ev.target.matches('.collapse-toggle')) {
                ev.preventDefault();
                ev.stopPropagation();
                const fieldset = ev.target.closest('fieldset');
                if (fieldset.classList.contains('collapsed')) {
                    // Show
                    ev.target.textContent = gettext('Hide');
                    fieldset.classList.remove('collapsed');
                } else {
                    // Hide
                    ev.target.textContent = gettext('Show');
                    fieldset.classList.add('collapsed');
                }
            }
        };
        document.querySelectorAll('fieldset.module').forEach(function(el) {
            el.addEventListener('click', toggleFunc);
        }); */

    });
}
