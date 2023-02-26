from bs4        import BeautifulSoup
import requests
import json

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
        page_number=1
        while page_number <= 200:
            page=requests.get(self.url + "?pn={}".format(page_number), headers={'User-Agent': USER_AGENT})
            soup = BeautifulSoup(page.content, 'html.parser')
            parse1=soup.find('div', class_='list-content-properties')
            parse2=parse1.find_all('div', class_='property-info-content')
            for i in parse2:
                self.house_links.append(i.find('a').get('href'))
            
            print("Page {} done".format(page_number))            
            page_number+=1
        self.write_house_links_to_json()


   

"""    def discography(self):
        url = 'https://en.wikipedia.org/wiki/Special:Search?search=%s_discography' % self.name
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find('table', attrs={'class': 'wikitable plainrowheaders'})
        titles = table.findAll(attrs={'scope': 'row'})


        def getAlbumTitles(url):
            albumTitles = [title.text for title in titles]
            return albumTitles

        def getDiscogLinks(url):
            album_href = [row.findAll('a') for row in titles]
            clean_links = []

            for i in album_href:
                for href in i:
                    if href.parent.name == 'i':
                        clean_links.append('https://en.wikipedia.org' + href.get('href'))

            return clean_links

        return dict(zip(getAlbumTitles(url), getDiscogLinks(url)))

name = input('Enter a band name: ')
artist = Band(name)
print(artist.discography())

#beatles = Band('beatles')
#print(beatles.discography())
    """

if __name__ == '__main__':
    scraper = House_Scraper('https://casa.sapo.pt/comprar-apartamentos/')
    scraper.discography()