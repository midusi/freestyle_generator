import numpy as np
import random
from collections import OrderedDict
from rima import rima

def sample(preds, temperature=1.0):
    '''Helper function to sample an index from a probability array'''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def last_word_from_verse(ids, tokenizer):
    word = ''
    for token in map(lambda i: tokenizer.id_to_token(i), reversed(ids[:-1])):
        if token == '[SEP]':
            return word
        if '▁' in token:
            word = token[1:]
        else:
            word += token

def update_rhyme(preds, word, tokenizer):
    for index in range(tokenizer.get_vocab_size()):
        # if(preds[index]) > 0.8: # Modificar a verdaderas candidatas a sílaba
        rhyme = rima(word, tokenizer.id_to_token(index))
        preds[index] += (1.0 - preds[index])*(0.9 if rhyme == 'C' else 0.9 if rhyme == 'A' else 0)
        # preds = np.exp(preds)/sum(np.exp(preds)) # Compute softmax
    return preds

def get_ids_to_np_array(use_emb, sequence_len, tokenizer):
    def ids_to_np_array(ids):
        if not use_emb:
            inp = np.zeros((1, sequence_len, tokenizer.get_vocab_size()))
            for t, idx in enumerate(ids[-sequence_len:]):
                inp[0, t, idx] = 1
        else:
            inp = np.array(ids[-sequence_len:])
        return inp
    return ids_to_np_array

def token_that_rhymes(model, ids, tokenizer, word, temp, rhymes_dict, ids_to_np_array):
    if not word in rhymes_dict:
        print('Not rhyming words for ' + word)
        return None
    rhyming_words = [(word, 'C') for word in rhymes_dict[word]['C']] + [(word, 'A') for word in rhymes_dict[word]['A']]
    rhyming_words_probs = OrderedDict()
    for (rhyme_word, rhyme_type) in rhyming_words:
        possible_ids = ids.copy()
        encoding = tokenizer.encode(rhyme_word)
        probs = 1 if rhyme_type == 'C' else 0.5
        for token_id in reversed(encoding.ids):
            preds = model.predict(ids_to_np_array(possible_ids))[0]
            probs = probs*preds[token_id]
            possible_ids.append(token_id)
        rhyming_words_probs[rhyme_word] = probs

    probs_array = np.array(list(rhyming_words_probs.values()))
    probs_array = np.exp(probs_array)/sum(np.exp(probs_array)) #Compute softmax
    word = list(rhyming_words_probs.keys())[sample(np.array(probs_array), temp)]
    ids.extend(reversed(tokenizer.encode(word).ids[:-1]))

def gen_verse(model, ids, temp, tokenizer, ids_to_np_array):
    while True:
        inp = ids_to_np_array(ids)
        out = model.predict(inp)[0]
        next_id = sample(out, temp)
        ids.append(next_id)
        if tokenizer.id_to_token(next_id) == '[SEP]':
            break 

def gen_stanza(model, ids, temp, tokenizer, rhymes_dict, ids_to_np_array):
    ending_words = []
    scheme = random.choice([[0,1,2], [None, 0, 1], [None, 1, 0]])
    print(scheme)
    for i in range(4):
        gen_verse(model, ids, temp, tokenizer, ids_to_np_array)
        ending_words.append(last_word_from_verse(ids, tokenizer))
        if i < 3 and scheme[i] is not None:
            token_that_rhymes(model, ids, tokenizer, ending_words[scheme[i]], temp, rhymes_dict, ids_to_np_array)

def generate(model, seed, tokenizer, sequence_len, temp, amount, rhymes_dict, use_emb):
    encoding = tokenizer.encode(seed)
    ids = list(reversed(encoding.ids))

    for _ in range(amount):
        gen_stanza(model, ids, temp, tokenizer, rhymes_dict, get_ids_to_np_array(use_emb, sequence_len, tokenizer))
        ids.append(tokenizer.token_to_id('[SEP]'))

    text = ''.join(reversed(list(map(lambda i: tokenizer.id_to_token(i), ids)))).replace('[SEP]','\n').replace('▁', ' ')
    #VER TEMA VOCALES FUERTES Y DEBILES (AUTO)
    return text