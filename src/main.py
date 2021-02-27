import io, os, json, pickle
import keras
from tokenizers import Tokenizer, Encoding

from preprocessing import shape_text
from models import getBasicLSTMModel, getEmbLSTMModel
from train import train
from generation import generate, generate_simple
from Experiment import Experiment


def get_local_training_data(path):
    with open(path + 'sentences', 'rb') as sentences_file, open(path + 'next_words', 'rb') as next_words_file, open(path + 'sentences_test', 'rb') as sentences_test_file, open(path + 'next_words_test', 'rb') as next_words_test_file:
        sentences = pickle.load(sentences_file)
        next_words = pickle.load(next_words_file)
        sentences_test = pickle.load(sentences_test_file)
        next_words_test = pickle.load(next_words_test_file)
    return sentences, next_words, sentences_test, next_words_test

def store_local_training_data(path, sentences, next_words, sentences_test, next_words_test):
    with open(path + 'sentences', 'wb') as sentences_file, open(path + 'next_words', 'wb') as next_words_file, open(path + 'sentences_test', 'wb') as sentences_test_file, open(path + 'next_words_test', 'wb') as next_words_test_file:
        pickle.dump(sentences, sentences_file)
        pickle.dump(next_words, next_words_file)
        pickle.dump(sentences_test, sentences_test_file)
        pickle.dump(next_words_test, next_words_test_file)

def store_history(history_path, history):
    if not os.path.isfile(history_path):
        with io.open(history_path, 'w') as history_file:
            json.dump(history.history, history_file)
    else:
        with io.open(history_path, 'r') as history_file:
            old_history = json.load(history_file)
        for key in old_history.keys():
            old_history[key] = old_history[key] + history.history[key]
        with io.open(history_path, 'w') as history_file:
            json.dump(old_history, history_file)

def init(experiments_path):
    load = (input('Load experiment? (Y-N) (N): ' ) or 'N')
    if (load  == 'Y' or  load == 'y'):
        EXP_NUMBER = input('Number of the experiment to be loaded: ')
    else:
        if not os.path.exists(experiments_path):
            os.makedirs(experiments_path)
        EXP_NUMBER = len(os.listdir(experiments_path))

    experiment_path = experiments_path + str(EXP_NUMBER) + '\\'
    weights_path = experiment_path + 'weights\\'
    generation_path = experiment_path + 'generated\\'
    local_data_path = experiment_path + 'data\\'

    if not os.path.exists(experiment_path):
        print('No experiment loaded')
        
        SEQ_LEN = int(input('Sequence lenght (5): ') or '5')
        MODEL = input('Language Model ((L)STM - (E)MBLSTM): ')
        VS = int(input('Vocabulary size (5000): ') or '5000')

        exp = Experiment(EXP_NUMBER, MODEL, SEQ_LEN, VS)
            
        os.makedirs(experiment_path)
        os.makedirs(weights_path)
        os.makedirs(generation_path)
        os.makedirs(local_data_path)
        os.makedirs(local_data_path + 'songs\\')
        os.makedirs(local_data_path + 'fs\\')
    else:
        with open(experiment_path + 'exp_file.json', 'r') as exp_file:
            exp = Experiment.from_json(json.load(exp_file))
        print('Loaded experiment {}'.format(exp.NUMBER))
        print('Details: {}'.format(exp.__dict__))
    
    return exp, experiment_path, weights_path, generation_path, local_data_path


path = 'D:\\Documentos\\GitHub\\freestyle_generator\\'
dataset_path = path + 'data\\'
experiments_path = path + 'experiments\\'

exp, experiment_path, weights_path, generation_path, local_data_path = init(experiments_path)

tokenizer = Tokenizer.from_file(dataset_path + 'tokenizer-bpe-{}.json'.format(exp.VS))

if exp.EPOCHS_TOTAL == 0 and exp.EPOCHS_FREE == 0:
    model = getBasicLSTMModel(exp.SEQ_LEN, tokenizer.get_vocab_size()) if exp.MODEL == 'L' else getEmbLSTMModel(exp.SEQ_LEN, tokenizer.get_vocab_size())
else:
    print('Model loaded')
    model = keras.models.load_model(weights_path + 'model_{}.h5'.format(exp.epochs_to_string()))
model.summary()

with io.open(experiment_path + 'exp_file.json', 'w') as exp_file:
    json.dump(exp.__dict__, exp_file)

op = int(input('1) Train\n2) Generate\n3) Exit\n'))
while op != 3:
    if op == 1:
        # TRAINING
        DS = input('Dataset ((S)ongs - (F)ree): ')
        corpus_path = dataset_path + ('corpus.txt' if (DS == 'S' or DS == 's') else 'corpus_fs.txt')
        local_data_path = local_data_path + ('songs\\' if (DS == 'S' or DS == 's') else 'fs\\')

        if os.path.isfile(local_data_path + 'sentences'):
            sentences, next_words, sentences_test, next_words_test = get_local_training_data(local_data_path)
        else:
            with open(corpus_path, 'r', encoding='utf-8') as corpus_file:
                corpus = corpus_file.read()
            encoder = Encoding.merge(tokenizer.encode_batch(list(filter(lambda line: line, corpus.split('\n')))))
            sentences, next_words, sentences_test, next_words_test = shape_text(exp.SEQ_LEN, encoder.ids)
            store_local_training_data(local_data_path, sentences, next_words, sentences_test, next_words_test)

        EPOCHS = int(input('Epochs to train: '))
        history = train(model, 256, EPOCHS, sentences, next_words, sentences_test, next_words_test, tokenizer.get_vocab_size(), exp.MODEL == 'E')
        if (DS == 'A' or DS == 'a'):
            exp.EPOCHS_TOTAL += EPOCHS
            store_history(experiment_path + 'history_a.json', history)
        else:
            exp.EPOCHS_FREE += EPOCHS
            store_history(experiment_path + 'history_f.json', history)
        model.save(weights_path + 'model_{}.h5'.format(exp.epochs_to_string()))

        with io.open(experiment_path + 'exp_file.json', 'w') as exp_file:
            json.dump(exp.__dict__, exp_file)
    if op == 2:
        # GENERATION
        temp = float(input('Temperature (1): ') or '1')
        amount = int(input('Verse amount (5): ') or '5')
        seed = 'en la improvisación'
        with open(dataset_path + 'rhymes.json', 'r') as rhymes_dict_file:
            rhymes_dict = json.load(rhymes_dict_file)

        text = generate(model, seed, tokenizer, exp.SEQ_LEN, temp, amount, rhymes_dict, exp.MODEL == 'E')
        with open(generation_path + 'generated_{}epochs.txt'.format(exp.epochs_to_string()), 'a', encoding='utf-8') as generated_file:
            generated_file.write(text)
    
    op = int(input('1) Train\n2) Generate\n3) Exit\n'))
