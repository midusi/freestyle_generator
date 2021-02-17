const axios = require('axios')
const fs = require('fs')
const jsdom = require('jsdom')
const { JSDOM } = jsdom
const axiosRetry = require('axios-retry')
axiosRetry(axios, { retryDelay: axiosRetry.exponentialDelay})

const baseUrl = 'https://www.musica.com/'
const artist = '/' + process.argv[2]
const id = 'letras.asp?letras=' + process.argv[3]

logError = error => console.log(error)

getDocument = html => new JSDOM(html).window.document

// Obtiene todos los links de una pagina de artista
getLinksInPage = document => Array.from(document.querySelectorAll('.listado-letras a'))
  .filter((a, i) => i % 2 == 0)
  .map(a => a.href)

// Obtiene la letra de una cancion
getLyrics = document => Array.from(document.querySelectorAll('#letra p'))
  .map(p => p.innerHTML.replace(/<br>/g,'\n').replace(/\[(.*?)\]/g,''))
  .join('\n\n')

getTitle = document => document.querySelector('.info h1').textContent

getSongLinks = url, path => axios.get(url).then(
    response => {
        links = getLinksInPage(getDocument(response.data))
        links.forEach(link => {
          axios.get(baseUrl + link).then(
            response => {
              doc = getDocument(response.data)
              lyrics = getLyrics(doc)
              title = getTitle(doc)
              fs.writeFile(path + title, lyrics, (err => {
                if(err) console.log(err)
                else console.log(title + ' guardado')
              }))
            }
          ).catch(logError)
        })
    }
).catch(logError)

if !fs.existsSync("./lyrics") fs.mkdir("lyrics", logError)
if !fs.existsSync("./lyrics" + artist) fs.mkdir("lyrics" + artist, logError)
getSongLinks(baseUrl + id, "./lyrics" + artist + "/")   