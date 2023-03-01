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
        with open('deneme.json','w',encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=4 )      


    def discography(self):

        #from page 1 to page 1000, all the house links are collected and stored in total 23414 links.
        page_number=1
        while page_number <= 1:
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
            return data

    def get_house_details(self):
        self.house_links=self.get_house_links()
        for i in self.house_links:
            i=i['house_link']
            page=requests.get(i, headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            price=int(soup.find("p", class_="fontRB fz24 price").text.replace("TL","").replace(" ","").replace("\n","").replace(".",""))
            all_details=soup.find("div", class_="spec-groups")
            all_details_table=all_details.find_all("ul", class_="adv-info-list")
            il_ilce_mah=soup.find("ul", class_="short-info-list")
            il_ilce_mah=il_ilce_mah.find_all("li")
            il=il_ilce_mah[0].text.replace("\n","").replace(" ","")
            ilce=il_ilce_mah[1].text.replace("\n","").replace(" ","")
            mahalle=il_ilce_mah[2].text.replace("\n","").replace(" ","")

            
            
            """new version:
                def get_house_details(self):
        self.house_links=self.get_house_links()
        for i in self.house_links:
            i=i['house_link']
            page=requests.get(i, headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            il_ilce_mah=soup.find("ul", class_="short-info-list")
            il_ilce_mah=il_ilce_mah.find_all("li")
            il=il_ilce_mah[0].text.replace("\n","").replace(" ","")
            ilce=il_ilce_mah[1].text.replace("\n","").replace(" ","")
            mahalle=il_ilce_mah[2].text.replace("\n","").replace(" ","")
            price=(soup.find("p", class_="fontRB fz24 price"))
            if price is not None:  #it is not sold
                price=int(soup.find("p", class_="fontRB fz24 price").text.replace("TL","").replace(" ","").replace("\n","").replace(".",""))
            else: #it is sold
                price=0
            print(il, ilce, mahalle, price)
            #all_details=soup.find("div", class_="spec-groups")
           # all_details_table=all_details.find_all("ul", class_="adv-info-list")
           
           """
            #TODO: LENGTH OF THE LIST IS NOT ALWAYS 10. IT SHOULD BE CHECKED. THAT CAUSES SOME PROBLEMS IN THE HOUSE DETAILS.

            #for left side details
            left_details=all_details_table[0].find_all("li", class_="spec-item")
            if len(left_details) < 10:
                continue
            ilan_no=left_details[0].text.replace("İlan no ","")
            room=left_details[4].text.replace("Oda + Salon Sayısı ","").replace("+ ","").split(" ")[0]
            salon=left_details[4].text.replace("Oda + Salon Sayısı ","").replace("+ ","").split(" ")[1]
            brut_m2=int(left_details[5].text.replace(" ", "").replace("\n","").replace("Brüt/NetM2","").split("/")[0].replace("m2", ""))
            net_m2=int(left_details[5].text.replace(" ", "").replace("\n","").replace("Brüt/NetM2","").split("/")[1].replace("m2", ""))
            floor_location=left_details[6].text.replace("Bulunduğu Kat ","").replace("Kat", "").replace(".","")
            building_age=int(left_details[7].text.replace("Bina Yaşı ","").replace("Yaşında", "").replace("Bina","").replace("Sıfır ","0"))
            
            print(ilan_no, room, salon, brut_m2, net_m2, floor_location, building_age)

            #for right side details
            right_details=all_details_table[1].find_all("li", class_="spec-item")
            bathroom_amount=right_details[1].text.replace("Banyo Sayısı ","")
            print(bathroom_amount)
scraper = House_Scraper('https://www.hepsiemlak.com/en/satilik/daire')
scraper.discography()
#scraper.get_house_links()
scraper.get_house_details()
