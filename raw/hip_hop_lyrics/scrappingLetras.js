const axios = require('axios')
const fs = require('fs')
const jsdom = require('jsdom')
const { JSDOM } = jsdom
const axiosRetry = require('axios-retry')
axiosRetry(axios, { retryDelay: axiosRetry.exponentialDelay})

const baseUrl = 'https://www.letras.com'
const artist = '/' + process.argv[2]

logError = error => console.log(error)

getDocument = html => new JSDOM(html).window.document

// Obtiene todos los links de una pagina de artista en forma de {name: nombreCancion, link: enlace}
getLinksInPage = document => Array.from(document.querySelectorAll('.song-name')).map(a => {name: a.text, link: a.href})

// Obtiene la letra de una cancion
getLyrics = document => document.getElementsByClassName('cnt-letra p402_premium')[0].innerHTML
  .replace(/\[(.*?)\]/g,'')
  .replace(/<p>/g,'')
  .replace(/<\/p>/g,'\n\n')
  .replace(/<br>/g,'\n')
  .replace(/\n\n\n/g,'\n\n')

getSongLinks = url, path => axios.get(url).then(
    response => {
        links = getLinksInPage(getDocument(response.data))
        links.forEach(({name, link}) => {
          axios.get(baseUrl + link).then(
            response => {
              lyrics = getLyrics(getDocument(response.data))
              fs.writeFile(path + name, lyrics, (err => {
                if(err) console.log(err)
                else console.log(name + ' guardado')
              }))
            }
          ).catch(logError)
        })
    }
).catch(logError)

if !fs.existsSync("./lyrics") fs.mkdir("lyrics", logError)
if !fs.existsSync("./lyrics" + artist) fs.mkdir("lyrics" + artist, logError)
getSongLinks(baseUrl + artist, "./lyrics" + artist + "/")   