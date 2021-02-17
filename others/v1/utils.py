import io, json

def export_embeddings(w2v, path):
    '''Generates embeddings files to use in TF embbedings visualizer (use with bpemb.emb as w2v)'''
    out_v = io.open(path + 'vecs.tsv', 'w', encoding='utf-8')
    out_m = io.open(path + 'meta.tsv', 'w', encoding='utf-8')
    for index in range(len(w2v.index2word)):
        word = w2v.index2word[index]
        vec = w2v.vectors[index]
        out_m.write(word + "\n")
        out_v.write('\t'.join([str(x) for x in vec]) + "\n")
    out_v.close()
    out_m.close()

def save_dict(data, path):
    '''Stores python dictionary in json file'''
    with io.open(path, 'w') as dict_file:
        json.dump(data, dict_file)
