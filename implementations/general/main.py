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
    if (input('Load experiment? Y-N') == 'Y'):
        EXP_NUMBER = input('Number of the experiment to be loaded')
    else:
        EXP_NUMBER = len(os.listdir(experiments_path))

    experiment_path = experiments_path + str(EXP_NUMBER) + '\\'

    if not os.path.exists(experiment_path):
        print('No experiment loaded')
        os.makedirs(experiment_path)
        
        TOKEN_LEVEL = input('Tokenization level: (B)PE, (W)ORDS, (S)YLLABLE')
        SEQ_LEN = input('Sequence lenght: ')
        MODEL = input('Language Model (LSTM - BPELSTM): ')

        if TOKEN_LEVEL == 'B':
            EMB_DIM = input('Embedding dimention: ')
            EMB_VS = input('Embedding Vocab Size: ')
            EMB_TRAIN = (input('Embedding trainable (Y-N): ') == 'Y')
            exp = Experiment(EXP_NUMBER, TOKEN_LEVEL, MODEL, SEQ_LEN, EMB_DIM, EMB_VS, EMB_TRAIN)
        else:
            exp = Experiment(EXP_NUMBER, TOKEN_LEVEL, MODEL, SEQ_LEN)

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

if exp.EPOCHS == 0:
    word_indices, indices_word, tokens, sentences, next_words = preprocess(dataset_path, experiment_path, exp.TOKEN_LEVEL, exp.SEQ_LEN, bpemb)

    model = getModel(exp, tokens, bpemb)
    model.summary()

    EPOCHS = input('Epochs to train:')
    history = train(model, experiment_path, 256, EPOCHS, tokens, word_indices)
    model.save(experiment_path + 'model.h5')
    exp.EPOCHS += EPOCHS

    text = generate(bpemb, model, indices_word, exp.SEQ_LEN, 'pokemon')
    generation_path = experiment_path + 'generated\\'
    os.makedirs(generation_path)
    with open(generation_path + 'generated_{}epochs.txt'.format(exp.EPOCHS), 'w') as generated_file:
        generated_file.write(text)
else:
    op = int(input('1) Preprocess\n2) Train\n3) Generate\n4) Export embeddings\n5) Exit'))

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

            EPOCHS = input('Epochs to train:')
            history = train(model, experiment_path, 256, EPOCHS, tokens, word_indices)
            exp.EPOCHS += EPOCHS
        if op == 3:
            model = keras.models.load_model(experiment_path + 'model.h5')
            print('Model loaded')

            with open(experiment_path + 'indices_word.json') as iw_file:
                indices_word = json.load(iw_file)
            text = generate(bpemb, model, indices_word, exp.SEQ_LEN, 'pokemon')
            generation_path = experiment_path + 'generated\\'
            with open(generation_path + 'generated_{}epochs.txt'.format(exp.EPOCHS), 'w') as generated_file:
                generated_file.write(text)
        if op == 4:
            export_embeddings(bpemb.emb, experiment_path)

with open(experiment_path + 'exp_file', 'wb') as exp_file:
    pickle.dump(exp, exp_file)
save_dict(exp.__dict__, experiment_path + 'exp_file.json')