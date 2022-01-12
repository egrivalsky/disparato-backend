from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from datamuse import datamuse

datamuse=datamuse.Datamuse()

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



    # find words related to word2
    related2 =  datamuse.words(rel_jja=word2)
    word2_list = []
    for n in related2:
        related_word = n['word']
        word2_list.append(related_word)

    original_words = {word1, word2}
    word1_set = set(word1_list)
    word2_set = set(word2_list)
    words_in_common = word1_set&word2_set
    # common_cousins = word1_cuz_set&word2_cuz_set

    # immediate_words = list(words_in_common)

    disparato = {
        'wordOne': word1,
        'wordTwo': word2,
        'immediateWords': list(words_in_common),
        'wordOneList': word1_list,
        'wordTwoList': word2_list,
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
    lists = json.loads(request.body.decode('utf-8'))

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

    # remove any immediately related words from word_one and word_2 lists
    slim_word1_list = list(set(word1_list)-set(usedWords))
    slim_word2_list = list(set(word2_list)-set(usedWords))

    # find words related to each word in word1_list
    # add the word and it's score to third_deg_list_word1
    third_deg_obj_word1 = {}
    third_deg_list_word1 = []

    for this_word in slim_word1_list:

        third_deg_list_word1 = datamuse.words(rel_jja=this_word)

        if this_word not in third_deg_obj_word1:
            third_deg_obj_word1[this_word] = third_deg_list_word1
        else:
            third_deg_obj_word1[this_word] = third_deg_obj_word1[this_word] + third_deg_list_word1


    # find words related to each word in word2_list
    # add the word and it's score to third_deg_list_word2
    third_deg_obj_word2 = {}

    for this_word in slim_word2_list:

        third_deg_list_word2 = datamuse.words(rel_jja=this_word)

        if this_word not in third_deg_obj_word2:
            third_deg_obj_word2[this_word] = third_deg_list_word2
        else:
            third_deg_obj_word2[this_word] = third_deg_obj_word2[this_word].append(third_deg_list_word2)
    
    # iterate through all third-degree words in third_deg_obj_word2
    # and check each to see if it's also a third-degree word in third_deg_obj_word1

    for entry in third_deg_obj_word1.keys():
        final_dict1 = {}
        raw_data = third_deg_obj_word1[entry]
        if len(raw_data) > 0:
            for item in raw_data:
                if type(item) == dict:
                    if item['score']:
                        if int(item['score']) >= 950:
                            if item['word']:                        
                                this_word = item['word']
                                if type(this_word) == str and this_word != 'the':
                                    # word1_checklist.append(this_word)
                                    if this_word not in final_dict1.keys():
                                        final_dict1[this_word] = [entry]
                                    # final_dict1 = {this_word: entry }
                                    # final_list_word1.append(final_dict1)
                                    else:
                                        final_dict1[this_word].append(entry)


    third_deg_set_word1 = set(word1_checklist)

    for entry in third_deg_obj_word2.keys():
        final_dict = {}
        raw_data = third_deg_obj_word2[entry]
        if len(raw_data) > 0:
            for item in raw_data:
                if type(item) == dict:
                    if item['score']:
                        if int(item['score']) >= 950:
                            if item['word']:                        
                                this_word = item['word']
                                if type(this_word) == str and this_word != 'the':
                                    final_list_word2.append(this_word)
                                    if this_word in final_dict1.keys():
                                        print('149')
                                        if this_word not in final_dict.keys():
                                            print('150')
                                            final_dict[this_word] = {
                                                 'word_one_connection': [final_dict1[this_word]], 
                                                 'word_two_connection': [entry]
                                                }
                                            print('157')
                                        else:
                                            print('159')
                                            final_dict[this_word]['word_one_connection'].append(final_dict1[this_word])
                                            final_dict[this_word]['word_two_connection'].append(entry)
 
                                        # final_list.append(final_dict)

    print("WORD ONE WORDS:")
    print(final_dict1.keys())
    print("WORD TWO WORDS:")
    print(final_list_word2)
    print('SET: ')
    print(set(final_dict1.keys())&set(final_list_word2))
    print("FINAL LIST:")
    for key in final_dict.keys():
        print(key + ":")
        print(final_dict[key])

    # third_deg_list_word2.append(item['word'])
    # third_deg_set_word2 = set(third_deg_list_word2)



 
    
        


    # if it is, grab it's parent from each of the objects and send them 
    # to our ultimate json object for the front end
    # print(slim_word2_list)
    # print(third_deg_obj_word2)
    return HttpResponse('second degree words')

def test_route(request, word):
    return HttpResponse('hello from the cloud, and... ' + word)
