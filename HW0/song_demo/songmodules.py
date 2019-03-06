import os
import pickle
import jieba
import operator
import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from datetime import datetime
from collections import Counter

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.moses import MosesTokenizer

font_path = '../tool/msjh.ttc'
font = font_manager.FontProperties(fname='../tool/msjh.ttc',
                                   weight='bold',
                                   style='normal', size=16)

import_stop = []
#自己建立一個stopword檔案
with open('stopword.txt', 'r', encoding='UTF-8') as file:
    for each in file.readlines():
        import_stop.append(each.strip())
    import_stop.append(' ')

#使用string去除punctuation
def remove_punctuation(content_string):
    translator = str.maketrans('', '', string.punctuation)
    clean_content = content_string.translate(translator)
    return(clean_content)

def remove_chinese_words(content):
    words = [word for word in content if word.isalpha()]
    return(words)

def cut_words(data):
    #stopWords = set(nltk.corpus.stopwords.words('english'))
    stopwords = nltk.corpus.stopwords.words('english')
    #新增stopwords
    for i in import_stop:
        stopwords.append(i)
    #stopwords.append('：')
    moses = MosesTokenizer()
    words = moses.tokenize(data)
    wordsFiltered = []

    for w in words:
        if w not in stopwords:
            wordsFiltered.append(w)
    return(wordsFiltered)
'''
    words = word_tokenize(data)
    wordsFiltered = []

    for w in words:
        if w not in stopwords:
            wordsFiltered.append(w)
'''
    

def sort_dict_by_values(d):
    return(sorted(d.items(), key=lambda x: x[1], reverse=True))


def song_get_coshow(contents):
    coshow_dict = {}
    cat_content = ' '.join(contents)
    clean_content = remove_punctuation(cat_content)
    cut_content = cut_words(clean_content)
    cut_content = remove_chinese_words(cut_content)
    
    cut_content = list(filter(lambda x: x!=' ', cut_content))
    for i in cut_content:
        try:
            coshow_dict[i] = coshow_dict[i] + 1
        except:
            coshow_dict[i] = 1

    sdbv = sort_dict_by_values(coshow_dict)
    return sdbv

def get_wordcloud_of_keywords(keyword_dict, image_path=False):
    if image_path:
        coloring = np.array(Image.open(os.path.join(image_path)))
        color_func = ImageColorGenerator(coloring)
        wc = WordCloud(max_font_size=300,
                       #background_color="white",
                       mask=coloring,
                       color_func=color_func,
                       font_path=font_path,
                       width=300, height=300,
                      max_words=10000)
    else:
        wc = WordCloud(max_font_size=30,
                       #background_color="white",
                       colormap='Set2',
                       font_path=font_path,
                       width=1000, height=300,
                      max_words=1000)
    im = wc.generate_from_frequencies(keyword_dict)
    return im