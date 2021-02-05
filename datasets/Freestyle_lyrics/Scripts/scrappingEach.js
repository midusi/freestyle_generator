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

letra = Array.from(document.getElementById("mw-content-text").children).filter(
    node => node.tagName === "P" || node.tagName === "OL"
).map(
   x => (x.tagName === "P") ? "\n\n" : x.innerText
).reduce((rest,x) => rest + x)

title = document.getElementById("PageHeader").children[0].children[1].innerText

download(title,letra)