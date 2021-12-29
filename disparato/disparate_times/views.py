from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from datamuse import datamuse


datamuse=datamuse.Datamuse()

# Create your views here.

def index(request):
    return HttpResponse('hello')

def related_words(request, word1, word2):
    
    print('these are the words: ' + word1 + ', ' + word2)

    #find words related to word1
    related1 = datamuse.words(rel_jja=word1)
    word1_list = []
    for n in related1:
        related_word = n['word']
        word1_list.append(related_word)

    #now find words related to each word in word1_list
    word1_cousins = []
    for n in word1_list:
        rel_word1 = n

        cuz_word_query = datamuse.words(rel_jja=rel_word1)

        for i in cuz_word_query:
            cousin_word = i['word']
            word1_cousins.append(cousin_word)
    word1_cuz_set = set(word1_cousins)

    # find words related to word2
    related2 = datamuse.words(rel_jja=word2)
    word2_list = []
    for n in related2:
        related_word = n['word']
        word2_list.append(related_word)
    
    #now find words related to each word in word2_list
    word2_cousins = []
    for n in word2_list:
        rel_word2 = n

        cuz_word_query = datamuse.words(rel_jja=rel_word2)

        for i in cuz_word_query:
            cousin_word = i['word']
            word2_cousins.append(cousin_word)
    word2_cuz_set = set(word2_cousins)

    original_words = {word1, word2}
    word1_set = set(word1_list)
    word2_set = set(word2_list)
    words_in_common = word1_set&word2_set
    common_cousins = word1_cuz_set&word2_cuz_set

    immediate_words = list(words_in_common)
    cousin_words = list(common_cousins)


    return JsonResponse({
        'wordOne': word1,
        'wordTwo': word2,
        'immediateWords': immediate_words,
        'cousinWords': cousin_words
    })

def test_route(request, word):
    return HttpResponse('hello from the cloud, and... ' + word)
