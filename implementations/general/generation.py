import numpy as np
from bpemb import BPEmb

def sample(preds, temperature=1.0):
    '''Helper function to sample an index from a probability array'''
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate(bpemb, model, indices_word, SEQ_LEN, seed):
    text = np.flip(np.array(bpemb.encode_ids(seed)))

    for _ in range(100):
        inp = text[-SEQ_LEN:]
        out = model.predict(inp)[0]
        next_id = sample(out,1)
        #next_id = np.argmax(out)
        
        next_id = indices_word[next_id]
        #print(inp, next_id)
        text = np.append(text, next_id)
        
    text = np.flip(text)
    text = bpemb.decode_ids(text)

    return text