import numpy as np
from rima import rima

def sample(preds, temperature=1.0):
    '''Helper function to sample an index from a probability array'''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def update_rhyme(preds, word, tokenizer):
    for index in range(tokenizer.get_vocab_size()):
        # if(preds[index]) > 0.8: #Modificar a verdaderas candidatas a sílaba
        rhyme = rima(word, tokenizer.id_to_token(index))
        preds[index] += (1.0 - preds[index])*(0.8 if rhyme == 'C' else 0.6 if rhyme == 'A' else 0)
    return preds

def generate(model, seed, tokenizer, sequence_len, temp, amount, use_emb):
    encoding = tokenizer.encode(seed)
    ids = list(reversed(encoding.ids))

    last_word = ''
    for token in reversed(encoding.tokens):
        last_word += token
        if '▁' in token:
            break
    last_word = last_word[1:]

    line_count, verse_count = 0, 0
    is_last_word = False
    while verse_count < amount:

        if not use_emb:
            inp = np.zeros((1, sequence_len, tokenizer.get_vocab_size()))
            for t, idx in enumerate(ids[-sequence_len:]):
                inp[0, t, idx] = 1
        else:
            inp = np.array(ids[-sequence_len:])

        out = model.predict(inp)[0]
        if is_last_word:
            out = update_rhyme(out, last_word, tokenizer)

        next_id = sample(out, temp)

        if is_last_word:
            is_last_word = False
            last_word = tokenizer.id_to_token(next_id)

        if tokenizer.id_to_token(next_id) == '[SEP]':
            is_last_word = True
            if line_count < 3:
                line_count += 1
            else:
                ids.append(tokenizer.token_to_id('[SEP]'))
                line_count = 0
                verse_count += 1
        
        ids.append(next_id)

    text = ''.join(reversed(list(map(lambda i: tokenizer.id_to_token(i), ids)))).replace('[SEP]','\n').replace('▁', ' ')
        
    return text