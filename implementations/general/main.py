from bpemb import BPEmb
import os, pickle, json
import keras

from preprocessing import preprocess
from models import getModel
from train import train
from generation import generate
from utils import export_embeddings, save_dict
from Experiment import Experiment


def init(experiments_path):
    load = (input('Load experiment? (Y-N) (N): ' ) or 'N')
    if (load  == 'Y' or  load == 'y'):
        EXP_NUMBER = input('Number of the experiment to be loaded: ')
    else:
        if not os.path.exists(experiments_path):
            os.makedirs(experiments_path)
        EXP_NUMBER = len(os.listdir(experiments_path))

    experiment_path = experiments_path + str(EXP_NUMBER) + '\\'

    if not os.path.exists(experiment_path):
        print('No experiment loaded')
        
        TOKEN_LEVEL = input('Tokenization level ((B)PE, (W)ORDS, (S)YLLABLE): ')
        SEQ_LEN = int(input('Sequence lenght (4): ') or '4')
        MODEL = input('Language Model ((L)STM - (B)PELSTM): ')

        if TOKEN_LEVEL == 'B':
            EMB_DIM = int(input('Embedding dimention (300): ') or '300')
            EMB_VS = int(input('Embedding Vocab Size (10000): ') or '10000')
            EMB_TRAIN = ((input('Embedding trainable (Y-N) (N): ') or 'N') == 'Y')
            exp = Experiment(EXP_NUMBER, TOKEN_LEVEL, MODEL, SEQ_LEN, EMB_DIM, EMB_VS, EMB_TRAIN)
        else:
            exp = Experiment(EXP_NUMBER, TOKEN_LEVEL, MODEL, SEQ_LEN)
            
        os.makedirs(experiment_path)
    else:
        with open(experiment_path + 'exp_file', 'rb') as exp_file:
            exp = pickle.load(exp_file)
        print('Loaded experiment {}'.format(exp.NUMBER))
        print('Details: {}'.format(exp.__dict__))
    
    return exp, experiment_path


path = 'D:\\Documentos\\GitHub\\freestyle_generator\\'
dataset_path = path + 'datasets\\freestyle_lyrics\\lyrics\\'
experiments_path = path + 'implementations\\general\\experiments\\'

exp, experiment_path = init(experiments_path)

if exp.TOKEN_LEVEL == 'B':
    bpemb = BPEmb(lang="es", dim=exp.EMB_DIM, vs=exp.EMB_VS)
else:
    bpemb = None

if exp.EPOCHS == 0:
    word_indices, indices_word, tokens, sentences, next_words = preprocess(dataset_path, experiment_path, exp.TOKEN_LEVEL, exp.SEQ_LEN, bpemb)

    with open(experiment_path + 'word_indices.json') as wi_file:
        word_indices = json.load(wi_file)

    model = getModel(exp, tokens, bpemb)
    model.summary()

    EPOCHS = int(input('Epochs to train: '))
    history = train(model, experiment_path, 256, EPOCHS, tokens, exp.TOKEN_LEVEL, word_indices)
    exp.EPOCHS += EPOCHS

    TEMP = int(input('Temperature (1): ') or '1')
    text = generate(bpemb, model, exp.TOKEN_LEVEL, indices_word, word_indices, exp.SEQ_LEN, TEMP, 'voy a ser el que en el')
    generation_path = experiment_path + 'generated\\'
    os.makedirs(generation_path)
    with open(generation_path + 'generated_{}epochs.txt'.format(exp.EPOCHS), 'w') as generated_file:
        generated_file.write(text)
else:
    op = int(input('1) Preprocess\n2) Train\n3) Generate\n4) Export embeddings\n5) Exit\n'))

    while op != 5:
        if op == 1:
            word_indices, indices_word, tokens, sentences, next_words = preprocess(dataset_path, experiment_path, exp.TOKEN_LEVEL, exp.SEQ_LEN, bpemb)
        if op == 2:
            model = keras.models.load_model(experiment_path + 'model.h5')
            print('Model loaded')
            model.summary()

            with open(experiment_path + 'tokens', 'rb') as tokens_file:
                tokens = pickle.load(tokens_file)
            with open(experiment_path + 'word_indices.json') as wi_file:
                word_indices = json.load(wi_file)
            
            EPOCHS = int(input('Epochs to train: '))
            history = train(model, experiment_path, 256, EPOCHS, tokens, exp.TOKEN_LEVEL, word_indices)
            exp.EPOCHS += EPOCHS
        if op == 3:
            model = keras.models.load_model(experiment_path + 'model.h5')
            print('Model loaded')

            with open(experiment_path + 'indices_word.json') as iw_file:
                indices_word = json.load(iw_file)
            with open(experiment_path + 'word_indices.json') as wi_file:
                word_indices = json.load(wi_file)

            TEMP = int(input('Temperature (1): ') or '1')

            text = generate(bpemb, model, exp.TOKEN_LEVEL, indices_word, word_indices, exp.SEQ_LEN, TEMP, 'voy a ser el que en el')
            print(text)
            generation_path = experiment_path + 'generated\\'
            with open(generation_path + 'generated_{}epochs.txt'.format(exp.EPOCHS), 'w') as generated_file:
                generated_file.write(text)
        if op == 4:
            export_embeddings(bpemb.emb, experiment_path)
        
        op = int(input('1) Preprocess\n2) Train\n3) Generate\n4) Export embeddings\n5) Exit\n'))

with open(experiment_path + 'exp_file', 'wb') as exp_file:
    pickle.dump(exp, exp_file)
save_dict(exp.__dict__, experiment_path + 'exp_file.json')