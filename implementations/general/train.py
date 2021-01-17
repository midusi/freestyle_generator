import pickle, os
import numpy as np

# Data generator for fit and evaluate
def generator(sentence_list, next_word_list, batch_size, tokens, word_indices): 
    while True:
        for i in range(int(len(sentence_list)/batch_size)):
            x = sentence_list[i*batch_size:(i+1)*batch_size]
            x = np.array([np.array(xi) for xi in x])
            y = next_word_list[i*batch_size:(i+1)*batch_size]
            y = [[1 if i == word_indices[str(token)] else 0 for i in range(len(tokens))] for token in y]
            y = np.array([np.array(yi) for yi in y])
            yield x, y

def train(model, experiment_path, BATCH_SIZE, EPOCHS, tokens, word_indices):

    with open(experiment_path + 'sentences', 'rb') as sentences_file:
        sentences = pickle.load(sentences_file)

    with open(experiment_path + 'next_words', 'rb') as next_words_file:
        next_words = pickle.load(next_words_file)

    history = model.fit(
        generator(sentences, next_words, BATCH_SIZE, tokens, word_indices),
        epochs=EPOCHS,
        steps_per_epoch=int(len(sentences)/BATCH_SIZE) + 1
    )

    return history
