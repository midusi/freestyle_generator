import glob, unicodedata, pickle, io

from utils import save_dict
from Syllabizer import silabizer

def get_text(dataset_path, token_level):
    '''Returns corpus from all txt files stored in dataset_path'''
    files = glob.glob(dataset_path + '/**/*.txt', recursive=True)
    corpora = ''

    for f in files:
        with io.open(f, 'r', encoding='utf-8') as fc:
            corpus = fc.read().lower().replace('\xa0', ' ').replace('-','').replace('\ufeff','')
            corpora += corpus
    
    if token_level == 'S' or token_level == 'W':
        for s in ['\n','?','¿',',','.','"',':',"'",'(',')']:
            corpus = corpus.replace(s,' '+s+' ')

    corpus = unicodedata.normalize('NFC', corpus)
    return corpora

def shape_text(sequence_length, text, TOKEN_LEVEL, word_indices, step=1):
    '''Cuts the text in semi-redundant sequences of SEQUENCE_LEN words'''
    sentences = []
    next_words = []
    for i in range(0, len(text) - sequence_length, step):
        sentences.append(list(reversed(text[i + 1: i + sequence_length + 1])))
        next_words.append(text[i])
    
    print('Total sequences:', len(sentences))
    return sentences, next_words

def tokenize(TOKEN_LEVEL, corpus, bpemb):
    if TOKEN_LEVEL == 'B':
        # tokenized_text = bpemb.encode(corpus)
        corpus = bpemb.preprocess(corpus)
        corpus = corpus.split('\n')
        tokenized_text = bpemb.encode_ids_with_eos(corpus)
        tokenized_text = [item for sublist in tokenized_text for item in sublist]

    elif (TOKEN_LEVEL == 'W') or (TOKEN_LEVEL == 'S'):
        symbols = ['\n','?','¿',',','.','"',':',"'",'(',')']
        for s in symbols:
            corpus = corpus.replace(s,' '+s+' ')
        tokenized_text = [w for w in corpus.split(' ') if (w.strip() != '' or w == '\n')]

        if TOKEN_LEVEL == 'S':
            s = silabizer()
            tokenized_text = list(map(s, tokenized_text))
            flat_list = []
            for i, word in enumerate(tokenized_text):
                for sylab in word:
                    flat_list.append(sylab)
                if (word != ["\n"] and (i+1 < len(tokenized_text) and tokenized_text[i+1] != ["\n"])):
                    flat_list.append('\ ')
            tokenized_text = flat_list
    
    print(tokenized_text[:100])
    tokens = set(tokenized_text)
    return tokens, tokenized_text

def preprocess(dataset_path, experiment_path, TOKEN_LEVEL, SEQ_LEN, bpemb = None):
    '''From a corpus in dataset_path generates dictionaries word_indices, indices_word, a list of tokens and data for training (sentences, next_words)'''
    corpus = get_text(dataset_path, TOKEN_LEVEL)
    corpus = unicodedata.normalize('NFC', corpus)

    tokens, tokenized_text = tokenize(TOKEN_LEVEL, corpus, bpemb)

    word_indices = dict((c, i) for i, c in enumerate(tokens))
    indices_word = dict((i, c) for i, c in enumerate(tokens))

    sentences, next_words = shape_text(SEQ_LEN, tokenized_text, TOKEN_LEVEL, word_indices)
    
    print()
    print('El texto tokenizado consta de {} tokens, con {} tokens distintos'.format(len(tokenized_text), len(tokens)))
    items_preview = 50
    print('Previsualización de los primeros {} tokens: {}'.format(items_preview, tokenized_text[:items_preview]))
    print('En total hay {} ejemplos en el conjunto de entrenamiento, algunos de ellos: {}'.format(len(sentences), list(zip(sentences[:5], next_words[:5]))))
    print()

    return word_indices, indices_word, tokens, sentences, next_words
