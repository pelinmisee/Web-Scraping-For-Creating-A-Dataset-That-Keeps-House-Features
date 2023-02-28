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
        with open('homepage_links.json','w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=4 )      


    def discography(self):

        #from page 1 to page 1000, all the house links are collected and stored in total 23414 links.
        page_number=1
        while page_number <= 1000:
            page=requests.get(self.url + "?page={}".format(page_number), headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            parse1=soup.find("div", class_="listView")
            parse2=parse1.find("ul", class_="list-items-container")
            parse3=parse2.find_all("li", class_="listing-item")
            for i in parse3:
                if i.find("a", class_="card-link")['href'] not in self.house_links:
                    self.house_links.append("https://www.hepsiemlak.com/"+i.find("a", class_="card-link")['href'])

            print("Page {} done".format(page_number))            
            page_number+=1
        
        self.write_house_links_to_json()

    
    def get_house_links(self):
        with open ('all.json', 'r', encoding='utf-8') as f:
            data=json.load(f)
            print(len(data))

    
scraper = House_Scraper('https://www.hepsiemlak.com/en/satilik/daire')
#scraper.discography()
scraper.get_house_links()