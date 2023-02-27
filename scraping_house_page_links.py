from bs4        import BeautifulSoup
import requests
import json


#user agent is specified for preventing some reachment problems to the website.
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

class House_Scraper:
    def __init__(self, url):
        self.url = url
        self.house_links=[]

    def write_house_links_to_json(self):
        data=[{"house_link": link} for link in self.house_links]
        with open('home_urls.json','w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=4 )      


    def discography(self):
        #from page 1 to 2442 were scraped 
        page_number=1
        while page_number <= 2442:
            page=requests.get(self.url + "?pn={}".format(page_number), headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            parse1=soup.find('div', class_='list-content-properties')
            parse2=parse1.find_all('div', class_='property-info-content')
            for i in parse2:
                if i.find('a').get('href') not in self.house_links and i.find('a').get('href').startswith('https:'):
                    self.house_links.append(i.find('a').get('href'))
            
            print("Page {} done".format(page_number))            
            page_number+=1
        self.write_house_links_to_json()

    
    def get_house_links(self):
        with open ('home_urls.json', "r") as f:
            data = json.load(f)
            return data

    def take_features_of_house(self,link_list):
        for i in link_list:
            page=requests.get(i['house_link'], headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            print(soup)

            #TODO: take features of EACH house and write them to a csv file then to a database

            



if __name__ == '__main__':
    scraper = House_Scraper('https://casa.sapo.pt/comprar-apartamentos/')
    #scraper.discography()
    house_links=scraper.get_house_links()
    scraper.take_features_of_house(house_links)


