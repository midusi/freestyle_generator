Array.from(document.getElementsByTagName("ytd-transcript-body-renderer")[0].children).map(elem => elem.children[1]).filter(elem => elem !== undefined).map(elem => elem.innerText).join('\n')
