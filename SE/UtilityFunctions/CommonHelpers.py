import pickle
import bz2
import _pickle as cPickle
from SE.Web_page import Web_page
def print_dict(dic):
    for key in dic:
        print(str(key)+"=>"+str(dic[key]))

def str_dict1(dic):
    ret = ""
    for key in dic:
        ret = ret+ str(key)+"=>"+str(dic[key])+","
    return ret

def dump_pickle(file_name, data):
    with bz2.BZ2File(file_name, "wb") as f: 
        cPickle.dump(data, f)

def load_pickle(file):
    data = bz2.BZ2File(file, "rb")
    data = cPickle.load(data)
    return data

def clean_url(url):
    if url.endswith('/'):
        url = url[:-1]
    if url.startswith("https"):
        url="http"+url[5:]
    return url