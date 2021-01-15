from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, Bidirectional, LSTM, Dropout, Activation

def getModel(exp, tokens, bpemb = None):
    if exp.MODEL == 'BPELSTM':
        return getBPEmbModel(exp.EMB_VS, exp.EMB_DIM, bpemb.vectors, exp.SEQ_LEN, len(tokens), 256, emb_trainable = exp.EMB_TRAIN)
    elif exp.MODEL == 'LSTM':
        return getBasicLSTMModel(exp.SEQ_LEN, len(tokens), 256)

def getBPEmbModel(emb_vs, emb_dim, emb_weights, seq_len, num_tokens, lstm_size, emb_trainable = False):
    model = Sequential()

    # define the model
    model = Sequential()
    model.add(Embedding(emb_vs, emb_dim, weights=[emb_weights], input_length=seq_len, trainable=emb_trainable))
    model.add(Bidirectional(LSTM(lstm_size)))
    model.add(Dropout(0.2))
    model.add(Dense(num_tokens))
    model.add(Activation('softmax'))

    # compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def getBasicLSTMModel(seq_len, num_tokens, lstm_size):
    model = Sequential()

    # define the model
    model = Sequential()
    model.add(Bidirectional(LSTM(lstm_size)))
    model.add(Dropout(0.2))
    model.add(Dense(num_tokens))
    model.add(Activation('softmax'))

    # compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model