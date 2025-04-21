from file_proccessor import FileProccessing
from paths import *
from datetime import date
from bs4 import BeautifulSoup as bs
TODAY = date.today()
class Parser(FileProccessing):
    def __init__(self,*args,**kwargs):
        super().__init__()
    def get_soup(self,html):
        soup = bs(html,'html.parser')
        return soup 
    def getting_class(self,input_text_file,target_class) -> None:
        html = self.read_text_file(input_text_file)
        soup = self.get_soup(html)
        return soup.find_all(class_=target_class)
    def parse_data(self,**data):
        return data
    

