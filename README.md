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

### GRU con Martín Fierro
El primer experimento para familiarizarse con la generación de texto fue el correr un modelo generador de texto con estilo del libro Martín Fierro definido en [este repositorio](https://github.com/sergioburdisso/recurrently-happy-rnn). La arquitectura era una capa de embedding, con 3 GRUs y una densa al final. Trabajaba a nivel de caracteres. Fue capaz de formar texto y palabras con estilo gauchesco (aunque algunas no existieran), aunque no fue capaz de generar texto que rime.
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

### Textgenrnn
Se encuentra en la carpeta [textgenrnn_example](https://github.com/midusi/freestyle_generator/tree/master/textgenrnn_example) y se utilizó [este módulo](https://github.com/minimaxir/textgenrnn) trabajando con con el dataset de HipHop. Se probaron algunas variaciones de los modelos que fueron de 2 a 3 capas LSTM de 128 unidades y con una dimensión del embedding en 100. También se probó incrementando la cantidad de unidades por capa, y con LSTM bidireccionales.
Al igual que el caso anterior, el texto generado era del estilo esperado, pero no se logró generar texto que rime.

---

### Poetry-Generator
Este experimento se realizó a partir de [este cuaderno de Kaggle](https://www.kaggle.com/paultimothymooney/poetry-generator-rnn-markov) donde se entrena un modelo de cadenas de markov para generar lineas de forma independiente, y una LSTM para que prediga la cantidad de sílabas que tendrá una linea en función de la anterior.
Luego, se genera una linea inicial y cada linea siguiente se elige primero generando muchas posibles lineas y puntuandolas en función de
* Que su cantidad de sílabas coincida con las predichas por la LSTM para la linea anterior
* Que su última palabra rime con la última palabra de la linea anterior (en función de un diccionario de rimas en inglés, pero que de cualquier forma resultó medianamente efectivo en español).

Los versos generados de esta forma riman y al trabajar con palabras no genera palabras inexistentes, sin embargo, no guardan relación alguna entre ellos o sus rimas.
```
Madre de Dios, la que te salí de la saga
Que yo fluyo en la liga
Porque sabes que ya te apremia
Por eso que no te envidia
Tú sabes que ya te agobia
Es claro que no es tabla
No te lo voy a ser más mala
Dímelo, dice que viene siempre se calla
Hay weás que no me hace la fila
Y si me ponen un tema?
Pero parece que no me gana
Sí que te voy a dejar de pana
Yo no soy de tu hermana
No me meto en la cara
Es normal que ya no para
Viene con rap no se compara
Ese que hace en la primera
Convertí las cosas que me tira
Porque parece que este se aferra
Yo creo que con la guitarra
Que yo fluyo en la guerra
```

---

### LSTMs con alteración para lograr rimas
Se realizaron distintas pruebas utilizando modelos LSTM para la generación de texto, tomando como referencia inicialmente lo descrito en [este artículo](https://medium.com/coinmonks/word-level-lstm-text-generator-creating-automatic-song-lyrics-with-neural-networks-b8a1617104fb). Se realizaron pruebas con modelos que predicen en base a palabras y en base a sílabas, utilizando codificación one-hot de las palabras y embeddings. Estas pruebas se encuentran en la carpeta implementations/LSTM.
Siendo que en principio, el resultado obtenido fue similar al generado por el de textgenrnn, se optó por alterar las predicciones de las LSTM para favorecer los versos que rimen. Para esto se realizaron dos modificaciones:
* Puntuacion de rimas: Se implementó una función que determinaba si dos palabras (o sílabas) riman, y esto se utilizó para aumentar la probabilidad asignada a una palabra (o sílaba) cuando esta es la última de una linea, si es que rima con la última palabra de un verso anterior.
* Generación invertida: Uno de los problemas que se presentó al momento de implementar el punto anterior fue que al modificar las puntuaciones devueltas por la red para la última palabra, si bien se lograba que esta rimara, muchas veces se observaba una disociación fuerte entre esa palabra y el resto de la frase. Para atacar este problema se decidió entrenar a la red para que genere texto de forma invertida, es decir, de atrás para adelante. Entonces, luego de modificar la última palabra (o sílaba) de un verso, se comienzan a generar las sílabas siguientes a partir de ella, lo que resultó en una mejora notable respecto al problema mencionado.
#### Observaciones
Al momento, se detectaron los siguientes problemas con el modelo sobre los que se apunta a seguir trabajando:
* **El dataset no es lo suficientemente grande y tiene gran variedad de palabras distintas.** Si bien el dataset tiene un tamaño equivalente a otros tomados como ejemplo para generar letras de canciones, el vocabulario de este es muy variado, lo que resulta en que muchas palabras tengan pocas apariciones. Esto causa que si preprocesamos el texto para filtrar palabras que aparezcan con cierta frecuencia, por ejemplo 3 veces, se reduzca el dataset de forma significativa (mas del 50%). Si bien este problema se reduce notablemente cuando el modelo predice en función de sílabas, resulta clave avanzar sobre esto, en principio, agrandando el dataset.
* **En el entrenamiento se observa un overfitting muy alto.** La diferencia entre el accuracy entre el set de entrenamiento y de validación son muy grandes, llegando a tener el valor de 0.9 en el primero, y valores no mayores de 0.6 en el segundo. Esto estimamos que probablemente se deba a lo observado en el primer punto, porque se ha intentado mitigar disminuyendo la complejidad de la red o a través del uso de capas de dropout sin obtener resultados significativamente mejores.
* **La función de rima no considera la pronunciación de palabras en inglés.** Esto sucede porque la rima se realiza en función de las vocales de la palabra y no en función de su fonética. Para esto, una solución propuesta a implementar es la de reemplazar palabras en inglés de uso común en el dataset por su pronunciación en español (como freestyle por fristail, o beat por bit) o mejorar la implementación de la función que detecta la rima.
