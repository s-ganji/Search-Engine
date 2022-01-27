import re
import string
from bs4 import BeautifulSoup
import pandas as pd

import re
import string

import nltk
import pandas as pd
from bs4 import BeautifulSoup
from parsivar import FindStems

import math
import random
import re
import string

import matplotlib



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


    file_names = ["ir-news-0-2.csv", "ir-news-2-4.csv", "ir-news-4-6.csv", "ir-news-6-8.csv", "ir-news-8-10.csv","ir-news-10-12.csv"]
    # file_names = ["ir-news-0-2.csv"]
    for l in range(len(file_names)):
        df = pd.read_csv(r"./doc_collection/" + file_names[l])
        contents = pd.DataFrame(df, columns=['content'])
        for i in range(len(contents)):
            print(i)
            str = contents.loc[i, "content"]
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
                    term_frequency[token] = term_frequency[token] + 1
                    # if we dont had this termid_docid pait exactly in our list we dont append pair in list
                    if pair not in termid_docid_pairs:
                        termid_docid_pairs.append(pair)

                # if we didnt have that term in our dictionary
                else:
                    pair = []
                    term_termid_match[token] = term_id
                    pair.append(term_id)
                    pair.append(doc_id)
                    termid_docid_pairs.append(pair)
                    term_id = term_id + 1
                    term_frequency[token] = 1

                T_M_dict[total_token_number] = len(term_termid_match)

            doc_id = doc_id + 1

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
        return inverted_index,T_M_dict,news,term_frequency
    else:
        return inverted_index, T_M_dict, news, term_frequency,stemming_list


def heaps_law(T_M_dict,news,part,stemming_list):

    sw = []
    sw = making_sw('stopwords-fa.txt')
    random_news = random.choices(news, k=5000)
    T = 0
    M = 0
    distinct_tokens = []
    for str in random_news:
        if part == 1:
            token_list = pre_process_1(str,sw)
        elif part == 2:
            token_list,stemming_list = pre_process_2(str,sw,stemming_list)
        #     stopwords???
        for token in token_list:
            T = T + 1
            if token not in distinct_tokens:
                distinct_tokens.append(token)
                M = M + 1

    random_news2 = random.choices(news, k=15000)
    T2 = 0
    M2 = 0
    distinct_tokens2 = []
    for str in random_news2:
        if part == 1:
            token_list = pre_process_1(str, sw)
        elif part == 2:
            token_list,stemming_list = pre_process_2(str, sw,stemming_list)
        #     stopwords???
        for token in token_list:
            T2 = T2 + 1
            if token not in distinct_tokens2:
                distinct_tokens2.append(token)
                M2 = M2 + 1

    log_T = math.log10(T)
    log_T2 = math.log10(T2)

    log_M = math.log10(M)
    log_M2 = math.log10(M2)
    b = 0
    log_k = 0

    b = (log_M - log_M2) / (log_T - log_T2)
    log_k = log_M - (b * log_T)
    k = 10 ** log_k
    # number of predict distinct terms of doc collection
    values_T = T_M_dict.keys()
    values_T = list(values_T)
    log_T = []
    log_M = []
    pred_log_M = []
    for t in values_T:
        pred_log_M.append(log_k + (b * math.log10(t)))
        log_M.append(math.log10(T_M_dict[t]))
        log_T.append(math.log10(t))

    plt.xlabel("log_T")
    plt.ylabel("log_M")
    plt.xlim([0, 7])
    plt.ylim([0, 7])
    plt.plot(log_T, pred_log_M)
    plt.plot(log_T, log_M)
    if part == 1:
        plt.title("Heaps’ Law for index1")
        plt.savefig('Heaps_law1.png')
    if part == 2:
        plt.title("Heaps’ Law for index2")
        plt.savefig('Heaps_law2.png')
    plt.clf()

def zipf_law(term_frequency):
    values = term_frequency.values()
    values = list(values)
    log_cf = []
    k = max(values)
    log_cf.append(math.log10(k))
    log_k = math.log10(k)
    log_rank = [math.log10(1)]
    number_of_tokens = len(term_frequency)
    for rank in range(1,number_of_tokens):
        log_cf.append(log_k - math.log10(rank+1))
        log_rank.append(math.log10(rank+1))

    cf_real = []
    log_cf_real = []
    cf_real.append(max(values))
    del values[values.index(max(values))]
    while len(values) != 0:
        max_freq= max(values)
        cf_real.append(max_freq)
        del values[values.index(max_freq)]
    for cf in cf_real:
        log_cf_real.append(math.log10(cf))

    plt.xlabel("log_rank")
    plt.ylabel("log_cf")
    plt.xlim([0, 7])
    plt.ylim([0, 7])
    plt.plot(log_rank,log_cf)
    plt.plot(log_rank,log_cf_real)
    if part == 1:
        plt.title("Zipf’s law for index1")
        plt.savefig('Zipf_law1.png')
    if part == 2:
        plt.title("Zipf’s law for index2")
        plt.savefig('Zipf_law2.png')
    plt.clf()
#

stemming_list = {}
# first case
part = 1
inverted_index,T_M_dict,news,term_frequency = create_index(part)
print(inverted_index)
heaps_law(T_M_dict,news,part,stemming_list)
zipf_law(term_frequency)

# second case
part = 2
inverted_index,T_M_dict,news,term_frequency,stemming_list = create_index(part)
print("inverted index of the second case:")
print(inverted_index)
heaps_law(T_M_dict,news,part,stemming_list)
zipf_law(term_frequency)

