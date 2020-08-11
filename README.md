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
Para comenzar la generación de texto a partir de un experimento ya realizado comenzamos tomando el Martín Fierro. Es un poema gauchesco con 2.741 líneas. Para agrandar un poco más el dataset agregamos también la vuelta de martín fierro y Fausto de Estanislao Fernandez. El resultado fue un texto 8.692 líneas, 41.454 palabras y 208.161 caracteres, incluyendo la numeración de cada verso de una estrofa

## Modelos Usados

Aquí se describen los modelos a lo largo del proyecto. El detalle de la experimentación realizada con cada uno se encuentra en la sección [experimentos](https://github.com/midusi/freestyle_generator#experimentos).

* LSTM: Los principales experimentos se llevaron a cabo utilizando redes LSTM para la generación de texto, con distintas variantes que se encuentran en los archivos dentro de la carpeta implementations/LSTM. Se realizaron pruebas generando texo de a palabras y de a sílabas, y se buscó manipular la salida de la red para favorecer las lineas que riman.
* GRU en base a caracteres: Se probó inicialmente este modelo tomado de https://github.com/sergioburdisso/recurrently-happy-rnn .
* textgenrnn: Es un módulo de python que trabaja sobre Keras para armar distintas variaciones de RNN. Permite trabajar a nivel de palabras o caracteres
* Markov + LSTM (Poetry-Generator): Modelo que usa Markov para generar texto y una LSTM que predice la estructura de los versos

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

Textgenrnn: Se encuentra en la carpeta [textgenrnn_example](https://github.com/midusi/freestyle_generator/tree/master/textgenrnn_example) y se utilizó [este módulo](https://github.com/minimaxir/textgenrnn) trabajando con con el dataset de HipHop. Se probaron algunas variaciones de los modelos que fueron de 2 a 3 capas LSTM de 128 unidades y con una dimensión del embedding en 100. También se probó incrementando la cantidad de unidades por capa, y con LSTM bidireccionales.
Al igual que el caso anterior, el texto generado era del estilo esperado, pero no se logró generar texto que rime.

---

Poetry-Generator:  Este experimento se realizó a partir de [este cuaderno de Kaggle](https://www.kaggle.com/paultimothymooney/poetry-generator-rnn-markov) donde se entrena un modelo de cadenas de markov para generar lineas de forma independiente, y una LSTM para que prediga la cantidad de sílabas que tendrá una linea en función de la anterior.
Luego, se genera una linea inicial y cada linea siguiente se elige primero generando muchas posibles lineas y puntuandolas en función de
* Que su cantidad de sílabas coincida con las predichas por la LSTM para la linea anterior
* Que su última palabra rime con la última palabra de la linea anterior (en función de un diccionario de rimas en inglés, pero que de cualquier forma resultó medianamente efectivo en español).

Los versos generados de esta forma riman y al trabajar con palabras no genera palabras inexistentes, sin embargo, no guardan relación alguna entre ellos o sus rimas.

---

Pruebas con LSTMs: Se realizaron distintas pruebas utilizando modelos LSTM para la generación de texto, tomando como referencia inicialmente lo descrito en [este artículo](https://medium.com/coinmonks/word-level-lstm-text-generator-creating-automatic-song-lyrics-with-neural-networks-b8a1617104fb). Siendo que en principio, el resultado obtenido fue similar al generado por el de textgenrnn, se optó por alterar las predicciones de las LSTM para favorecer los versos que rimen. Para esto se realizaron dos modificaciones:
* Puntuacion de rimas
* Generación invertida
