

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
import csv
from word2number import w2n

df = pd.read_csv('dataset/news.csv', names=["url", "date", "headline", "news", "platform", "death", "injury", "location", "vehicle", ""])

for row in list(csv.reader(open("dataset/news.csv"))):

    row = row[3]

    ws_tok = nltk.tokenize.WhitespaceTokenizer()
    token_list = ws_tok.tokenize(row)
    print(token_list[0:10])

    tb_tokenizer = nltk.tokenize.treebank.TreebankWordTokenizer()
    token_list = tb_tokenizer.tokenize(row)
    print(token_list[0:10])

    from nltk import word_tokenize
    token_list = word_tokenize(row)
    print(token_list[0:10])

    from nltk.stem import PorterStemmer
    porter = PorterStemmer()
    porter_tokens = [porter.stem(token) for token in token_list]

    from nltk.stem import LancasterStemmer
    lanc = LancasterStemmer()
    lanc_tokens = [lanc.stem(token) for token in token_list]

    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    lemma_tokens = [lemmatizer.lemmatize(token) for token in token_list]
    pos_tags = nltk.pos_tag(token_list)
    print(pos_tags[0:10])

    def get_lemma_tag(pos_tag):
        if pos_tag.startswith('J'):
            return 'a'
        elif pos_tag.startswith('V'):
            return 'v'
        elif pos_tag.startswith('N'):
            return 'n'
        elif pos_tag.startswith('R'):
            return 'r'
        else:
            return ''
        
    list(nltk.bigrams(token_list))

    list(nltk.ngrams(token_list, 4))
import re

input = list(csv.reader(open("input.csv")))
writer = csv.writer(open('output.csv', 'w'))
count = 0
success = 0
failed = 0

for row in input:
    count += 1
    sentence = row[3].split('.')[0]
    spl = sentence.split('kill')
    try:
        digit = re.search("[1-9][0-9]*", spl[0])
        if digit is not None:
            row[5] = digit.group(0)
        else:
            row[5] = w2n.word_to_num(spl[0])
    except:
        row[5] = 0
    try:
        digit = re.search("[1-9][0-9]*", spl[1].split('injur')[0])
        if digit is not None:
            row[6] = digit.group(0)
        else:
            row[6] = w2n.word_to_num(spl[1].split('injur')[0])
    except Exception as e:
        # print(e)
        row[6] = 0

    if row[6] == 0 and row[5] == 0:
        failed += 1
    else:
        success += 1

    writer.writerow(row)

print("Total: "+str(count))
print("Success: "+str(success))
print("Failed: "+str(failed))
print("Success rate: "+str(success/count*100)+"%")