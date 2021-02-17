import re

class char():
    def __init__(self):
        pass
    
class char_line():
    def __init__(self, word):
        self.word = word
        self.char_line = [(char, self.char_type(char)) for char in word]
        self.type_line = ''.join(chartype for char, chartype in self.char_line)
        
    def char_type(self, char):
        if char in set(['a', 'á', 'e', 'é','o', 'ó', 'í', 'ú']):
            return 'V' #strong vowel
        if char in set(['i', 'u', 'ü']):
            return 'v' #week vowel
        if char=='x':
            return 'x'
        if char=='s':
            return 's'
        else:
            return 'c'
            
    def find(self, finder):
        return self.type_line.find(finder)
        
    def split(self, pos, where):
        return char_line(self.word[0:pos+where]), char_line(self.word[pos+where:])
    
    def split_by(self, finder, where):
        split_point = self.find(finder)
        if split_point!=-1:
            chl1, chl2 = self.split(split_point, where)
            return chl1, chl2
        return self, False
     
    def __str__(self):
        return self.word
    
    def __repr__(self):
        return repr(self.word)

class silabizer():
    def __init__(self):
        self.grammar = []
        
    def split(self, chars):
        rules  = [('VV',1), ('cccc',2), ('xcc',1), ('ccx',2), ('csc',2), ('xc',1), ('cc',1), ('vcc',2), ('Vcc',2), ('sc',1), ('cs',1),('Vc',1), ('vc',1), ('Vs',1), ('vs',1)]
        for split_rule, where in rules:
            first, second = chars.split_by(split_rule,where)
            if second:
                if first.type_line in set(['c','s','x','cs']) or second.type_line in set(['c','s','x','cs']):
                    #print 'skip1', first.word, second.word, split_rule, chars.type_line
                    continue
                if first.type_line[-1]=='c' and second.word[0] in set(['l','r']):
                    continue
                if first.word[-1]=='l' and second.word[-1]=='l':
                    continue
                if first.word[-1]=='r' and second.word[-1]=='r':
                    continue
                if first.word[-1]=='c' and second.word[-1]=='h':
                    continue
                return self.split(first)+self.split(second)
        return [chars]
        
    def __call__(self, word):
        return self.split(char_line(word))

def vocales(p):
    v = ['a', 'e', 'i', 'o', 'u']
    return [c for c in p if c in v]

def desde_tonica(palabra):
    'Devuelve los caracteres de palabra a partir de la sílaba tónica'
    tilde = re.search('(á|é|í|ó|ú).*', palabra)
    if tilde:
        return tilde[0]
    s = silabizer()
    silabas = s(palabra)
    if palabra[-1] in ['n', 's', 'a', 'e', 'i', 'o', 'u'] and len(silabas) > 1:
        for idx, c in enumerate(reversed(silabas[-2].word)):
            if c in ['a', 'e', 'i', 'o', 'u']:
                return (silabas[-2].word[-(idx + 1):] + silabas[-1].word)
    else:
        for idx, c in enumerate(reversed(silabas[-1].word)):
            if c in ['a', 'e', 'i', 'o', 'u']:
                return silabas[-1].word[-idx:]
    return ''

def rima(p1, p2):
    'Devuelve C si es una rima consonante, A si es una rima asonante o X si las palabras no riman'
    dt1, dt2 = desde_tonica(p1), desde_tonica(p2)
    return 'C' if dt1 == dt2 else 'A' if vocales(dt1) == vocales(dt2) else 'X'
