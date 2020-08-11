# freestyle_generator

En este experimento se busca implementar un modelo generador de texto que replique el estilo freestyle utilizado en las batallas de rap.

## Datasets usados

Los datasets utilizados se encuentran en la carpeta [datasets](https://github.com/midusi/freestyle_generator/tree/master/datasets), y son los siguientes:

### FreeStyle
Este es el dataset más fiel al objetivo final. Contiene letras de batallas de rap de la FMS Argentina 2018/2019, FMS Argentina 2019 y FMS España 2018/2019, corrigiendolas a partir de las transcripciones autogeneradas de Youtube.
También cuenta con las transcripciones de batallas encontradas en [esta wiki](https://batallas-de-rap-lyrics.fandom.com/es/wiki/Batallas_de_Rap_Lyrics_Wiki).
Además se incluyeron las sesiones de freestyle de distintos freestylers producidas por bizarrap.

El archivo que reúne todas las letras tiene unas 9.865 líneas, 65.721 palabras y 347.310 caracteres

### HipHop
Un dataset mucho mayor al anterior que obtuvo de [esta pagina](https://www.hhgroups.com/) que almacena letras de canciones de hip hop. El archivo [concatenated.txt](https://github.com/midusi/freestyle_generator/blob/master/datasets/Hip%20Hop%20lyrics/concatenated.txt) contiene todas las canciones de este genero de dicha pagina (cerca de 10.000) y consta de 487.137 líneas y 3.362.970 palabras. Este dataset se utilizó para comparar los experimentos realizados con el dataset anterior.

### Martin Fierro
Para empezar la generación de texto con estilo en base a caracteres empezamos tomando el martín Fierro. Es un poema gauchesco con 2.741 líneas. Para agrandar un poco más el dataset agregamos también la vuelta de martín fierro y Fausto de Estanislao Fernandez. El resultado fue un texto 8.692 líneas, 41.454 palabras y 208.161 caracteres, incluyendo la numeración de cada verso de una estrofa

## Modelos Usados

Aquí se describen los modelos a lo largo del proyecto. El detalle de la experimentación realizada con cada uno se encuentra en la sección [experimentos](https://github.com/midusi/freestyle_generator#experimentos).

* LSTM: Los principales experimentos se llevaron a cabo utilizando redes LSTM para la generación de texto, con distintas variantes que se encuentran en los archivos dentro de la carpeta models/LSTM. Se realizaron pruebas generando texo de a palabras y de a sílabas, y se buscó manipular la salida de la red para favorecer las lineas que riman.
* GRU en base a caracteres: Se probó inicialmente este modelo tomado de https://github.com/sergioburdisso/recurrently-happy-rnn .
* textgenrnn: Es un módulo de python que trabaja sobre Keras para armar distintas variaciones de RNN. Permite trabajar a nivel de palabras o caracteres
* Poetry-Generator (Markov + LSTM): Modelo que usa Markov para generar texto y una LSTM que predice la estructura de los versos

## Experimentos

GRU con Martín Fierro: El primer experimento para familiarizarse con la generación de texto fue el correr un modelo generador de texto con estilo del libro Martín Fierro definido en [este repositorio](https://github.com/sergioburdisso/recurrently-happy-rnn). La arquitectura era una capa de embedding, con 3 GRUs y una densa al final. Trabajaba a nivel de caracteres. Fue capaz de formar texto y palabras con estilo gauchesco (aunque algunas no existieran), aunque no fue capaz de generar texto que rime.
```
en los guevos de gallinas,
porque el mal nunca se silto.

-"No me vido con arreglar.

y al ver cercano su entierro,
con igualda, pa ganarse,
y a cada paso rumpico
No hay un aumenio del muchacho
pues en mis libros adentros,
que viene a todas las motas
"esto es la justicia entera.
me hinquilque de esto no mas
y a la pun....a ia desgrenia
no se llevan al gobierno
no lo dejamos landas,
vamos a ver que tal lo hace,
le dije:-"Pa su aguela
```

---

Textgenrnn: Se encuentra en la carpeta [textgenrnn_example](https://github.com/midusi/freestyle_generator/tree/master/textgenrnn_example) y se utilizó [este módulo](https://github.com/minimaxir/textgenrnn) trabajando con con el dataset de HipHop. Primero usamos el archivo más chico. Probamos con algunas variaciones pero los modelos eran de 2 a 3 capas LSTM de 128 unidades y la dimensión del embedding en 100. También probamos incrementando la cantidad de unidades por capa, y con LSTM bidireccionales. Una vez que tuvimos le dataset más grande de canciones intentamos entrenar con eso, pero los tiempos excedían la duración de la sesión en Google Collab.

---

Poetry-Generator:  Acá pudimos probar las letras de Freestyle, que no son muchas y sacamos buenos resultados. Los versos riman y al trabajar con palabras no genera palabras inexistentes. Con un modelo de markov genera líneas de texto. Por otro lado usando un diccionario de rimas en inglés determina qué finales de palabras riman con una línea. De esa forma entrena a una LSTM muy chica que sólo toma la cantidad de sílabas de una línea y las rimas posibles para determinar qué tipo de línea rima con una dada. Una vez entrenada, recorre el texto generado por el modelo de Markov evaluando qué línea incorporar para ir generando un verso que rime. Esta implementacion se encuentra en la carpeta [markov_LSTM_implementation](https://github.com/midusi/freestyle_generator/tree/master/markov_LSTM_implementation), basada en [este cuaderno de kaggle](https://www.kaggle.com/paultimothymooney/poetry-generator-rnn-markov).
