import io, os, json
import keras
from tokenizers import Tokenizer, Encoding

from preprocessing import shape_text
from models import getBasicLSTMModel, getEmbLSTMModel
from train import train
from generation import generate
from Experiment import Experiment


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

    if not os.path.exists(experiment_path):
        print('No experiment loaded')
        
        SEQ_LEN = int(input('Sequence lenght (5): ') or '5')
        MODEL = input('Language Model ((L)STM - (E)MBLSTM): ')
        VS = int(input('Vocabulary size (5000): ') or '5000')

        exp = Experiment(EXP_NUMBER, MODEL, SEQ_LEN, VS)
            
        os.makedirs(experiment_path)
        os.makedirs(weights_path)
        os.makedirs(generation_path)
    else:
        with open(experiment_path + 'exp_file.json', 'r') as exp_file:
            exp = Experiment.from_json(json.load(exp_file))
        print('Loaded experiment {}'.format(exp.NUMBER))
        print('Details: {}'.format(exp.__dict__))
    
    return exp, experiment_path, weights_path, generation_path


path = 'D:\\Documentos\\GitHub\\freestyle_generator\\'
dataset_path = path + 'data\\'
experiments_path = path + 'experiments\\'

exp, experiment_path, weights_path, generation_path = init(experiments_path)

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
        DS = input('Dataset ((A)ll - (F)ree): ')
        corpus_path = dataset_path + ('corpus.txt' if (DS == 'A' or DS == 'a') else 'corpus_fs.txt')
        with open(corpus_path, 'r', encoding='utf-8') as corpus_file:
            corpus = corpus_file.read()

        encoder = Encoding.merge(tokenizer.encode_batch(list(filter(lambda line: line, corpus.split('\n')))))
        sentences, next_words, sentences_test, next_words_test = shape_text(exp.SEQ_LEN, encoder.ids)

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
        temp = int(input('Temperature (1): ') or '1')
        amount = int(input('Verse amount (5): ') or '5')
        seed = 'me voy yendo'
        with open(dataset_path + 'rhymes.json', 'r') as rhymes_dict_file:
            rhymes_dict = json.load(rhymes_dict_file)

        text = generate(model, seed, tokenizer, exp.SEQ_LEN, temp, amount, rhymes_dict, exp.MODEL == 'E')
        
        with open(generation_path + 'generated_{}epochs.txt'.format(exp.epochs_to_string()), 'w', encoding='utf-8') as generated_file:
            generated_file.write(text)
    
    op = int(input('1) Train\n2) Generate\n3) Exit\n'))
