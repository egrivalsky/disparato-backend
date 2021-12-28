from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
from datamuse import datamuse

datamuse=datamuse.Datamuse()

# Create your views here.

def index(request):
    return HttpResponse(word_list)

def related_words(request, word):
    print('this is the word: ' + word)
    related = datamuse.words(rel_jja=word)
    rhymes = datamuse.words(rel_rhy=word)
    print(word)
    word_list = []
    for n in related:
        related_words = n['word']
        word_list.append(related_words)
    for n in rhymes:
        related_words = n['word']
        word_list.append(related_words)
    # return render(request, 'related_words.html', {'word_list': word_list})
    print(word_list)
    return HttpResponse(word_list)