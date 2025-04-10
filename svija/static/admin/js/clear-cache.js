
//:::::::::::::::::::::::::::::::::::::::: clear-cache.js

/*———————————————————————————————————————— notes

    Empties the cache when the user clicks on the link
    in the admin header

    Uses Fetch to create an asynchronous request

    If the request is successful, the /csync script
    returns 1 */

//———————————————————————————————————————— remove link if there's no input field
//                                         because csrf cookie won't be available

window.addEventListener("load", (event) => {
  if (document.getElementsByTagName('input').length == 0)
    document.getElementById('clearCache').innerHTML = ''
})

//———————————————————————————————————————— clear()

function clear(){

  // I am not sure if this is correct
  // it doesn't make sense but it seems to work so 
  // I won't mess with it 

  var csrfcookie = ''
  
  if (csrfcookie == '')
    csrfcookie = document.getElementsByTagName('input')[0].value

//———————————————————————————————————— data = new FormData()

  let data = new FormData()
  data.append('message', 'humpty')

  const request = new Request( '/csync', {

      method : 'POST',
      headers: {'X-CSRFToken': csrfcookie},
      mode   : 'same-origin',
      body   : data

  })

  fetch(request).then(
    function(response){
      return response.text().then(
        function(text){
         showAlert(text)
        }
      )
    }
   ).catch(
     function(text){
       showAlert(text)
       return
     }
   )

  return false
}

//:::::::::::::::::::::::::::::::::::: functions

//———————————————————————————————————— showAlert(returnValue){

function showAlert(returnValue){
  if (returnValue == 1) alert(MSG_CACHE_CLEARED)
  else alert(MSG_CACHE_UNABLE)
}

//:::::::::::::::::::::::::::::::::::::::: fin

