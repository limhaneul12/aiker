import re
import json
import os.path
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from lxml import etree
from gensim.utils import to_unicode
from functools import reduce
from keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Mecab
#from numba import jit

## == LIST PRINT ========
MAX_PRINT = 2000

def show_list(preprint, lst, max_print=MAX_PRINT):
    print(preprint)

    for index, value in enumerate(lst):
        print(index, ": ", value[:max_print], "\n")
    print("")

## == Tokenize ========
WIKI_REMOVE_CHARS1 = re.compile("'+|(=+.{2,30}=+)|__TOC__|(ファイル:).+|:(en|de|it|fr|es|kr|zh|no|fi):|\n|(&lt;)[\s\S]+?(&gt;)|(&quot;)|<.*?>|&nbsp;|분류:.*]", re.UNICODE)
#WIKI_REMOVE_CHARS2 = re.compile("파일:.*g|style=.*;|.* = .*g|cellspacing=.*[\"]|colspan=\w|valign=\w+|font-size.*%;|text-align:\w+|----|-|{{.*}}:|{|id=.*;|!width=\w+%|[\|]\w+px", re.UNICODE)
WIKI_REMOVE_CHARS2 = re.compile("\[\[|\]\]", re.UNICODE)
WIKI_SPACE_CHARS = re.compile("(\\s|゙|゚|　)+", re.UNICODE)
EMAIL_PATTERN = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.UNICODE)
URL_PATTERN = re.compile("(ftp|http|https)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.UNICODE)
WIKI_REMOVE_TOKEN_CHARS = re.compile("(\\*$|:$|^파일:.+|^;|{{|}}|\[\[|\]\]|\|)", re.UNICODE)
MULTIPLE_SPACES = re.compile(' +', re.UNICODE)

def tokenizer(content, token_min_len=2, token_max_len=100, lower=True, tokenize=False):
    content = re.sub(EMAIL_PATTERN,      ' ', content)  # remove email pattern
    content = re.sub(URL_PATTERN,        ' ', content)  # remove url pattern
    content = re.sub(WIKI_REMOVE_CHARS1, ' ', content)  # remove unnecessary chars
    content = re.sub(WIKI_REMOVE_CHARS2, ' ', content)  # remove unnecessary chars
    content = re.sub(WIKI_SPACE_CHARS,   ' ', content)
    content = re.sub(MULTIPLE_SPACES,    ' ', content)

    if tokenize:
        print("tokenizer - tokenize")
        tokens = content.replace(", )", "").split(" ")
        result = []
        for token in tokens:
            print("tokenizer - tokens ", token)
            if not token.startswith('_'):
                token_candidate = to_unicode(re.sub(WIKI_REMOVE_TOKEN_CHARS, '', token))
            else:
                token_candidate = ""
            if len(token_candidate) > 0:
                result.append(token_candidate)
        return result
    else:
        return content

mecab = Mecab()
## == Parsing =========
def node_clear(elem):
    # It's safe to call clear() here because no descendants will be accessed
    elem.clear()

    # Also eliminate now-empty references from the root node to <title>
    while (elem.getprevious() is not None) and (elem.getparent() is not None):
        del elem.getparent()[0]

## -- Node Check -----
ABSTRACT_MODE = "abstract"
ARTICLES_MODE = "articles"
ABSTRACT_TAG  = ['doc', 'title', 'abstract']
ARTICLES_TAG  = ['page','title', 'text'    ]
ARTICLES_NAME_SPACE = "{http://www.mediawiki.org/xml/export-0.10/}"

ARTICLES_TAG = list(map(lambda tag: ARTICLES_NAME_SPACE + tag, ARTICLES_TAG))

def check_page(tag, mode):
    if mode == ABSTRACT_MODE:
        return tag == ABSTRACT_TAG[0]
    if mode == ARTICLES_MODE:
        return tag == ARTICLES_TAG[0]

def check_available(event, tag, mode):
    return event == 'start' and check_page(tag, mode)

def check_title(tag, mode):
    if mode == ABSTRACT_MODE:
        return tag == ABSTRACT_TAG[1]
    if mode == ARTICLES_MODE:
        return tag == ARTICLES_TAG[1]

def check_content(tag, mode):
    if mode == ABSTRACT_MODE:
        return tag == ABSTRACT_TAG[2]
    if mode == ARTICLES_MODE:
        return tag == ARTICLES_TAG[2]

## -- Get Content -----
def get_title(title, mode):
    if mode == ABSTRACT_MODE:
        return title[6:]
    if mode == ARTICLES_MODE:
        return title

def get_value(text, tag, mode, tokenize=False):
    if text == None:
        return None
    if tag == ABSTRACT_TAG[1] or tag == ARTICLES_TAG[1]:
        return tokenizer(get_title(text, mode))
    else:
        return tokenizer(text, tokenize=tokenize)

## -- Make List -----
SEPERATE = ["title", "content"]

def check_pop(event, tag, mode):
    return event == 'start' and tag == check_content(tag, mode)

def get_doc_list(doc_list, value, seperate, debugging=False, max_print=30):
    doc_list[-1] = doc_list[-1] + value

    if debugging:
        print(seperate + ": ", doc_list[-1][:max_print])
        # show_list(seperate + " list: ", doc_list, max_print)

    return doc_list

def parse(context, mode, debugging=False, max_print=30, tokenize=False):
    title   = []
    content = []
    find = False

    print("===========", mode)

    for event, elem in context:
        if debugging:
            print("%s: %s" % (event, elem.tag))

        if check_available(event, elem.tag, mode):
            find = True
            title.append("")
            if tokenize:
                content.append([])
            else:
                content.append("")
            # node_clear(elem)
            continue
        if not find:
            # node_clear(elem)
            continue

        value = get_value(elem.text, elem.tag, mode, tokenize=tokenize)
        if value == None:
            if check_pop(event, elem.tag, mode):
                title.pop()
                find = False
            # node_clear(elem)
            continue

        if check_title(  elem.tag, mode):
            title   = get_doc_list(title,   value, SEPERATE[0],
                                   debugging, max_print)
        if check_content(elem.tag, mode):
            content = get_doc_list(content, value, SEPERATE[1],
                                   debugging, max_print)

        node_clear(elem)

    if debugging:
        print("\n")
    return (title, content)

## == Match ===========
#@jit
def match_index(ab_title, ar_title):
    print("=========== Match Index")
    ab_dic = { title:index for index,title in enumerate(ab_title) }
    matched = list(map(ab_dic.get, ar_title))

    print("=========== Index Filter")
    ab_index = list(filter(lambda i: i is not None,
                           matched))
    ar_index = list(filter(lambda i: matched[i] is not None,
                           range(len(matched))))
    return (ab_index, ar_index)

#@jit
def match_content(index_list, content_list, mode):
    print("=========== Match " + mode)
    return list(map(lambda i: content_list[i], index_list))

## == Encoding ===========
def content_tokenizer(content_list):
    print("content_tokenizer")
    return (mecab.morphs(string) for string in content_list)

    # return list(map(mecab_morphs, # tokenizer(string, tokenize=True)
    #                 content_list))

def update_dic(word_index, value_list):
    for string in value_list:
        if not word_index.get(string):
            word_index.update({string: len(word_index)+1})
    return word_index

def make_dic(word_index, content_list):
    print("make_dic")
    for value_list in content_list:
        word_index = update_dic(word_index, value_list)
    return word_index

# def word_indexer(ab_title, ab_content, ar_title, ar_content):
#     print("=========== Word Index")
#     print("==> Abstact Title Index")
#     word_index = make_dic({}, content_tokenizer(ab_title))
#     print("====> Articles Title Index")
#     word_index = make_dic(word_index, content_tokenizer(ar_title  ))
#     print("======> Abstact Content Index")
#     word_index = make_dic(word_index, content_tokenizer(ab_content))
#     print("========> Articles Content Index")
#     word_index = make_dic(word_index, content_tokenizer(ar_content))
#     return word_index

def word_indexer(title_list, ab_list, ar_list):
    print("=========== Word Index")
    print("==> Title Index")
    word_index = make_dic({}, content_tokenizer(title_list))
    print("======> Abstact Index")
    word_index = make_dic(word_index, content_tokenizer(ab_list))
    print("========> Articles Index")
    word_index = make_dic(word_index, content_tokenizer(ar_list))
    return word_index

def get_index(word_index, string):
    if string in word_index:
        return word_index.get(string)
    else:
        return 0

def value_sequence(word_index, value_list):
    #return (get_index(word_index, string) for string in value_list)
    return list(map(lambda string:
                      get_index(word_index, string), value_list))

def make_sequence(word_index, content_list):
    print("make_sequence")
    # return (value_sequence(word_index, value_list) for value_list in content_list)
    return list(map(lambda value_list: value_sequence(word_index, value_list),
                     content_list))

def max_word_length(lst):
    return reduce(lambda num1, num2: num1 if num1 > num2 else num2,
                  map(lambda string: len(string), lst))

def make_sequences(word_index, title_list, ab_list, ar_list, debugging=False):
    print("=========== Make Sequence")
    print("==> Title Sequence")
    title_sequence = make_sequence(word_index, content_tokenizer(title_list))
    del(title_list)
    print("======> Abstact Sequence")
    ab_sequence    = make_sequence(word_index, content_tokenizer(ab_list   ))
    del(ab_list)
    print("========> Articles Sequence")
    ar_sequence    = make_sequence(word_index, content_tokenizer(ar_list   ))
    del(ar_list)

    if debugging:
        print("Title Sequence: ", title_sequence, "\n")
        print("Abstract Sequence: ", ab_sequence, "\n")
        print("Articles Sequence: ", ar_sequence, "\n")
    return (title_sequence, ab_sequence, ar_sequence)

TITLE_MAX = 10
AB_MAX    = 100
AR_MAX    = 10000
def max_length(title_sequence, ab_sequence, ar_sequence):
    title_max = max_word_length(title_sequence)
    ab_max    = max_word_length(ab_sequence)
    ar_max    = max_word_length(ar_sequence)

    print("========== Max Length")
    print("length: {0}, {1}, {2}".format(title_max, ab_max, ar_max))

    return (title_max, ab_max, ar_max)

#@jit(forceobj=True)
def list_merge(lst1, lst2):
    return np.concatenate([lst1, lst2])

#@jit(forceobj=True)
def list_divide(sequence, size):
    return (sequence[i * size:(i + 1) * size]
                         for i in range((len(sequence) + size -1) // size))

def make_pad_sequence(sequence, max_length):
    size = 1000
    return list(reduce(
        list_merge, map(lambda seq_snippet:
                        pad_sequences(seq_snippet, maxlen=max_length, padding='post'),
                        list_divide(sequence, size))))

def make_pad_sequences(title_sequence, ab_sequence, ar_sequence, debugging=False):
    print("=========== Make Pad Sequence")
    if debugging:
        title_max, ab_max, ar_max = max_length(title_sequence, ab_sequence, ar_sequence)
    else:
        title_max, ab_max, ar_max = (TITLE_MAX, AB_MAX, AR_MAX)

    print("==> Title Padding")
    title_pad = make_pad_sequence(title_sequence, title_max)
    print("======> Abstact Padding")
    ab_pad    = make_pad_sequence(ab_sequence,    ab_max   )
    print("========> Articles Padding")
    ar_pad    = make_pad_sequence(ar_sequence,    ar_max   )
    return (title_pad, ab_pad, ar_pad)


## == Parqeut =========
COLUMNS = ['title', 'abstract', 'text']
def create_parquet_table(title_list, ab_list, ar_list):
    df = pd.DataFrame({COLUMNS[0]: list(title_list),
                       COLUMNS[1]: list(ab_list),
                       COLUMNS[2]: list(ar_list)    })
    return pa.Table.from_pandas(df)

RCOLUMNS = ['title', 'content']
def create_parquet_content_table(title_list, content_list):
    df = pd.DataFrame({RCOLUMNS[0]: list(title_list),
                       RCOLUMNS[1]: list(content_list)})
    return pa.Table.from_pandas(df)

def write_parquet(table, path="wiki.parquet", compression="snappy"):
    pq.write_table(table, path, compression=compression)

def read_parquet(path, columns=COLUMNS):
    return pq.read_table(path, columns)

def load_parqet_parsed(path, columns=RCOLUMNS):
    df = read_parquet(path, columns).to_pandas()
    return (df.values[:, 0], df.values[:, 1])

def load_parqet_content(path, columns=COLUMNS):
    df = read_parquet(path, columns).to_pandas()
    return (df.values[:, 0], df.values[:, 1], df.values[:, 2])

def info_parquet(path):
    parquet_file = pq.ParquetFile(path)
    print(parquet_file.metadata)
    print(parquet_file.schema  )
    print("\n")

def show_table(table, row=5):
    df = table.to_pandas()

    if row == "all":
        print(df)
    else:
        print(df.head(row))

    print("\n")

## == Main ============
AB_FILE    = "./data/kowiki-latest-abstract.xml"
AR_FILE    = "./data/kowiki-latest-pages-articles.xml"
OUT_FILE   = "./data/wiki.parquet"
RAW_FILE   = "./data/wiki_raw.parquet"
RAB_FILE   = "./data/wiki_raw_abstract.parquet"
RAR_FILE   = "./data/wiki_raw_articles.parquet"
SEQ_FILE   = "./data/wiki_seq.parquet"
VOCA_FILE  = "./data/wiki_vocab.json"

SAB_FILE   = "./data/abstract_sample.xml"
SAR_FILE   = "./data/article_sample.xml"
SOUT_FILE  = "./data/wiki_sample.parquet"
SRAW_FILE  = "./data/wiki_raw_sample.parquet"
SRAB_FILE  = "./data/wiki_raw_abstract_sample.parquet"
SRAR_FILE  = "./data/wiki_raw_articles_sample.parquet"
SSEQ_FILE  = "./data/wiki_seq_samaple.parquet"
SVOCA_FILE = "./data/wiki_vocab_sample.json"

DEBUGGING  = False # True False | Print for debugging
SAMPLE     = False # True False | Use sample file mode
if SAMPLE:
    AB_FILE   = SAB_FILE
    AR_FILE   = SAR_FILE
    OUT_FILE  = SOUT_FILE
    RAW_FILE  = SRAW_FILE
    RAB_FILE  = SRAB_FILE
    RAR_FILE  = SRAR_FILE
    SEQ_FILE  = SSEQ_FILE
    VOCA_FILE = SVOCA_FILE

def write_vocab(word_index, path=VOCA_FILE):
    json.dump(word_index, open(path, 'w'))

def read_vocab(path=VOCA_FILE):
    return json.load(open(path))

def preprocessing_parsing(ab_file, ar_file, debugging, max_print):
    if os.path.isfile(RAB_FILE) and os.path.isfile(RAR_FILE):
        print("====== Load RAW Parsed Data Start =====")
        ab_title, ab_content = load_parqet_parsed(RAB_FILE)
        ar_title, ar_content = load_parqet_parsed(RAR_FILE)
        print("====== Load RAW Parsed Data Start =====")
    else:
        print("====== Create Parse Data Start =====")
        print("====== Parsing Start =====")
        abstract = etree.iterparse(ab_file, events=('start', 'end', ),
                                   tag=ABSTRACT_TAG, huge_tree=True)
        articles = etree.iterparse(ar_file, events=('start', 'end', ),
                                   tag=ARTICLES_TAG, huge_tree=True)

        ab_title, ab_content = parse(abstract, ABSTRACT_MODE, debugging, max_print)
        ar_title, ar_content = parse(articles, ARTICLES_MODE, debugging, max_print)

        print("====== Parsing End =====")
        print("size: {0}, {1}, {2}, {3}".format(len(ab_title), len(ab_content),
                                                len(ar_title), len(ar_content)))
        print("====== Save RAW Data Start =====")
        write_parquet(create_parquet_content_table(ab_title, ab_content),
                      RAB_FILE)
        write_parquet(create_parquet_content_table(ar_title, ar_content),
                      RAR_FILE)
        print("====== Save RAW Data End =====")
        print("====== Create Parse Data End =====")

    if debugging:
        print("abstract title: ", ab_title)
        show_list("abstract content: ", ab_content, max_print)
        print("articles title: ", ar_title)
        show_list("article content:",   ar_content, max_print)
    print("\n")

    return (ab_title, ab_content, ar_title, ar_content)

def preprocessing_matching(ab_title, ab_content, ar_title, ar_content,
                           debugging, max_print):
    print("====== Matching Start =====")
    ab_index, ar_index = match_index(ab_title, ar_title)
    title_list = match_content(ab_index, ab_title,   "Title"      )
    ab_list    = match_content(ab_index, ab_content, ABSTRACT_MODE)
    ar_list    = match_content(ar_index, ar_content, ARTICLES_MODE)

    print("====== Matching End =====")
    print("index size: {0}, {1}".format(len(ab_index), len(ar_index)))
    print("content size: {0}, {1}, {2}".format(len(title_list),
                                               len(ab_list), len(ar_list)))
    if debugging:
        print("matched title: ", title_list)
        show_list("matched abstact: ", ab_list, max_print)
        show_list("matched article: ", ar_list, max_print)
    print("\n")
    return (title_list, ab_list, ar_list)

def preprocessing_raw(ab_file, ar_file, debugging, max_print):
    if os.path.isfile(RAW_FILE):
        print("====== Load RAW Data Start =====")
        title_list, \
            ab_list, ar_list = load_parqet_content(RAW_FILE)
        print("====== Load Raw Data End =====")
        print("\n")
    else:
        print("====== Create RAW Data Start =====")
        ab_title, ab_content, \
            ar_title, ar_content = preprocessing_parsing(ab_file, ar_file,
                                                         debugging, max_print)
        title_list, \
            ab_list, ar_list = preprocessing_matching(ab_title, ab_content,
                                                      ar_title, ar_content,
                                                      debugging, max_print)
        print("====== Create RAW Data End =====")
        del(ab_title, ab_content, ar_title, ar_content)
        print("====== Save RAW Data Start =====")
        write_parquet(create_parquet_table(title_list, ab_list, ar_list),
                      RAW_FILE)
        print("====== Save RAW Data End =====")
        print("\n")

    return (title_list, ab_list, ar_list)

def preprocessing_vocab(ab_file, ar_file, debugging, max_print):
    if os.path.isfile(VOCA_FILE):
        print("====== Load Vocab Data Start =====")
        word_index = read_vocab(VOCA_FILE)
        print("====== Load Vocab Data End =====")
    else:
        print("====== Create Vocab Data Start =====")
        title_list, \
            ab_list, ar_list = preprocessing_raw(ab_file, ar_file,
                                                 debugging, max_print)
        # word_index = word_ind(ab_title, ab_content,
        #                           ar_title, ar_content)
        # del(ab_title, ab_content, ar_title, ar_content)
        word_index = word_indexer(title_list, ab_list, ar_list)
        print("====== Create Vocab Data End =====")
        print("word index size: ", len(word_index))
        del(title_list, ab_list, ar_list)
        print("====== Save Vocab Data Start =====")
        write_vocab(word_index, VOCA_FILE)
        print("====== Save Vocab Data End =====")

    if debugging:
        print("word index: ", word_index)
    print("\n")
    return word_index

def preprocessing_sequence(ab_file, ar_file, debugging, max_print):
    if os.path.isfile(SEQ_FILE):
        print("====== Load Sequence Data Start =====")
        title_sequence, \
            ab_sequence, ar_sequence= load_parqet_content(SEQ_FILE)
        print("====== Load Sequence Data End =====")
    else:
        print("====== Create Sequence Data Start =====")
        word_index = preprocessing_vocab(ab_file, ar_file, debugging, max_print)

        title_list, \
            ab_list, ar_list = preprocessing_raw(ab_file, ar_file,
                                                     debugging, max_print)
        title_sequence, \
            ab_sequence, ar_sequence= make_sequences(word_index,
                                                     title_list, ab_list, ar_list)
        print("====== Create Sequence Data End =====")
        print(title_sequence)
        del(word_index, title_list, ab_list, ar_list)
        print("====== Save Sequence Data Start =====")
        write_parquet(create_parquet_table(title_sequence, ab_sequence, ar_sequence),
                      SEQ_FILE)
        print("====== Save Sequence Data End =====")
    return (title_sequence, ab_sequence, ar_sequence)

def preprocessing_wiki(ab_file=AB_FILE, ar_file=AR_FILE,
                       debugging=DEBUGGING, max_print=MAX_PRINT):
    if os.path.isfile(OUT_FILE):
        print("====== Load Encoding Data Start =====")
        title_pad, \
            ab_pad, ar_pad = load_parqet_content(OUT_FILE)
        print("====== Load Encoding Data End =====")
    else:
        print("====== Create Encoding Data Start =====")
        title_sequence, \
            ab_sequence, ar_sequence= preprocessing_sequence(ab_file, ar_file,
                                                             debugging, max_print)
        title_pad, \
            ab_pad, ar_pad = make_pad_sequences(title_sequence,
                                               ab_sequence, ar_sequence, debugging)
        print("====== Create Encoding Data End =====")
        print("content size: {0}, {1}, {2}".format(len(title_pad),
                                                   len(ab_pad), len(ar_pad)))
        del(title_sequence, ab_sequence, ar_sequence)
        print("====== Save Encoding Data Start =====")
        write_parquet(create_parquet_table(title_pad, ab_pad, ar_pad),
                      OUT_FILE)
        print("====== Save Encoding Data End =====")
    if debugging:
        print("padded title: ",    title_pad)
        print("padded abstract: ", ab_pad   )
        print("padded articles: ", ar_pad   )
        print("\n")
    return (title_pad, ab_pad, ar_pad)


if __name__== '__main__':
    preprocessing_wiki(AB_FILE,  AR_FILE)

    print("")

    if DEBUGGING:
        print("Vocab File")
        print(read_vocab(VOCA_FILE))
        print("\n")
        info_parquet(OUT_FILE)
        show_table(read_parquet(OUT_FILE), "all")
    else:
        info_parquet(OUT_FILE)
        show_table(read_parquet(OUT_FILE))

