
//:::::::::::::::::::::::::::::::::::::::: fetch-remote.js

/*———————————————————————————————————————— notes

    Empties the cache when the user clicks on the link
    in the admin header

    Uses Fetch to create an asynchronous request

    If the request is successful, the /csync script
    returns 1

    FETCH CANNOT WORK IF THE SERVER IS NOT
    CONFIGURED TO SEND THE FOLLOWING HEADER

    Header set Access-Control-Allow-Origin "*"   */

//———————————————————————————————————— getNews(code_lang)

function getNews(code_lang){
  if (code_lang != 'fr') code_lang = 'en'
  getRemoteFile(`https://cloud.svija.com/${code_lang}/index.html`, updateNews)
}

function updateNews(txt){
  document.getElementById('newsMessage').innerHTML = txt
}

//———————————————————————————————————— clearCache()

function clearCache(){
  getRemoteFile(`/csync`, reportCleared)
}

function reportCleared(returnValue){
  if (returnValue == 1) alert(MSG_CACHE_CLEARED)
  else alert(MSG_CACHE_UNABLE)
}

//:::::::::::::::::::::::::::::::::::: tools fetch function

//———————————————————————————————————— getRemoteFile(path, returnFunction)

function getRemoteFile(path, returnFunction){

  if (path.substr(0,1) != '/')
    headerArray = {'Content-Type': 'text/plain'}

  else{
    var csrfcookie = ''
    if(document.getElementsByTagName('input').length > 0)
      if (csrfcookie == '')
        csrfcookie = document.getElementsByTagName('input')[0].value

    headerArray = {'X-CSRFToken': csrfcookie}
  }

  const request = new Request( path, {
    method : 'POST',
    headers: headerArray,
    mode   : 'cors',
  })

  path = path + '?' + Math.random()

  fetch(request)
    .then(
      function(result){
        if (result.ok) return result.text()
        else { console.log(`!result.ok: ${path}`) }
      }
    ).then(
      function(text){
        if (text != '') returnFunction(text)
        else{ console.log(`empty file: ${path}`) }
      }
   ).catch(
     function(err){
       console.log(`fetch error: ${err}`)
       return ''
     }
   )
}

//:::::::::::::::::::::::::::::::::::::::: fin

