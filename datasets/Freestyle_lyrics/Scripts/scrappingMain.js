// Funcion para descargar texto como archivos
function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
}

// Funcion para scrappear solo una letra
getLyric = doc => Array.from(doc.getElementById("mw-content-text").children).filter(
    node => node.tagName === "P" || node.tagName === "OL"
).map(
   x => (x.tagName === "P") ? "\n\n" : x.innerText
).reduce((rest,x) => rest + x)

// Funcion para descargar cada letra cada letra
getText = link => {

}

// Ponerle el id a la tabla manualmente
Array.from(document.getElementById("tabla").children).reduce(
    (res,x) => res.concat(Array.from(x.children).map(
        td => td.firstChild
    )),[]
).filter(
    node => !(node.tagName === "A" && node.innerText.includes(" vs "))
).forEach(
    node => node.remove()
)