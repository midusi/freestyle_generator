import json, io
from preprocessing import get_text
from rima import rima


path = 'D:\\Documentos\\GitHub\\freestyle_generator\\'
data_path = path + 'data\\'

def tokenize_wl(corpus):
    '''Tokenizes text at word level'''
    symbols = ['\n','?','¿',',','.','"',':','(',')','[',']','-','!','¡']
    for s in symbols:
        corpus = corpus.replace(s,' '+s+' ')
    return [w for w in corpus.split(' ') if (w.strip() != '' or w == '\n')]

words = set(tokenize_wl(get_text(data_path)))
rhymes = {}
for idx, word in enumerate(words):
    print('Procesando palabra ' + word + ', ' + str(idx) + '/' + str(len(words)))
    rhymes[word] = {'A': [], 'C': []}
    for word_to_rhyme in words:
        if word != word_to_rhyme:
            rhyme = rima(word, word_to_rhyme)
            if rhyme != 'X':
                rhymes[word][rhyme].append(word_to_rhyme)

with io.open(data_path + 'rhymes.json', 'w') as rhymes_file:
    json.dump(rhymes, rhymes_file)
        