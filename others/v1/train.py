import pickle, os
import numpy as np

# Data generator for fit and evaluate
def generator(sentence_list, next_word_list, batch_size, TOKEN_LEVEL, tokens, word_indices): 
    while True:
        for i in range(int(len(sentence_list)/batch_size)):
            x = sentence_list[i*batch_size:(i+1)*batch_size]
            if TOKEN_LEVEL != 'B':
                x = [[[1 if i == word_indices[str(token)] else 0 for i in range(len(tokens))] for token in xi] for xi in x]
                x = np.array([np.array([np.array(token) for token in xi]) for xi in x])
            else:
                x = np.array([np.array(xi) for xi in x])
            y = next_word_list[i*batch_size:(i+1)*batch_size]
            y = [[1 if i == word_indices[str(token)] else 0 for i in range(len(tokens))] for token in y]
            y = np.array([np.array(yi) for yi in y])
            yield x, y

def train(model, experiment_path, BATCH_SIZE, EPOCHS, tokens, TOKEN_LEVEL, word_indices, sentences, next_words):

    history = model.fit(
        generator(sentences, next_words, BATCH_SIZE, TOKEN_LEVEL, tokens, word_indices),
        epochs=EPOCHS,
        steps_per_epoch=int(len(sentences)/BATCH_SIZE) + 1
    )

    model.save(experiment_path + 'model.h5')

    return history
