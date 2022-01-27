import operator
import re
import string
from bs4 import BeautifulSoup
import pandas as pd

import re
import string

import nltk
import pandas as pd
from bs4 import BeautifulSoup
from click._compat import raw_input
from parsivar import FindStems

import math
import random
import re
import string

import matplotlib
import heapq


matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup

def remove_punct(text):
    punctuations = string.punctuation + "،" + "؟"
    def change(ch):
        if ch in punctuations or ch.isdigit():
            return " "
        else:
            return ch
    no_punct = "".join([change(ch) for ch in text])
    return no_punct

def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    str = soup.get_text(" ")
    return str

def tokenize_1(text):
    tokens = re.split('\W+', text)
    return tokens

def making_sw(sw_dir):
    sw = []
    with open(sw_dir, encoding="utf8") as f:
        lines = f.readlines()
        for w in lines:
            sw.append(re.findall('\S+', w)[0])
    # adding br and empty string to stop words
    sw.append('br')
    sw.append('')
    return sw

def remove_sw(tokens,sw):
    text = [w for w in tokens if w not in sw and len(w)>=2]
    return text

def pre_process_1(str,sw):
    str = remove_html_tags(str)
    str = remove_punct(str)
    token_list = tokenize_1(str)
    token_list = remove_sw(token_list, sw)
    return token_list

def normalize(text):
    # Replace Arabic letters with Persian letters
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ی", text)
    text = re.sub("ك", "ک", text)
    text = re.sub("ۀ", "ه", text)
    text = re.sub("ء", "", text)
    text = re.sub("ة", "ه", text)
    # Replace all types of half-distance with distance
    text = re.sub("\u200c", " ", text)
    text = re.sub("\u200d", " ", text)
    text = re.sub("\xa0", " ", text)
    # Eliminate the vowels
    noise = re.compile(""" ّ |َ |ً |ُ |ٌ |ِ |ٍ |ْ |ـ""",re.VERBOSE)
    text = re.sub(noise, '', text)

    # delete mentions and peoples name
    text = re.sub(r'@[A-Za-z0-9_]+', ' ', text)
    # delete url
    text = re.sub(r'https?://[^ ]+', ' ', text)
    # delete url
    text = re.sub(r'www.[^ ]+', ' ', text)
    # Delete specific characters
    text = re.sub(r"[a-zA-Z!$()&@0-9:\\#/|{}<>?؟=.\"\'…»«;,،]", " ", text)
    # delete emoji
    emoji_pattern = u'([🤦🤗🤪🤷🤘🤣🤔🤐🤚🤢🤡])|([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])|([\U0001F1E0-\U0001F1FF])|([\U00002702-\U000027B0])|([\U000024C2-\U0001F251])'
    text = re.sub(emoji_pattern, ' ', text)

    # delete html tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(" ")

    # remove punctuations marks
    punctuations = string.punctuation + "،" + "؟"
    def change(ch):
        if ch in punctuations or ch.isdigit():
            return " "
        else:
            return ch
    no_punct = "".join([change(ch) for ch in text])
    return no_punct


