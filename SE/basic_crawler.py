
import requests
import pathlib, os
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
import threading
from multiprocessing import  RawValue, Lock
import multiprocessing
from urllib3.exceptions import InsecureRequestWarning
from SE.UtilityFunctions import CommonHelpers
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from . import Web_page
import time
class Crawler:
    def __init__(self,urls=[]):
        
        self.urls_to_visit=Queue()
        for each in urls:
            self.urls_to_visit.put(each)
        self.urls_visited = {}
        self.temp=[]
        self.val = RawValue('i', 0)
        self.lock = Lock()
        

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

    def clean_url(self,url):
        if url.endswith('/'):
            url = url[:-1]
        if url.startswith("https"):
            url="http"+url[5:]
        return url

    def get_linked_urls(self,url,data):
        # print("get linked urls")
        web_page = Web_page.Web_page(url,data)
        self.urls_visited[self.clean_url(url)]=web_page
        urls = web_page.get_URLs_from_page()
        return urls

    def add_url_to_visit(self,url,parent):
        # print("in add_url_to_visit")
            
        url = self.clean_url(url)
        if url not in self.urls_visited and url not in self.temp:
            self.urls_to_visit.put(url)
            self.temp.append(url)
        if url in self.urls_visited:
            web_page = self.urls_visited[url]
            web_page.incoming_urls.append(self.clean_url(parent))


    def download(self,url):
        
        k=requests.get(url,verify=False)
        return k.text

    def crawl(self):
        url = self.urls_to_visit.get(timeout=60)
        url=self.clean_url(url)
        html = self.download(url)
        print(f"Length of data in thread {threading.current_thread().name} in {url[-10:]} = {len(html)}")
        for out_url in self.get_linked_urls(url, html):
            if "uic.edu" in out_url:
                self.add_url_to_visit(out_url,url)
        self.increment()
        self.i=self.i+1
        
        return True
    
    def post_scrape_callback(self, res):
        print(len(self.urls_visited))
        if(len(self.urls_visited)>10):
            with self.urls_to_visit.mutex:
                self.urls_to_visit.queue.clear()
        if res:
            pass
            # self.parse_links(result.text)
            # self.scrape_info(result.text)

    def runEachThread(self):
        while True and len(self.urls_visited)<self.n:
            try:
                time.sleep(0.5)
                self.crawl()
                self.i = self.i +1
                if self.i%200==0:
                    print(self.i,len(self.urls_visited))
            except Empty:
                break
            except Exception as e :
                print("exception",e)
                
            


    def run(self,n):
        self.i=0
        self.n=n
        # print("Init q size =",self.urls_to_visit.qsize())
        
        workers = []
        for i in range(5):
            worker = threading.Thread(target=self.runEachThread)
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
        print("end of while",len(self.urls_visited))
    
        self.dump_data_to_pickle()

    def dump_data_to_pickle(self):
        self.doc_list={}
        for key in self.urls_visited:
            web_page =self.urls_visited[key]
            web_page.run_preprocess()
            self.doc_list[key]=web_page.words
        print(pathlib.Path(__file__).parent.resolve())
        CommonHelpers.dump_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/cleaned_word_list.pickle"),self.doc_list)
        CommonHelpers.dump_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(), "data/web_pages.pickle"),self.urls_visited)

    def init_data_from_pickle(self):
        print(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/web_pages.pickle"))

        self.doc_list = CommonHelpers.load_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/cleaned_word_list.pickle"))
        self.urls_visited = CommonHelpers.load_pickle(os.path.join(pathlib.Path(__file__).parent.resolve(),"data/web_pages.pickle"))


