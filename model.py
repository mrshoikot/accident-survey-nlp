import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
import csv
from word2number import w2n
import re
import json

# nltk.download('all')

df = pd.read_csv('dataset/news.csv', names=["url", "date", "headline", "news", "platform", "death", "injury", "location", "vehicle", ""])
dataset = list(csv.reader(open("dataset/news.csv")))


def linearsearch(arr, x):
   for i in range(len(arr)):
      result = re.search(arr[i].lower(), x)
      if result is not None:
        return result.group(0)

def formatVehicle(v):
    v = row[8].replace(' ','').replace('-','').lower()
    if v and v[-1] == 's' and v[-3:] != 'bus':
        v = v[:-1]

    if v == 'motorbike':
        v='motorcycle'

    if v == 'bu':
        v = 'bus'

    return v

for row in dataset:

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

input = list(csv.reader(open("input.csv")))
writer = csv.writer(open('output.csv', 'w'))
count = 0
success = 0
failed = 0

vehicleTypes = []
places = json.loads(open('dataset/places.json').read())
linearPlaces = []

for division in places:
    for district in places[division]:
        for place in places[division][district]:
            linearPlaces.append([place, district, division])

# print(dataset[0][8])

for row in dataset:
    v = formatVehicle(row[8])

    if v and v not in vehicleTypes and v:
        vehicleTypes.append(v)

print(vehicleTypes)

writer.writerow(["url", "date", "headline", "news", "platform", "death", "injury", "location", "vehicle"])

isHeader = True

for row in input:

    if isHeader:
        isHeader = False
        continue

    count += 1
    row.append('')
    row.append('')
    sentence = row[3].split('.')[0]
    spl = sentence.split('kill')
    try:
        digit = re.search("[1-9][0-9]*", spl[0])
        if digit is not None:
            row[5] = digit.group(0)
        else:
            row[5] = w2n.word_to_num(spl[0])
    except:
        if row[3][:2] == 'A ':
            row[5] = 1
        else:
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

    row.append('')
    row.append('')

    for placeItem in linearPlaces:
        place = re.search(placeItem[0].lower(), row[3].lower())
        if place:
            row[7] = (placeItem[1])
            break
        else:
            district = re.search(placeItem[1].lower(), row[3].lower())
            if district:
                row[7] = (placeItem[1])
                break

    
    row[8] = linearsearch(vehicleTypes, row[3].replace(' ','').replace('-','').lower())

    if row[6] == 0 and row[5] == 0:
        failed += 1
    else:
        success += 1

    if int(row[5]) > 15:
        continue

    writer.writerow(row[0:9])

print("Total: "+str(count))
print("Success: "+str(success))
print("Failed: "+str(failed))
print("Success rate: "+str(success/count*100)+"%")


output = pd.read_csv('dataset/news.csv', names=["url", "date", "headline", "news", "platform", "death", "injury", "location", "vehicle"])



# output.plot(kind='scatter',x='platform',y='death',color='red')
# plt.show()