def tokenize_2(text):
    after_verbs = ['ام', 'ای', 'است', 'ایم', 'اید', 'اند', 'بودم', 'بودی', 'بود']
    before_verbs = ['خواهم', 'خواهی', 'خواهد', 'خواهیم', 'خواهید', 'می', 'خواهند']
    ends = ['ات', 'ان', 'ترین', 'تر', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', 'ا', 'پذیر', 'بخش', 'مند', 'گیر']
    common_cw = ['غیر رسمی','غیر قانونی','سر سپرده','بی ‌تفاوت','به‌ عنوان','به‌ خاطر','به ویژه','ریيس‌ جمهور','شگفت انگیز','بی نظیر','ایده ال','گر چه','هر چند','بیش‌ از پیش','به راستی','سر در گم','بی نهایت','هر آنچه','سر انجام','مع ذلک','علی ای حال','بنا بر این','چنان چه','فیما بین']
    for cw in common_cw:
        if cw in text:
            str_rep = cw.replace(" ","\u200c")
            text = text.replace(cw,str_rep)
    tokens = text.split()
    for t in range(len(tokens)):
        if tokens[t] in after_verbs:
            tokens[t-1] = tokens[t-1] +" "+ tokens[t]
            tokens[t-1].replace(" ","\u200c")
            tokens[t] = " "
        if tokens[t] in before_verbs:
            tokens[t + 1] = tokens[t] +" "+ tokens[t+1]
            tokens[t + 1].replace(" ","\u200c")
            tokens[t] = " "
        if tokens[t] in ends:
            tokens[t - 1] = tokens[t - 1] +" "+ tokens[t]
            tokens[t-1].replace(" ","\u200c")
            tokens[t] = " "
    new_tokens = []
    for t in range(len(tokens)):
        if tokens[t] != " " and tokens[t] != "":
            new_tokens.append(tokens[t])
    return new_tokens

def stemming(tokens,stemming_list):
    my_stemmer = FindStems()
    new_tokens = []
    new = ""
    term = " "
    for w in tokens:
        term = w
        new = my_stemmer.convert_to_stem(w)
        # deal with
        if new == w:
            if w[-1] == 'ن':
                 w = w[:-1] + " " + w[-1]
            new = my_stemmer.convert_to_stem(w)
            if new[-1] == 'ن' and new[-2] == " ":
                new = new.replace(" ","")

        # dealing with 2 answers,and select better one
        if "&" in new:
            index = new.find('&')
            if new[index+1:] in w:
                new = new[index+1:]
            else:
                new = new[:index]
        new_tokens.append(new)
        if new != term:
            if new == "گفت" or new == "گو" or new == "رود" or new == "رو" or new == "خواه" or new == "سپاس" or new == "هنر" or new == "شریف" or new == "دوست" or new == "یاد" or new == "توان" or new == "شنو" or new == "کرد" or new == "ساز" or new == "دان" :
                if term not in stemming_list[new]:
                    stemming_list[new].append(term)
    return new_tokens,stemming_list


def pre_process_2(str,sw,stemming_list):
    str = normalize(str)
    token_list = tokenize_2(str)
    token_list,stemming_list = stemming(token_list,stemming_list)
    token_list = remove_sw(token_list, sw)
    return token_list,stemming_list

def create_index(part):

    sw = []
    sw = making_sw('stopwords-fa.txt')

    term_id = 0
    doc_id = 0
    termid_docid_pairs = []
    term_termid_match = {}

    termid_freq_perdoc = {}
    document_freq = {}

    # for heaps and zipf's law
    total_token_number = 0
    term_frequency = {}
    news = []
    T_M_dict = {}

    if part ==2:
        stemming_list = {}
        stemming_list["گفت"] = []
        stemming_list["گو"] = []
        stemming_list["رود"] = []
        stemming_list["رو"] = []
        stemming_list["خواه"] = []
        stemming_list["سپاس"] = []
        stemming_list["هنر"] = []
        stemming_list["شریف"] = []
        stemming_list["دوست"] = []
        stemming_list["یاد"] = []
        stemming_list["توان"] = []
        stemming_list["شنو"] = []
        stemming_list["کرد"] = []
        stemming_list["ساز"] = []
        stemming_list["دان"] = []

    news_title = {}
    file_names = ["ir-news-0-2.csv", "ir-news-2-4.csv", "ir-news-4-6.csv", "ir-news-6-8.csv", "ir-news-8-10.csv","ir-news-10-12.csv"]
    # file_names = ["ir-news-0-2.csv"]
    for l in range(len(file_names)):
        df = pd.read_csv(r"./doc_collection/" + file_names[l])
        contents = pd.DataFrame(df, columns=['content'])
        titles = pd.DataFrame(df,columns=['title'])
        for i in range(len(contents)):
            termid_freq = {}
            # print(i)
            str = contents.loc[i, "content"]
            news_title[doc_id] = titles.loc[i,"title"]
            news.append(str)
            if part == 1:
                token_list = pre_process_1(str,sw)
            elif part == 2:
                token_list,stemming_list = pre_process_2(str,sw,stemming_list)

            for token in token_list:
                total_token_number = total_token_number + 1
                # if we had term in dictionary
                if token in term_termid_match.keys():
                    pair = []
                    pair.append(term_termid_match[token])
                    pair.append(doc_id)
                    term_frequency[token] +=1
                    # if we dont had this termid_docid pait exactly in our list we dont append pair in list
                    if pair not in termid_docid_pairs:
                        termid_docid_pairs.append(pair)
                        # print(term_termid_match[token])
                        termid_freq[term_termid_match[token]] = 1
                        document_freq[term_termid_match[token]] += 1
                        # print(term_termid_match[token],pair)
                    elif pair in termid_docid_pairs:
                        # print(pair)
                        # if termid_freq[]
                        # print(term_termid_match[token], pair,termid_freq[term_termid_match[token]])
                        termid_freq[term_termid_match[token]] += 1
                # if we didnt have that term in our dictionary
                else:
                    pair = []
                    term_termid_match[token] = term_id
                    pair.append(term_id)
                    pair.append(doc_id)
                    termid_docid_pairs.append(pair)
                    termid_freq[term_id] = 1
                    document_freq[term_id] = 1
                    term_id += 1
                    term_frequency[token] = 1
                    # print("3")
                    # print(pair)
                    # print(term_id)
                T_M_dict[total_token_number] = len(term_termid_match)

            termid_freq_perdoc[doc_id] = termid_freq

            doc_id = doc_id + 1
            if i == 300:
                break

    champion_list = {}
    # making champion lists
    for term in term_termid_match:
        termid = term_termid_match[term]
        for d in termid_freq_perdoc:
            termid_frequency_dict = termid_freq_perdoc[d]
            term_ids = list(termid_frequency_dict.keys())
            term_freq = list(termid_frequency_dict.values())
            if termid in term_ids:
                freq = term_freq[term_ids.index(termid)]
                chamion_termids = list(champion_list.keys())
                if termid in chamion_termids:
                    champion_list[termid][d] = freq
                elif termid not in chamion_termids:
                    champion_list[termid] = {}
                    champion_list[termid][d] = freq
        champion_list[termid] = {k: v for k, v in sorted(champion_list[termid].items(), key=lambda item: item[1],reverse=True)}
        values = list(champion_list[termid].values())
        max_freq = max(values)
        test_dict = {}
        for k in champion_list[termid]:
            # ???????????????????????????????????????????????????????????????????????????????????
            if champion_list[termid][k] > max_freq-2:
                test_dict[k] = champion_list[termid][k]
        champion_list[termid] = test_dict

    print("champion list:")
    print(champion_list)

    if part == 2:
        print("List of words mapped to these words : دان، ، ساز، کرد، شنو، توان، یاد، دوست، شریف، هنر، سپاس، خواه،رو ،رود ،گو ،گفت ")
        print(stemming_list)

    print("term map to termId:")
    print(term_termid_match)

    # sort by terms
    termid_docid_pairs.sort(key=lambda x: x[0])

    # inverted index construction
    inverted_index = {}
    for pair in termid_docid_pairs:
        if pair[0] in inverted_index.keys():
            inverted_index[pair[0]].append(pair[1])
        else:
            inverted_index[pair[0]] = [pair[1]]
    if part == 1:
        return inverted_index,T_M_dict,news,term_frequency,termid_freq_perdoc,document_freq,doc_id,term_termid_match,champion_list,news_title
    else:
        return inverted_index, T_M_dict, news, term_frequency,stemming_list,termid_freq_perdoc,document_freq,doc_id,term_termid_match,champion_list,news_title

def tf_idf(term_freq_perdoc,doc_freq,docid,query,term_termid,index,news,champion_list,news_title):

    tf_idf_weights = {}
    N = docid
    documents_size = {}
    for docid in term_freq_perdoc:
        d_size = 0
        tf_idf_weights[docid] = {}
        for termid in term_freq_perdoc[docid]:
            tf = term_freq_perdoc[docid][termid]
            df = doc_freq[termid]
            w = 0
            w = (1+math.log10(tf))*(math.log10((N/df)))
            tf_idf_weights[docid][termid] = w
            d_size += (w * w)
        d_size = math.sqrt(d_size)
        documents_size[docid] = d_size

    words = query.split(" ")
    tf_query = {}
    term_termid_keys = list(term_termid.keys())
    tf_query_keys = list(tf_query.keys())
    for word in words:
        if word in term_termid_keys:
            if term_termid[word] in tf_query_keys:
                tf_query[term_termid[word]] += 1
            else:
                tf_query[term_termid[word]] = 1
                tf_query_keys = list(tf_query.keys())

    query_weights = {}
    doc_scores = {}
    query_size = 0
    for termid in tf_query:
        tf = tf_query[termid]
        df = doc_freq[termid]
        w_t_q = 0
        w_t_q = (1 + math.log10(tf)) * (math.log10((N / df)))
        query_weights[termid] = w_t_q
        query_size += (w_t_q * w_t_q)


    for termid in tf_query:
        w_t_q = query_weights[termid]

    #     getting documents that have at least one common word with query from postings list of query words
        postings_list = []

        # step2,with postings list
        # postings_list = index[termid]

        # step 3, with champion list
        postings_list = champion_list[termid]

        for docid in postings_list:
            w_t_d = tf_idf_weights[docid][termid]
            doc_scores_keys = list(doc_scores.keys())
            if docid in doc_scores_keys:
                doc_scores[docid] += (w_t_q * w_t_d)
            else:
                doc_scores[docid] = w_t_q * w_t_d

    for docid in doc_scores:
        doc_scores[docid] = doc_scores[docid]/(documents_size[docid]*query_size)

    # print(doc_scores)

    # select k news with highest cosine similarity with query
    doc_scores_values = list(doc_scores.values())
    doc_scores_keys = list(doc_scores.keys())
    k_top = heapq.nlargest(10,doc_scores_values)

    # print(k_top)
    for k in k_top:
        docid = doc_scores_keys[doc_scores_values.index(k)]
        print("*********")
        print("news number %s"%(docid))
        print(news_title[docid])
        print(news[docid])


    return doc_scores,tf_idf_weights

stemming_list = {}
# first case
part = 1
inverted_index,T_M_dict,news,term_frequency,term_freq_perdoc,document_freq,docid,term_termid, champion_list,news_titles= create_index(part)
print("inverted index:")
print(inverted_index)
print()
# print(term_freq_perdoc[5])
# computing weights of words
query = " "
query = raw_input("enter query: ")
doc_scores,tf_idf_weights = tf_idf(term_freq_perdoc,document_freq,docid,query,term_termid,inverted_index,news,champion_list,news_titles)

# part 4-1
tf_idf_weights_perdoc = {}
tf_idf_weights_perdoc=tf_idf_weights[1]
w_values_list = list(tf_idf_weights_perdoc.values())
w_keys_list = list(tf_idf_weights_perdoc.keys())
term_termid_keys = list(term_termid.keys())
term_termid_values = list(term_termid.values())
# print(term_termid)
print("news number 2:")
print("title: %s"%(news_titles[1]))
print("5 words with maximum weight in news 2")
for w in heapq.nlargest(5,w_values_list):
    out_string = "word: {} , weight: {}"
    print(out_string.format(term_termid_keys[term_termid_values.index(w_keys_list[w_values_list.index(w)])],w))

print()
print("5 words with minimum weight in news 2")
for w in heapq.nsmallest(5,w_values_list):
    out_string = "word: {} , weight: {}"
    print(out_string.format(term_termid_keys[term_termid_values.index(w_keys_list[w_values_list.index(w)])],w))



# # second case
# part = 2
# inverted_index,T_M_dict,news,term_frequency,stemming_list,term_freq_perdoc,document_freq,docid,term_termid, champion_list,news_titles = create_index(part)
# print("inverted index of the second case:")
# print(inverted_index)
# print()
# query = " "
# query = raw_input("enter query: ")
# doc_scores,tf_idf_weights = tf_idf(term_freq_perdoc,document_freq,docid,query,term_termid,inverted_index,news,champion_list,news_titles)
# # part 4-1
# tf_idf_weights_perdoc = {}
# tf_idf_weights_perdoc=tf_idf_weights[1]
# w_values_list = list(tf_idf_weights_perdoc.values())
# w_keys_list = list(tf_idf_weights_perdoc.keys())
# term_termid_keys = list(term_termid.keys())
# term_termid_values = list(term_termid.values())
# # print(term_termid)
# print("news number 2:")
# print("title: %s"%(news_titles[1]))
# print("5 words with maximum weight in news 2")
# for w in heapq.nlargest(5,w_values_list):
#     out_string = "word: {} , weight: {}"
#     print(out_string.format(term_termid_keys[term_termid_values.index(w_keys_list[w_values_list.index(w)])],w))
#
# print()
# print("5 words with minimum weight in news 2")
# for w in heapq.nsmallest(5,w_values_list):
#     out_string = "word: {} , weight: {}"
#     print(out_string.format(term_termid_keys[term_termid_values.index(w_keys_list[w_values_list.index(w)])],w))


