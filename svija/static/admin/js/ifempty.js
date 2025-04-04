/*———————————————————————————————————————— static/admin/js/ifempty.js

  my SO question that gave me answer
  https://stackoverflow.com/questions/73108883/is-there-a-way-to-make-a-collapsed-inline-initially-visible-in-django-admin-if

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

      // fieldsets
      var bits = elem.querySelectorAll('input.vTextField')
      for (var x=0; x<bits.length; x++)
        if(bits[x].value != '')
          elem.classList.remove('collapse')

      // inlines
      var bits = elem.querySelectorAll('tr.form-row.has_original')
      if (bits.length > 0) {
        elem.classList.remove('collapse');
      }
    }
  });
}


// The Object.entries() static method returns an array of a given
// object's own enumerable string-keyed property key-value pairs.

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries

