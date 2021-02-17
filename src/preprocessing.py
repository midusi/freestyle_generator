import glob, unicodedata, io, os
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Metaspace
from tokenizers.processors import TemplateProcessing

def get_text(dataset_path):
    '''Returns corpus from all txt files stored in dataset_path'''
    files = glob.glob(dataset_path + '/**/*.txt', recursive=True)
    corpora = ''

    for f in files:
        with io.open(f, 'r', encoding='utf-8') as fc:
            corpus = fc.read().lower().replace('\xa0', ' ').replace('\ufeff','')
            corpora += corpus + '\n\n'

    corpora = unicodedata.normalize('NFC', corpora)
    return corpora

def store_corpus(path, filename):
    corpus = get_text(path)
    with io.open(filename, 'w', encoding='utf-8') as corpus_file:
        corpus_file.write(corpus)

def get_bpe_tokenizer(vs, dataset_path):
    files = glob.glob(dataset_path + '/**/*.txt', recursive=True)

    tokenizer = Tokenizer(BPE(unk_token='[UNK]'))
    tokenizer.pre_tokenizer = Metaspace()
    trainer = BpeTrainer(vocab_size=vs, special_tokens=['[UNK]', '[SEP]'])
    tokenizer.train(files, trainer)
    tokenizer.post_processor = TemplateProcessing(
        single="$0 [SEP]",
        special_tokens=[("[SEP]", tokenizer.token_to_id("[SEP]"))],
    )
    return tokenizer

def shape_text(sequence_length, text, step=1):
    '''Cuts the text in semi-redundant sequences of sequence_length words'''
    sentences = []
    next_words = []
    for i in range(0, len(text) - sequence_length, step):
        sentences.append(list(reversed(text[i + 1: i + sequence_length + 1])))
        next_words.append(text[i])
    return sentences, next_words

if __name__ == "__main__":
    path = 'D:\\Documentos\\GitHub\\freestyle_generator\\'
    raw_path = path + 'raw\\'
    data_path = path + 'data\\'

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    store_corpus(raw_path, data_path + 'corpus.txt')
    store_corpus(raw_path + 'freestyle_lyrics\\', data_path + 'corpus_fs.txt')

    VS = 5000

    tokenizer = get_bpe_tokenizer(VS, data_path)
    tokenizer.save(data_path + "tokenizer-bpe-" + str(VS) + ".json")
