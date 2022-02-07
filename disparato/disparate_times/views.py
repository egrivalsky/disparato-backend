from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from datamuse import datamuse
from . import models
datamuse=datamuse.Datamuse()

def index(request):
    return HttpResponse('hello')

def update_or_create(anyWord):
    db = models.Word

    if not db.objects.filter(word=anyWord):
        related = datamuse.words(rel_jja=anyWord)
        db.objects.create(
            word = anyWord,
            written = datetime.datetime.now(),
            last_accessed = datetime.datetime.now(),
            times_accessed = 1,
            rel_word = related
        )

        # print(f"{anyWord} added to db")
        # print("DIRECTLY FROM DATAMUSE:")
        # print(type(related))
        return related

    else:
        word_entry = db.objects.filter(word=anyWord)
        this_pk = list(word_entry.values('pk'))[0]['pk']
        # print(this_pk)
        # print(related)
        # this_pk = related[0]['pk']
        record = db.objects.get(pk=this_pk)
        related = record.rel_word
        word_entry.update(last_accessed=datetime.datetime.now())
        word_entry.update(times_accessed = record.times_accessed + 1)
        print(f"{anyWord} already in database, updated")
        # print(f"Times Accessed: {record.times_accessed}")
        # print(f"Last Access Time: {record.last_accessed}")
        # print(type(related))


        return related

def related_words(request, word1, word2):
    print('these are the words: ' + word1 + ', ' + word2) 
    related1 = update_or_create(word1)
    # #find words related to word1

    # db = models.Word
    # # keywords = db.objects.all()
    # # print(keywords)
    # if not db.objects.filter(word=word1):
    #     related1 = datamuse.words(rel_jja=word1)
    #     db.objects.create(
    #         word = word1,
    #         rel_word = related1,
    #         written = datetime.datetime.now()
    #     )

    #     print(f"{word1} added to db")


    #     # print(db.objects.filter(word1))
    #     # print(db.objects.filter(word1).rel_word)
    # else:
    #     word1_entry = db.objects.filter(word=word1)
    #     related1 = word1_entry.objects('rel_word')

    word1_list = []

    for n in related1:
        related_word = n['word']
        word1_list.append(related_word)



    # find words related to word2
    related2 =  update_or_create(word2)
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
    # lists = json.loads(request.body.decode('utf-8'))

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
    # slim_word1_list = list(set(word1_list)-set(usedWords))
    # slim_word2_list = list(set(word2_list)-set(usedWords))

    # find words related to each word in word1_list
    # add the word and it's score to third_deg_list_word1

    # word1_final_object = {}
    # third_deg_dict_word1 = {}
    # third_deg_list_word1 = []

    wordOneDict = {}
    for word in word1_list:
        if word not in wordOneDict.keys():
            wordOneDict[word] = []
    
    for word in wordOneDict.keys():
        query_result = update_or_create(word)
        if len(query_result) > 0:
            for item in query_result:
                if int(item['score']) > 950:
                    wordOneDict[word].append(item['word'])

    # for word in wordOneDict.keys():
    #     print(word)
    #     print(wordOneDict[word])



    # for this_word in word2_list:

    wordTwoDict = {}
    for word in word2_list:
        if word not in wordTwoDict.keys():
            wordTwoDict[word] = []
    
    for word in wordTwoDict.keys():
        query_result = update_or_create(word)
        if len(query_result) > 0:
            for item in query_result:
                if int(item['score']) > 950 and word not in wordOneDict.keys():
                    wordTwoDict[word].append(item['word'])

    # for word in wordTwoDict.keys():
    #     print(word)
    #     print(wordTwoDict[word])
    
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

                # finalDict[thisWord].update({'wordOneParent': prevValue.append(entry)})
                # finalDict[thisWord] = finalDict[thisWord]['wordOneParent'].append(entry)

    for entry in wordTwoDict.keys():
        thisList = wordTwoDict[entry]
        while len(thisList) > 0:
            thisWord = thisList.pop()
            wordTwoTempList.append(thisWord)
            if thisWord in semiFinalDict.keys():
                semiFinalDict[thisWord]['wordTwoParent'].append(entry)

    # group all common third-degree words in one list

    thirdDegWords = list(set(wordOneTempList) & set(wordTwoTempList))

    # print(len(wordOneTempList))
    # print(len(wordTwoTempList))
    # print(thirdDegWords)
    # print(len(thirdDegWords))

    #iterate through thirdDegWords and create dictionary showing each word and its lineage
    finalList = []
    for word in thirdDegWords:
        d = {}
        d[word] = semiFinalDict[word]
        finalList.append(d)

    # for i in range(len(finalList)):
    #     print(finalList[i])


        # if len(raw_data) > 0:
        #     for item in raw_data:
        #         if type(item) == dict:
        #             if item['score']:
        #                 if int(item['score']) >= 950:
        #                     if item['word']:                        
        #                         this_word = item['word']
        #                         if type(this_word) == str and this_word != 'the':
        #                             # word1_checklist.append(this_word)
        #                             if this_word not in final_dict1.keys():
        #                                 final_dict1[this_word] = [entry]
        #                             # final_dict1 = {this_word: entry }
        #                             # final_list_word1.append(final_dict1)
        #                             else:
        #                                 final_dict1[this_word].append(entry)


    # # third_deg_set_word1 = set(word1_checklist)

    # for entry in third_deg_obj_word2.keys():
    #     final_dict = {}
    #     raw_data = third_deg_obj_word2[entry]
    #     if len(raw_data) > 0:
    #         for item in raw_data:
    #             if type(item) == dict:
    #                 if item['score']:
    #                     if int(item['score']) >= 950:
    #                         if item['word']:                        
    #                             this_word = item['word']
    #                             if type(this_word) == str and this_word != 'the':
    #                                 final_list_word2.append(this_word)
    #                                 if this_word in final_dict1.keys():
    #                                     print('149')
    #                                     if this_word not in final_dict.keys():
    #                                         print('150')
    #                                         final_dict[this_word] = {
    #                                              'word_one_connection': [final_dict1[this_word]], 
    #                                              'word_two_connection': [entry]
    #                                             }
    #                                         print('157')
    #                                     else:
    #                                         print('159')
    #                                         final_dict[this_word]['word_one_connection'].append(final_dict1[this_word])
    #                                         final_dict[this_word]['word_two_connection'].append(entry)
 
    #                                     # final_list.append(final_dict)

    # print("WORD ONE WORDS:")
    # print(final_dict1.keys())
    # print("WORD TWO WORDS:")
    # print(final_list_word2)
    # print('SET: ')
    # print(set(final_dict1.keys())&set(final_list_word2))
    # print("FINAL LIST:")
    # for key in final_dict.keys():
    #     print(key + ":")
    #     print(final_dict[key])

    # third_deg_list_word2.append(item['word'])
    # third_deg_set_word2 = set(third_deg_list_word2)



 
    
        


    # if it is, grab it's parent from each of the objects and send them 
    # to our ultimate json object for the front end
    # print(slim_word2_list)
    # print(third_deg_obj_word2)
    return HttpResponse(json.dumps(finalList), content_type="application/json")

def test_route(request, word):
    return HttpResponse('hello from the cloud, and... ' + word)
