# freestyle_generator

## Datasets usados

Los datasets utilizados se encuentran en la carpeta [datasets](https://github.com/midusi/freestyle_generator/tree/master/datasets), y son los siguientes:

### Martin Fierro
Para empezar la generación de texto con estilo en base a caracteres empezamos tomando el martín Fierro. Es un poema gauchesco con 2.741 líneas. Para agrandar un poco más el dataset agregamos también la vuelta de martín fierro y Fausto de Estanislao Fernandez. El resultado fue un texto 8.692 líneas, 41.454 palabras y 20.8161 caracteres, incluyendo la numeración de cada verso de una estrofa

### FreeStyle
Este sería el dataset más fiel al objetivo final. Es una transcripción de Batallas de Gallo obtenidas de [esta wiki](https://batallas-de-rap-lyrics.fandom.com/es/wiki/Batallas_de_Rap_Lyrics_Wiki). El archivo que reúne todas tiene unas 7.780 líneas, 42.778 palabras y 23.2103 caracteres

### HipHop
Se obtuvo de [esta pagina](https://www.hhgroups.com/) que almacena letras de canciones de hip hop. Primero pudimos descargar algunas canciones y armar un archivo de 6.845 líneas, 45.408 palabras y 24.2769 caracteres. Luego obtuvimos el archivo [concatenated.txt](https://github.com/midusi/freestyle_generator/blob/master/datasets/Hip%20Hop%20lyrics/concatenated.txt) contiene todas las canciones de este genero de dicha pagina(cerca de 10.000) y consta de 487.137 líneas y 3.362.970 palabras. 

## Modelos Usados

*GRU en base a caracteres. Primer modelo, tomado de https://github.com/sergioburdisso/recurrently-happy-rnn . 
*textgenrnn. Es un módulo de python que trabaja sobre Keras para armar distintas variaciones de RNN. Permite trabajar a nivel de palabras o caracteres
*Poetry-Generator. Modelo que usa Markov para generar texto y una LSTM que usa una puntuación de rimas basada en un diccionario de rimas en inglés para generar versos

## Experimentos

GRU con Martín Fierro: El primer intento fue con un modelo que generaba texto con estilo del martín fierro. La arquitectura era una capa de embedding, con 3 GRUs y una densa al final. Trabajaba a nivel de caracteres. No pudo tomar rimas ni métricas, pero si formaba palabras con estilo gauchesco aunque algunas no existieran

Textgenrnn: Se encuentra en la carpeta [textgenrnn_example](https://github.com/midusi/freestyle_generator/tree/master/textgenrnn_example) y se utilizó [este módulo](https://github.com/minimaxir/textgenrnn) trabajando con con el dataset de HipHop. Primero usamos el archivo más chico. Probamos con algunas variaciones pero los modelos eran de 2 a 3 capas LSTM de 128 unidades y la dimensión del embedding en 100. También probamos incrementando la cantidad de unidades por capa, y con LSTM bidireccionales. Una vez que tuvimos le dataset más grande de canciones intentamos entrenar con eso, pero los tiempos excedían la duración de la sesión en Google Collab.

Poetry-Generator:  Acá pudimos probar las letras de Freestyle, que no son muchas y sacamos buenos resultados. Los versos riman y al trabajar con palabras no genera palabras inexistentes. Con un modelo de markov genera líneas de texto. Por otro lado usando un diccionario de rimas en inglés determina qué finales de palabras riman con una línea. De esa forma entrena a una LSTM muy chica que sólo toma la cantidad de sílabas de una línea y las rimas posibles para determinar qué tipo de línea rima con una dada. Una vez entrenada, recorre el texto generado por el modelo de Markov evaluando qué línea incorporar para ir generando un verso que rime. Esta implementacion se encuentra en la carpeta [markov_LSTM_implementation](https://github.com/midusi/freestyle_generator/tree/master/markov_LSTM_implementation), basada en [este cuaderno de kaggle](https://www.kaggle.com/paultimothymooney/poetry-generator-rnn-markov).
