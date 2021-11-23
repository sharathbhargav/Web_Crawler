
import requests


from UtilityFunctions import PreprocessHelpers
from urllib3.exceptions import InsecureRequestWarning
from UtilityFunctions import CommonHelpers
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import Web_page

class Crawler:
    def __init__(self,urls=[]):
        self.urls_to_visit=urls
        self.urls_visited = {}

    def clean_url(self,url):
        if url.endswith('/'):
            url = url[:-1]
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
        if url not in self.urls_visited and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)
        if url in self.urls_visited:
            web_page = self.urls_visited[url]
            web_page.incoming_urls.append(self.clean_url(parent))


    def download(self,url):
        
        k=requests.get(url,verify=False)
        return k.text

    def crawl(self, url):
        html = self.download(url)
        print(f"Length of data in {url} = {len(html)}")
        for out_url in self.get_linked_urls(url, html):
            if "uic.edu" in out_url:
                self.add_url_to_visit(out_url,url)
    
    def run(self,n):
        i=0
        while self.urls_to_visit and i<n:
            url = self.urls_to_visit.pop(0)
            if url:
                print(f'Crawling: {url}')
                try:
                    self.crawl(url)
                except Exception as e :
                    print("exception",e)
                finally:
                    i+=1
        self.dump_data_to_pickle()

    def dump_data_to_pickle(self):
        self.doc_list={}
        for key in self.urls_visited:
            web_page =self.urls_visited[key]
            web_page.run_preprocess()
            self.doc_list[key]=web_page.words
        CommonHelpers.dump_pickle("data/cleaned_word_list.pickle",self.doc_list)
        CommonHelpers.dump_pickle("data/web_pages.pickle",self.urls_visited)

    def init_data_from_pickle(self):
        self.doc_list = CommonHelpers.load_pickle("data/cleaned_word_list.pickle")
        self.urls_visited = CommonHelpers.load_pickle("data/web_pages.pickle")


