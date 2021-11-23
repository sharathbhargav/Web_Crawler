from UtilityFunctions import PreprocessHelpers
from bs4 import BeautifulSoup
from urllib.parse import urljoin
class Web_page:
    def __init__(self,url,html_data):
        self.url =url
        self.data=html_data
        self.out_going_urls=[]
        self.incoming_urls = []
    
    def run_preprocess(self):
        preprocessor = PreprocessHelpers.Preprocessor()
        self.cleaned_data = BeautifulSoup(self.data).get_text()
        preprocessor.set_text(self.cleaned_data)
        self.words = preprocessor.run_lemma_pipeline()
    
    def get_URLs_from_page(self):
        soup = BeautifulSoup(self.data, 'html.parser')
        for link in soup.find_all('a'):
            path = str(link.get('href'))
            if path and path.startswith("/"):
                path = urljoin(self.url,path)
            self.out_going_urls.append(path)
            yield path

    def get_out_going_urls(self):
        return self.out_going_urls

    def get_in_urls(self):
        return self.incoming_urls