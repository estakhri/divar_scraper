import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


class UrlScraper():

    def __init__(self):

        # using firefox driver, you can change it to other drivers documented in selenium website
        options = webdriver.FirefoxOptions()
        # prevent loading images
        options.set_preference('permissions.default.image', 2)
        self.driver = webdriver.Firefox(options=options)


    def load_page(self, url):

        self.driver.get(url)
        #wait for completely loading page
        time.sleep(2)
        # Here we fetched driver page source from driver.
        page_html = self.driver.page_source
        # BeautifulSoup is dumping page source to html
        self.soup = BeautifulSoup(page_html, 'html.parser')


    def create_csv_file(self):

        # create csv file with header
        rowHeaders = ["Mahale" ,"Title", "Subtitle", "Meter", "Year", "Room", "TotalPrice", "MeterPrice", "Floor", "Description"]
        self.file_csv = open('DivarScraper.csv', 'w', newline='', encoding='utf-8-sig')
        self.mycsv = csv.DictWriter(self.file_csv, delimiter=";",fieldnames=rowHeaders)
        self.mycsv.writeheader()

    def scrap(self):

        # Here I fetch all products div elements
        first_page = (self.soup.find_all('div', class_='kt-row'))
        for i in first_page:
            Title = i.find('h1', class_='kt-page-title__title').text
            Subtitle = i.find('div', class_='kt-page-title__subtitle').text
            details = i.find_all('td', class_='kt-group-row-item__value')
            Meter = details[0].text
            Year = details[1].text
            Room = details[2].text
            details2 = i.find_all('p', class_='kt-unexpandable-row__value')
            TotalPrice = details2[0].text.replace("تومان","").replace('٬','').strip()
            MeterPrice = details2[1].text.replace("تومان","").replace('٬','').strip()
            Floor = details2[2].text
            Description = i.find('p', class_='kt-description-row__text--primary').text.replace("\n", " ")
            #try:
                #warranty_details = [j.text for j in details if j.text[:14] == "Brand Warranty"][0]
            #except:
                #warranty_details = "No data available"

            self.mycsv.writerow({"Mahale": self.mahale,"Title": Title, "Subtitle": Subtitle, "Meter": Meter, "Year": Year, "Room": Room, "TotalPrice": TotalPrice, "MeterPrice": MeterPrice, "Floor": Floor, "Description": Description})

    def tearDown(self):

        # Here driver.quit function is used to close chromedriver
        self.driver.quit()
        # Here we also need to close Csv file which I generated above
        self.file_csv.close()

    def scrap_page(self,url):

        self.driver.get(url)
        # scroll down to load more data
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # scroll down again to load more data
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for data to load completly
        time.sleep(30)
        # Get page html source
        page_html = self.driver.execute_script("return document.documentElement.outerHTML;")
        soup = BeautifulSoup(page_html, 'html.parser')
        # read all main data from main div with class post-list__widget-col-c1444
        pages = soup.find_all('div', class_='post-list__widget-col-c1444')
        for p in pages:
            if not p.find('a', class_='') is None:
                href="https://divar.ir"+p.find('a', class_='')['href']
                # for viewing what happened during the job
                print(href)
                self.load_page(href)
                self.scrap()




if __name__ == "__main__":
    # these are shiraz areas, you can change them based on you city's areas
    urls=["abjavar","abyari","shiraz-cemetery","abunasr","abiverdi","ahmad-abad","ahmadi","eram-shiraz","eslahnejad","atlasi",
          "emam-hosein","bagh-e-takht","berijestoon","besat","bonakdaran","azaadi","rahmat-boulevard","pdonak","tachara","tappeh-telviziyoun","tahavoli",
          "barbari-terminal","talkh-e-dash","tondgooyan","janbazan","jomhoori","javadiyeh","chogha","chencheneh","chogiah","hafeziyeh","hossein-abad",
          "kholde-barin","khalili","derki","darvazeh","dokuhak","dinakan","rahmat-abad","rezvan","shahrak-rokn-abad",
          "rishmak","zargari","zerehi","zand","ziba-shahr","saman","sait-edari","sattar-khan","bani-hashemi","saadiyeh","siloo","saadi-cinema","shah-gholi-beigi",
          "sharif-abad","arian-town","shahrak-imam-hossein","fargaz","amir-kabir","shahrak-isar","shahrak-bahonar","bezin-town","shahrak-parvaaz","jamaran","hojat-abad",
          "sajjadieh","seraj","sharak-e-sadi","shahrak-beheshti","shahrak-motahhari","shahrak-erfan","fajr-town","qasre-qomsheh","koshkek","shahrak-golestaan",
          "north-shahrak-golestan","shahrak-golha","shahrak-e-mokhaberat","shahrak-modares","shahrak-mahdiabad","mehregan","shahrak-e-shahid-navvab-e-safavi",
          "valfajr","shahrak-valiasr","sheikh-ali-choupan","shishehgari","saheb-al-zaman","edalat-boulevard","afif-abad","farzanegan","farhang-shahr","farhangian",
          "fazl-abad","fazilat-boulevard","east-ghodoosi","west-ghodoosi","ghasr-dasht","ghaleh-shahzadeh-bagom","ghaleh-ghebleh","ghale-no","karandish","kaftarak",
          "koozehgari","kuy-azadi","kuy-zahra","kuy-farhangian","kuy-ghozat","kuy-valiasr","kuy-yas","kian-shahr",
        "goldasht","goldasht-hafez","goldasht-mohammadi",
          "goldasht-moaliabad","golshan","golkoub","god-araban","gouyom","laleh","lab-e-ab","lashkari","mah-firouzan","mehrab","kolbeh","dozak","kuy-sang-siah","kuy-tollab",
        "mohammadiyeh","mahmoudieh","moslem","west-moshir","moaliabad","maqar","molla-sadra","mansoor-abad","paygah-havayi","mahdi-abad","mahdiyeh","mianrood",
        "shah-square","narenjestan","neshat","nasr-abad","niayesh","modarresblvd","vazir-abad","vesal","haft-tanan","hoveyzeh"]
    UrlScraper = UrlScraper()
    UrlScraper.create_csv_file()
    for url in urls:
        UrlScraper.mahale=url
        # this url used for shiraz city, you can change to other cities
        UrlScraper.scrap_page("https://divar.ir/s/shiraz/buy-apartment/"+url+"?building-age=-1&sort=sort_date")

    UrlScraper.tearDown()
    print("Fetching data completed.")
