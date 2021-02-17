import numpy as np

# Data generator for fit and evaluate
def generator(sentence_list, next_word_list, batch_size, vocab_size, use_emb): 
    while True:
        for i in range(int(len(sentence_list)/batch_size)):
            x = sentence_list[i*batch_size:(i+1)*batch_size]
            if not use_emb:
                x = [[[1 if i == token else 0 for i in range(vocab_size)] for token in xi] for xi in x]
                x = np.array([np.array([np.array(token) for token in xi]) for xi in x])
            else:
                x = np.array([np.array(xi) for xi in x])
            y = next_word_list[i*batch_size:(i+1)*batch_size]
            y = [[1 if i == token else 0 for i in range(vocab_size)] for token in y]
            y = np.array([np.array(yi) for yi in y])
            yield x, y

def train(model, BATCH_SIZE, EPOCHS, sentences, next_words, vocab_size, use_emb):
    history = model.fit(
        generator(sentences, next_words, BATCH_SIZE, vocab_size, use_emb),
        epochs=EPOCHS,
        steps_per_epoch=int(len(sentences)/BATCH_SIZE) + 1
    )
    return history
