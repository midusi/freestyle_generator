class Experiment():

    def __init__(self, NUMBER, TOKEN_LEVEL, MODEL, SEQ_LEN, EMB_DIM = None, EMB_VS = None, EMB_TRAIN = None):
       self.NUMBER = NUMBER
       self.TOKEN_LEVEL = TOKEN_LEVEL
       self.MODEL = MODEL
       self.SEQ_LEN = SEQ_LEN
       self.EMB_DIM = EMB_DIM
       self.EMB_VS = EMB_VS
       self.EMB_TRAIN = EMB_TRAIN
       self.EPOCHS = 0
    
    def to_string(self):
        return (
            'exp{}_tokenLevel{}_seqLen{}_model{}'.format(self.NUMBER, self.TOKEN_LEVEL, self.SEQ_LEN, self.MODEL) + 
            ('_embDim{}_embVS{}_embTrain{}'.format(self.EMB_DIM, self.EMB_VS, self.EMB_TRAIN) if self.TOKEN_LEVEL == 'BPE' else '')
        )