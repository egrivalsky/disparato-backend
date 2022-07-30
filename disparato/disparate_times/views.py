from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from datamuse import datamuse
from . import models
datamuse=datamuse.Datamuse()

error_object = {
    'error': True,
    'displayMessageToUser': False,
    'message': "Something went wrong",
    'origin': "origin unknown"
}

def index(request):
    return HttpResponse('hello')

def update_or_create_2_deg(anyWord):
    db = models.Word

    if not db.objects.filter(word=anyWord):
        related = datamuse.words(rel_trg=anyWord)
        db.objects.create(
        word = anyWord,
        written = datetime.datetime.now(),
        last_accessed = datetime.datetime.now(),
        times_accessed = 1,
        rel_word = related
    )
        return related


    else:
        word_entry = db.objects.filter(word=anyWord)
        this_pk = list(word_entry.values('pk'))[0]['pk']
        record = db.objects.get(pk=this_pk)
        related = record.rel_word
        word_entry.update(last_accessed=datetime.datetime.now())
        word_entry.update(times_accessed = record.times_accessed + 1)

        return related

def update_or_create(anyWord):
    print('46')
    db = models.Word
    print('48')
    if not db.objects.filter(word=anyWord):
        related = datamuse.words(rel_trg=anyWord)
        if type(related) == list and len(related) > 0:
            db.objects.create(
            word = anyWord,
            written = datetime.datetime.now(),
            last_accessed = datetime.datetime.now(),
            times_accessed = 1,
            rel_word = related
        )
            return related
        else:
            error_object['displayMessageToUser'] = True;
            error_object['message'] = f"DataMuse did not find any words related to {anyWord}.";
            error_object['origin'] = "update_or_create function";
            print(error_object['message']);

            return error_object

    else:
        word_entry = db.objects.filter(word=anyWord)
        this_pk = list(word_entry.values('pk'))[0]['pk']
        record = db.objects.get(pk=this_pk)
        related = record.rel_word
        word_entry.update(last_accessed=datetime.datetime.now())
        word_entry.update(times_accessed = record.times_accessed + 1)

        return related

def related_words(request, word1, word2):
    print('these are the words: ' + word1 + ', ' + word2)
    response = update_or_create(word1)
    if type(response) == dict and response['error']:
        print('981')
        return HttpResponse(json.dumps(response), content_type="application/json")
    elif type(response) != list:
        error_object['displayMessageToUser'] = True;
        error_object['message'] = "improper response from datamuse"
        error_object['origin'] = "related_words function"
        print('87')
        return HttpResponse(json.dumps(error_object), content_type="application/json")
    elif len(response) < 1:
        error_object['message'] = "no relations found"
        error_object['origin'] = "related_words function"
        print('92')
        return HttpResponse(json.dumps(error_object), content_type="application/json")
    else:
        related1 = response
        print('96')

    word1_list = []

    for n in related1:
        related_word = n['word']
        word1_list.append(related_word)

    # find words related to word2
    response = update_or_create(word2)
    if type(response) == dict and response['error']:
        return HttpResponse(json.dumps(response), content_type="application/json")
    elif type(response) != list:
        print(type(response))
        error_object['displayMessageToUser'] = True;
        error_object['message'] = "improper response from datamuse"
        error_object['origin'] = "related_words function"
        return HttpResponse(json.dumps(error_object), content_type="application/json")
    elif len(response) < 1:
        error_object['message'] = "no relations found"
        error_object['origin'] = "related_words function"
        return HttpResponse(json.dumps(error_object), content_type="application/json")
    else:
        related2 = response
    
    word2_list = []

    for n in related2:
        related_word = n['word']
        word2_list.append(related_word)

    word1_set = set(word1_list)
    word2_set = set(word2_list)
    words_in_common = word1_set&word2_set
    go_deeper_list1 = word1_set - words_in_common
    go_deeper_list2 = word2_set - words_in_common

    disparato = {
        'wordOne': word1,
        'wordTwo': word2,
        'immediateWords': list(words_in_common),
        'wordOneList': word1_list,
        'wordTwoList': word2_list,
        'goDeeperList1': list(go_deeper_list1),
        'goDeeperList2': list(go_deeper_list2),
    }

    
    # return JsonResponse(disparato)
    return HttpResponse(json.dumps(disparato), content_type="application/json")

@csrf_exempt
def second_degree_words(request):
    print("searching...")

    final_list_word1 = []
    final_list_word2 = []
    word1_checklist = [] #a list of third degree words to simplify checking word2 third-degree words against
    final_list = []
    lists = json.loads(request.body)

    # Payload from request.body = lists: 
    #    {
        # "wordOne": w1,
        # "wordTwo": w2,
        # "immediateWords": props.disparato,
        # "wordOneList": props.w1List,
        # "wordTwoList": props.w2List
    #    } 

    word_one = lists['wordOne']
    word_two = lists['wordTwo']
    usedWords = lists['immediateWords']
    word1_list = lists['wordOneList']
    word2_list = lists['wordTwoList']

    # # remove any immediately related words from word_one and word_2 lists

    wordOneDict = {}
    for word in word1_list:
        if word not in wordOneDict.keys():
            wordOneDict[word] = []
    
    for word in wordOneDict.keys():
        query_result = update_or_create_2_deg(word)
        if len(query_result) > 0:
            for item in query_result:
                if int(item['score']) > 950:
                    wordOneDict[word].append(item['word'])


    wordTwoDict = {}
    for word in word2_list:
        if word not in wordTwoDict.keys():
            wordTwoDict[word] = []
    
    for word in wordTwoDict.keys():
        query_result = update_or_create_2_deg(word)
        if len(query_result) > 0:
            for item in query_result:
                if int(item['score']) > 950 and word not in wordOneDict.keys():
                    wordTwoDict[word].append(item['word'])
    
    # # iterate through all third-degree words (values) in wordTwoDict
    # # and check each to see if it's also a third-degree word in WordOneDict

    wordOneTempList = []
    wordTwoTempList = []
    semiFinalDict = {}
    for entry in wordOneDict.keys():
        thisList = wordOneDict[entry]
        while len(thisList) > 0:
            thisWord = thisList.pop()
            wordOneTempList.append(thisWord)
            if thisWord not in semiFinalDict.keys():
                semiFinalDict[thisWord] = {'wordOneParent': [entry], 'wordTwoParent': []}
            else:
               semiFinalDict[thisWord]['wordOneParent'].append(entry)

    for entry in wordTwoDict.keys():
        thisList = wordTwoDict[entry]
        while len(thisList) > 0:
            thisWord = thisList.pop()
            wordTwoTempList.append(thisWord)
            if thisWord in semiFinalDict.keys():
                semiFinalDict[thisWord]['wordTwoParent'].append(entry)

    # group all common third-degree words in one list

    thirdDegWords = list(set(wordOneTempList) & set(wordTwoTempList))

    #iterate through thirdDegWords and create dictionary showing each word and its lineage
    finalList = []
    for word in thirdDegWords:
        d = {}
        d[word] = semiFinalDict[word]
        finalList.append(d)

    return HttpResponse(json.dumps(finalList), content_type="application/json")

def test_route(request, word):
    return HttpResponse('hello from the cloud, and... ' + word)
