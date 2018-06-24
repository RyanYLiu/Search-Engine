from Index import get_bookkeeping_content
import pickle
import operator
from collections import defaultdict
import numpy as np

def search_index(query, path_dict):
    inv_index = pickle.load(open("Inverted_index\\ranked.p", 'rb'))

    search_terms = query.split()
    query_postings = defaultdict(dict)
    for term in search_terms:
        if term in inv_index:
            posting_list = sorted(inv_index[term].items(), reverse=True, key=operator.itemgetter(1))
            query_postings[term] = posting_list

    temp_docs = {}
    final_docs = {}
    for posting in query_postings.values():
        for doc in posting:
            if doc[0] not in temp_docs:
                temp_docs[doc[0]] = doc[1]
            else:
                final_docs[doc[0]] = temp_docs.pop(doc[0]) + doc[1]

    if len(final_docs) < 10:
        temp_list = sorted(temp_docs.items(), reverse=True, key=operator.itemgetter(1))
        for n in range(10-len(final_docs)):
            final_docs[temp_list[n][0]] = temp_list[n][1]
            # print(temp_list[n])
    returned_links = sorted(final_docs.items(), reverse=True, key=operator.itemgetter(1))

    i = 1
    for ind in range(10):
        # print(returned_links[ind])
        print("{}. Document: {} URL: {}".format(i, returned_links[ind][0], path_dict[returned_links[ind][0]]))
        i += 1



if __name__ == "__main__":
    path_dict = get_bookkeeping_content()
    print("Type quit to end program\n--------------------------\n")
    while True:
        query = input("Search for: ")
        if query == "quit":
            break
        results = search_index(query.lower(), path_dict)
        print()