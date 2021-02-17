import numpy as np
from bpemb import BPEmb

from Syllabizer import silabizer



def sample(preds, temperature=1.0):
    '''Helper function to sample an index from a probability array'''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate(bpemb, model, TOKEN_LEVEL, indices_word, word_indices, SEQ_LEN, TEMP, seed):

    if TOKEN_LEVEL == 'B':
        text = bpemb.encode_ids(seed)
    elif TOKEN_LEVEL == 'W' or TOKEN_LEVEL == 'S':
        text = seed.split()
        if TOKEN_LEVEL == 'S':
            s = silabizer()
            text = list(map(s, text))
            flat_list = []
            for i, word in enumerate(text):
                for sylab in word:
                    flat_list.append(sylab)
                if (word != ["\n"] and (i+1 < len(text) and text[i+1] != ["\n"])):
                    flat_list.append('\ ')
            text = flat_list

    text = list(reversed(text))

    for _ in range(100):

        if TOKEN_LEVEL != 'B':
            inp = np.zeros((1, SEQ_LEN, len(indices_word)))
            for t, word in enumerate(text[-SEQ_LEN:]):
                inp[0, t, word_indices[word]] = 1.
        else:
            inp = text[-SEQ_LEN:]

        out = model.predict(inp)[0]
        next_id = sample(out, TEMP)
        #next_id = np.argmax(out)
        
        next_id = indices_word[str(next_id)]
        text.append(next_id)
        
    text = list(reversed(text))

    if TOKEN_LEVEL == 'B':
        text = bpemb.decode_ids(text)
    elif TOKEN_LEVEL == 'S':
        text = ''.join(text)
    elif TOKEN_LEVEL == 'W':
        text = ' '.join(text)

    return text