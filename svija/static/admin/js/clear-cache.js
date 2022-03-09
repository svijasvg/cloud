/*———————————————————————————————————————— clear-cache.js

    Empties the cache when the user clicks on the link
    in the admin header

    Uses Fetch to create an asynchronous request

    If the request is successful, the /csync script
    returns 1 */

//———————————————————————————————————————— clear()

function clear(){

  // I am not sure if this is correct
  // it doesn't make sense but it seems to work so 
  // I won't mess with it 

  var csrfcookie = '';
  
  if (csrfcookie == '')
    csrfcookie = document.getElementsByTagName('input')[0].value;

//———————————————————————————————————— data = new FormData()

  let data = new FormData();
  data.append('message', 'humpty');

  const request = new Request( '/csync', {

      method : 'POST',
      headers: {'X-CSRFToken': csrfcookie},
      mode   : 'same-origin',
      body   : data

  });

  fetch(request).then(
    function(response){
      return response.text().then(
        function(text){
         showAlert(text);
        }
      )
    }
  );

  return false;
}


//———————————————————————————————————— showAlert(returnValue){

function showAlert(returnValue){
  if (returnValue == 1) alert('Cache cleared.');
  else alert('Unable to clear cache — are you connected to the internet?');
}

//————————————————————————————————————————
