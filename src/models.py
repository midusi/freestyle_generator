from keras.models import Sequential
from keras.layers import Embedding, Dense, Bidirectional, LSTM, Dropout, Activation

def getBasicLSTMModel(seq_len, num_tokens, lstm_size=256):
    model = Sequential()
    model.add(Bidirectional(LSTM(lstm_size), input_shape=(seq_len, num_tokens)))
    model.add(Dropout(0.2))
    model.add(Dense(num_tokens))
    model.add(Activation('softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def getEmbLSTMModel(seq_len, num_tokens, lstm_size=256, emb_dim=300, emb_trainable=True):
    model = Sequential()
    model.add(Embedding(num_tokens, emb_dim, input_length=seq_len, trainable=emb_trainable))
    model.add(Bidirectional(LSTM(lstm_size)))
    model.add(Dropout(0.2))
    model.add(Dense(num_tokens))
    model.add(Activation('softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model
