from bs4        import BeautifulSoup
import requests
import json
import csv

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


    def add_header(self):
        with open('house_info.csv', 'w', encoding='utf-8') as f:
            #add header
            writer = csv.writer(f)
            writer.writerow(["ilan_no","room","salon","brut_m2","net_m2","floor_location","building_age","building_floor","compliance_with_loan","bathroom_amount","building_type","fuel_type","price","il","ilce","mahalle","home_link"])


    def write_house_info_to_csv(self,ilan_no,room,salon,brut_m2,net_m2,floor_location,building_age,building_floor,compliance_with_loan,bathroom_amount,building_type,fuel_type,price,home_link,il,ilce,mahalle):
       
        
        with open('house_info.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([ilan_no,room,salon,brut_m2,net_m2,floor_location,building_age,building_floor,compliance_with_loan,bathroom_amount,building_type,fuel_type,price,home_link,il,ilce,mahalle])

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
        with open ('deneme.json', 'r', encoding='utf-8') as f:
            data=json.load(f)
            return data

    def get_house_details(self):
        self.house_links=self.get_house_links()
        self.add_header()
        ilan_no=0
        room=0
        salon=0
        brut_m2=0
        net_m2=0
        floor_location=0
        building_age=0
        building_floor=0
        compliance_with_loan=False
        bathroom_amount=0
        building_type=""
        fuel_type=""
        for i in self.house_links:
            i=i['house_link']
            page=requests.get(i, headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            price=(soup.find("p", class_="fontRB fz24 price"))
            home_link=i
            if price is not None:  #it is not sold
                print(i)
                #bottom details part
                il_ilce_mah=soup.find("ul", class_="short-info-list")
                il_ilce_mah=il_ilce_mah.find_all("li")
                il=il_ilce_mah[0].text.replace("\n","").replace(" ","")
                ilce=il_ilce_mah[1].text.replace("\n","").replace(" ","")
                mahalle=il_ilce_mah[2].text.replace("\n","").replace(" ","")

                price=int(soup.find("p", class_="fontRB fz24 price").text.replace("TL","").replace(" ","").replace("\n","").replace(".","").replace("GBP",""))
                all_details=soup.find("div", class_="spec-groups")
                all_details_table=all_details.find_all("ul", class_="adv-info-list")
                
                #left details part
                left_details=all_details_table[0].find_all("li", class_="spec-item")
                for i in range(len(left_details)):
                    if left_details[i].text.startswith("İlan no"):
                        ilan_no=left_details[i].text.replace("İlan no ","")
                    elif left_details[i].text.startswith("Oda + Salon Sayısı"):
                        room_and_salon=left_details[i].text.replace("Oda + Salon Sayısı ","")
                        room=int(room_and_salon.split("+")[0])
                        salon=int(room_and_salon.split(" + ")[1])
                    elif left_details[i].text.startswith("Brüt / Net M2"):
                        m2=left_details[i].text.replace("Brüt / Net M2 ","").replace(" ","").replace("\n","")
                        brut_m2=int(m2.split("/")[0].replace("m2","").replace(".",""))
                        net_m2=int(m2.split("/")[1].replace("m2","").replace(".",""))
                    elif left_details[i].text.startswith("Bulunduğu Kat"):
                        floor_location=left_details[i].text.replace("Bulunduğu Kat ","").replace(". Kat", "")
                    elif left_details[i].text.startswith("Bina Yaşı"):
                        building_age=left_details[i].text.replace("Bina Yaşı ","").replace("Yaşında","").replace("\n","")
                        if building_age.startswith("Sıfır"):
                            building_age=0
                        else:
                            building_age=int(building_age)
                    elif left_details[i].text.startswith("Kat Sayısı"):
                        building_floor=int(left_details[i].text.replace("Kat Sayısı ","").replace("Katlı",""))
                    
                    elif left_details[i].text.startswith("Kredi"):
                        compliance_with_loan=left_details[i].text.replace("Krediye Uygunluk ","")
                        if compliance_with_loan.startswith("Uygun"):
                            compliance_with_loan=True

                    else:
                        continue

                #right details part
                right_details=all_details_table[1].find_all("li", class_="spec-item")
                for i in range(len(right_details)):
                    if right_details[i].text.startswith("Kat Sayısı"):
                        building_floor=int(right_details[i].text.replace("Kat Sayısı ","").replace("Katlı",""))
                        print(building_floor)
                    elif right_details[i].text.startswith("Kredi"):
                        compliance_with_loan=right_details[i].text.replace("Krediye Uygunluk ","")
                        if compliance_with_loan.startswith("Uygun"):
                            compliance_with_loan=True
                    elif right_details[i].text.startswith("Banyo"):
                        bathroom_amount=int(right_details[i].text.replace("Banyo Sayısı ",""))
                    elif right_details[i].text.startswith("Yapı Tipi"):
                        building_type=right_details[i].text.replace("Yapı Tipi ","")
                    elif right_details[i].text.startswith("Yakıt Tipi"):
                        fuel_type=right_details[i].text.replace("Yakıt Tipi ","")
                    
            self.write_house_info_to_csv(ilan_no,room,salon,brut_m2,net_m2,floor_location,building_age,building_floor,compliance_with_loan,bathroom_amount,building_type,fuel_type,price,il,ilce,mahalle,home_link)
            
            """
            later that might be used for percantage of sold houses according to location
            it is sold and there is no price information thus don't need to collect other details
            """
scraper = House_Scraper('https://www.hepsiemlak.com/en/satilik/daire')
#scraper.discography()
#scraper.get_house_links()
scraper.get_house_details()
