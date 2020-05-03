const axios = require('axios')
const fs = require('fs')
const jsdom = require('jsdom')
const { JSDOM } = jsdom
const axiosRetry = require('axios-retry')
axiosRetry(axios, { retryDelay: axiosRetry.exponentialDelay})

const baseUrl = 'https://www.hhgroups.com/'
const initialUrl = 'letras/o3d2p'

logError = error => console.log(error)

getDocument = html => (new JSDOM(html)).window.document

// Obtiene el numero de paginas
getTotalPages = doc => {
    pages = Array.from(doc.querySelector('.list_pag').children)
    return 40//parseInt(pages[pages.length-1].textContent)
}

// Obtiene todos los links de una pagina
getLinksInPage = document => [...document.querySelectorAll('.list_table .tbl_oneline .x')].map(node => node.href)

formatText = text => (text[0] === '[') ? '' : ((text[0] === ' ') ? text.substr(1) : text)

getLyrics = ({ window }) => {
    nodeIterator = window.document.createNodeIterator(window.document.querySelector('.letra_body'),window.NodeFilter.SHOW_ALL, 
        node => node.nodeType === window.Node.TEXT_NODE || node.tagName === 'BR', false)
    
    node = nodeIterator.nextNode()
    text = ''
    
    while(node) {
        text = text + ((node.nodeType !== window.Node.TEXT_NODE) ? '\n' : formatText(node.textContent))
        node = nodeIterator.nextNode()
    }
    return text
}

writeErrorFile = (index, error) => fs.writeFile(`./lyrics/errors/${index}`, error, logError)

getSongLinks = url => axios.get(url).then(
    response => {
        links = [...Array(getTotalPages(getDocument(response.data))).keys()].map(
            index => axios.get(baseUrl + initialUrl + (index)).then(
                response => getLinksInPage(getDocument(response.data))
            ).catch(logError)
        )
        // Cuando obtuve todos los links de todas las paginas pido la letra de cada una
        Promise.all(links).then(
            result => result.flat().map(
                (link, index) => axios.get(link).then(
                    response => fs.writeFile(`./lyrics/${index}`, getLyrics(new JSDOM(response.data)),logError)
                ).catch((error) => writeErrorFile(index,error))
            )
        ).catch(logError)
    }
).catch(logError)

if (!fs.existsSync("./lyrics")) fs.mkdir("lyrics",logError)
if (!fs.existsSync("./lyrics/errors")) fs.mkdir("lyrics/errors",logError)
getSongLinks(baseUrl + initialUrl + '1')   