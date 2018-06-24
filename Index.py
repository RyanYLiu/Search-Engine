from bs4 import BeautifulSoup
import pickle
import os
import json
# from nltk.tokenize import RegexpTokenizer
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

def get_bookkeeping_content():
    base = "WEBPAGES_RAW"
    bookkeeping = open(os.path.join(base,"bookkeeping.json"), 'r')
    bookkeeping_content = bookkeeping.read()
    bookkeeping.close()
    decoder = json.JSONDecoder()
    path_dict = decoder.decode(bookkeeping_content)
    return path_dict


def tokenize(text):
    token_freq = defaultdict(int)
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text, language='english')
    # tokens = RegexpTokenizer('\d+|\w+|').tokenize(text)
    for token in tokens:
        lower_token = token.lower()
        if lower_token not in stop_words and (lower_token.isalpha() or lower_token.isnumeric()):
            token_freq[token.lower()] += 1
    return token_freq

def create_inverted_index(path_dict):
    base = "WEBPAGES_RAW"
    inv_index = defaultdict(dict)
    sub_tag_indexes = [defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict)]
    # TODO: Implement weights on header, bold, strong, title tags
    sub_tags = ["title", "h1", "h2", "strong", "b"]
    # ranked_index = zip(sub_tags, sub_tag_indexes)

    num_docs = 0
    for path in path_dict.keys():
        add_doc = False
        html = open(os.path.join(base, path), 'r', encoding="utf-8")
        html_str = html.read()
        html.close()
        soup = BeautifulSoup(html_str, "lxml")

        # parse the body tag
        body_tag = soup.find_all("body")
        if body_tag == []:
            continue
        body_text = body_tag[0].get_text().strip()
        body_tokens = tokenize(body_text)
        if len(body_tokens) != 0:
            add_doc = True
            num_docs += 1
            for token,freq in body_tokens.items():
                inv_index[token][path] = freq
            for i in range(len(sub_tags)):
                temp = body_tag[0].find_all(sub_tags[i])
                for j in temp:
                    sub_tag_tokens = tokenize(j.get_text().strip())
                    if len(sub_tag_tokens) != 0:
                        for s_token,s_freq in sub_tag_tokens.items():
                            sub_tag_indexes[i][s_token][path] = s_freq
        # print(sub_tag_indexes)
        # parse the head tag
        head_tag = soup.find_all("head")
        if head_tag == []:
            continue
        head_text = head_tag[0].get_text().strip()
        head_tokens = tokenize(head_text)
        if len(head_tokens) != 0:
            if not add_doc:
                num_docs += 1
            for token,freq in head_tokens.items():
                inv_index[token][path] = freq
            for i in range(len(sub_tags)):
                temp = head_tag[0].find_all(sub_tags[i])
                for j in temp:
                    sub_tag_tokens = tokenize(j.get_text().strip())
                    if len(sub_tag_tokens) != 0:
                        for s_token,s_freq in sub_tag_tokens.items():
                            sub_tag_indexes[i][s_token][path] = s_freq

        if num_docs%1000 == 0:
            print(path)

    print("Unique tokens in index:", len(inv_index))
    print("Documents in corpus:", num_docs)
    pickle.dump(inv_index, open("Inverted_index\\title.p", 'wb'))
    for i in range(len(sub_tags)):
        pickle.dump(sub_tag_indexes[i], open("Inverted_index\\{}.p".format(sub_tags[i]), 'wb'))


def calc_tfidf():
    N = 37407
    inv_index = pickle.load(open("Inverted_index\\main.p", 'rb'))
    ranked_index = defaultdict(dict)
    for term in inv_index:
        df = len(inv_index[term])
        for doc,freq in inv_index[term].items():
            tfidf = (1+np.log10(freq)) * np.log10(N/df)
            ranked_index[term][doc] = tfidf
    pickle.dump(ranked_index, open("Inverted_index\\ranked.p", 'wb'))
    # print(inv_index["informatics"])
    # print(ranked_index["informatics"])
    # tf = len()
    # idf = np.log10(N/tf)
    # tfidf = (1+np.log10(tf)) * idf
    # return tfidf


if __name__ == "__main__":
    # path_dict = get_bookkeeping_content()
    # create_inverted_index(path_dict)
    calc_tfidf()
