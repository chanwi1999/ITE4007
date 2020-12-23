import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os

opcodes = ['mov', 'push', 'call', 'pop', 'cmp', 'jz', 'lea', 'test', 'jmp', 'add', 'jnz', 'retn', 'xor', 'and', 'bt', 'fdivp', 'fild', 'fstcw', 'imul', 'int', 'nop', 'pushf', 'rdtsc', 'sbb', 'setb', 'setle', 'shld', 'std', '(bad)']

def sample(num):
    global opcodes, norm, mal

    dirname = os.getcwd() + '/' + str(num)
    allfiles = os.listdir(dirname)
    filelist = [filename for filename in allfiles]

    n = len(filelist)
#   n = 10
    data = []
    for i in range(0, n):
        fname = dirname + '/' + filelist[i]
        f = open(fname, 'r')
        lines = f.readlines()
        seq = ''
        for op in lines:
            seq += op   
        data.append(seq)
        f.close()

    data = np.array(data)
    t = TfidfVectorizer().fit(data)
    ops = t.get_feature_names()
    t = t.transform(data)
    t = t.toarray()

    B = []
    for i in range(0, len(opcodes)):
        if opcodes[i] in ops:
            idx = ops.index(opcodes[i])
            tmp = []
            for j in range(0, n):
                tmp.append(t[j][idx])
            B.append(tmp)
        else:
            tmp = []
            for j in range(0, n):
                tmp.append(0)
            B.append(tmp)

    t = np.array(B)

    return t

def cos_similarity(v1, v2):

    dot_product = np.dot(v1, v2)
    l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
    similarity = dot_product / l2_norm
    
    return similarity


def max_similarity(num, v1):
    
    maximum = 0
    for i in range(0, num.shape[1]):
        v2 = np.array(num[:,i]).reshape(-1,)
        res = cos_similarity(v1, v2)

        if maximum < res:
            maximum = res

    return maximum


def test(filename):
    fname = os.getcwd() + '/seq/' + filename

    if os.stat(fname).st_size ==  0:
        return np.array([0]*29).reshape(-1,)

    f = open(fname, 'r')
    lines = f.readlines()
    seq = ''
    for op in lines:
        seq += op
    f.close()

    seq = np.array([seq])
    tfidf = TfidfVectorizer().fit(seq.ravel())
    ops = tfidf.get_feature_names()
    tfidf = tfidf.transform(seq)
    tfidf = tfidf.toarray()

    A = []
    for i in range(0, len(opcodes)):
        if opcodes[i] in ops:
            idx = ops.index(opcodes[i])
            A.append(tfidf[0][idx])
        else:
            A.append(0)

    tfidf = np.array(A).reshape(-1,)
    return tfidf


def main():
    global opcodes

    normal = sample(0)
    malware = sample(1)

    dirname = os.getcwd() + '/seq'
    allfiles = os.listdir(dirname)
    filelist = [filename for filename in allfiles]

    cnt_norm = 0
    cnt_mal = 0
    n = len(filelist)
#    n = 10
    for i in range(0, n):
        
        tfidf = test(filelist[i])
        
        norm = max_similarity(normal, tfidf)
        mal = max_similarity(malware, tfidf)

        if norm > mal:
            cnt_norm += 1
        else:
            cnt_mal += 1

    print('normal code: ' + str(cnt_norm))
    print('malware: ' + str(cnt_mal))

main()
