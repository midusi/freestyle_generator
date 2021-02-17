class Experiment():

    def __init__(self, NUMBER, MODEL, SEQ_LEN, VS):
       self.NUMBER = NUMBER
       self.MODEL = MODEL
       self.SEQ_LEN = SEQ_LEN
       self.VS = VS
       self.EPOCHS_TOTAL = 0
       self.EPOCHS_FREE = 0

    @staticmethod
    def from_json(data):
        exp = Experiment(None, None, None, None)
        exp.__dict__ = data
        return exp
    
    def to_string(self):
        return 'exp{}_seqLen{}_model{}_vs{}'.format(self.NUMBER, self.SEQ_LEN, self.MODEL, self.VS)
    
    def epochs_to_string(self):
        return 'epTot{}_epFree{}'.format(self.EPOCHS_TOTAL, self.EPOCHS_FREE)
