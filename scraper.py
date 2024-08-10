import requests
import os
from bs4 import BeautifulSoup


class WebScraper:
    
    def __init__(self,url):
        self.url = url
        self.html_content = None

    
    def fetch(self):
        response = requests.get(self.url)
        print(response.status_code)
        if response.status_code == 404:
            raise Exception("Not found. Check web url. {}".format(response.request.url))

        elif response.status_code == 200:
            self.html_content = response.content
        
        else:
            print("Fail to request. Status code {}".format(response.status_code))


    def get_navigators(self):

        if self.html_content is None:
            self.fetch()

        page_content = self.html_content

        soup = BeautifulSoup(page_content,"html.parser")

        page_links = soup.find_all("a",class_ = ["navigatelink_current","navigatelink"])

        page_numbers = [link.get_text() for link in page_links if link.get_text() != "Sonraki >"]

        numbers = []

        [numbers.append(x) for x in page_numbers if x not in numbers]

        return numbers  ## list
    
    
    def get_filenames(self):

        if self.html_content is None:
            self.fetch()

        page_content = self.html_content

        soup = BeautifulSoup(page_content,"html.parser")

        page_links = soup.find_all("td",class_ = ["td_reports_name"])

        filenames = [link.get_text() for link in page_links]

        return filenames  ## list
