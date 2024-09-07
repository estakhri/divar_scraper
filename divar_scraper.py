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

        #setting browser window size for specific porpose
        #self.driver.set_window_size(800, 6000)

        self.ads_stat=dict()

    # loading main page of the category
    def load_page(self, url):

        self.driver.get(url)
        #wait for completely loading page
        time.sleep(2)
        #  fetching driver page source from driver.
        page_html = self.driver.page_source
        # BeautifulSoup is dumping page source to html
        return BeautifulSoup(page_html, 'html.parser')


    # create scv file for writing ads data
    def create_csv_file(self):

        # create csv file with header
        rowHeaders = ["Mahale" ,"Title", "Subtitle", "Meter", "Year", "Room", "TotalPrice", "MeterPrice", "Floor", "Description"]
        self.file_csv = open('DivarScraper.csv', 'w', newline='', encoding='utf-8-sig')
        self.mycsv = csv.DictWriter(self.file_csv, delimiter=";",fieldnames=rowHeaders)
        self.mycsv.writeheader()

    # write ad data to csv file
    def write_to_csv_file(self,ad):
        self.mycsv.writerow({"Mahale": ad['Mahale'],"Title": ad['Title'], "Subtitle": ad['Subtitle'], "Meter": ad['Meter'], "Year": ad['Year'], "Room": ad['Room'], "TotalPrice": ad['TotalPrice'], "MeterPrice": ad['MeterPrice'], "Floor": ad['Floor'], "Description": ad['Description']})

    # scrap an ad page
    def scrap(self,url,mahale):

        # Here fetching all ads div elements
        ad_page = (self.load_page(url).find_all('div', class_='kt-row'))
        ad=None
        for i in ad_page:
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
            ad={"Mahale": mahale,"Title": Title, "Subtitle": Subtitle, "Meter": Meter, "Year": Year, "Room": Room, "TotalPrice": TotalPrice, "MeterPrice": MeterPrice, "Floor": Floor, "Description": Description}
        return ad

    # closing csv file and browser
    def tearDown(self):

        # Here driver.quit function is used to close chromedriver
        self.driver.quit()
        # Here we also need to close Csv file which I generated above
        self.file_csv.close()

    # scrap all data by getting ads and scrapping them and saving to csv file
    def scrap_page(self,url,mahale):

        ads=self.get_ads(url)
        print(url,len(ads))
        for ad in ads:
            # for viewing what happened during the job
            print(ads[ad])
            scrap_ad=self.scrap(ads[ad],mahale)
            self.write_to_csv_file(scrap_ad)


    # get list of ads in a category page
    def get_ads(self,url):
        self.driver.get(url)
        # scroll down to end to load more data
        lastHeight=0
        ads=dict()
        client_height=self.driver.execute_script("return document.documentElement.clientHeight;")

        # scroll slowly in page and scrap all ads *** DO NOT SCROLL MANUALLY LET PROGRAM DO IT ***
        while lastHeight<self.driver.execute_script("return document.documentElement.scrollHeight;"):
            #scroll slowly by browser height
            self.driver.execute_script("window.scrollBy(0,"+str(client_height)+");")
            lastHeight=self.driver.execute_script("return document.documentElement.scrollTop;")+client_height
            # Get page html source
            page_html = self.driver.execute_script("return document.documentElement.outerHTML;")
            soup = BeautifulSoup(page_html, 'html.parser')
            pages = soup.find_all('div', class_='post-list__widget-col-c1444')
            for p in pages:
                if not p.find('a', class_='') is None:
                    href="https://divar.ir"+p.find('a', class_='')['href']
                    # adding each ad to ads dictionary
                    ads[href[href.rfind('/')+1:]]=href
            time.sleep(5)
        self.ads=ads
        return ads

    # count and save ads of a category page
    def save_count_ads_to_file(self,url):
        rowHeaders={"Mahale","URL","Count"}
        ads=self.get_ads(url)
        file_csv= open('DivarAds.csv', 'a+', newline='', encoding='utf-8-sig')
        _csv=csv.DictWriter(file_csv, delimiter=";",fieldnames=rowHeaders)
        # if any ads exist in the url
        if len(ads)>0:
            _csv.writerow({"Mahale":url[url.rfind('/')+1:url.rfind('?')],"URL":url,"Count":len(ads)})
        file_csv.close()







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

        # this url used for shiraz city, you can change to other cities
        UrlScraper.scrap_page("https://divar.ir/s/shiraz/buy-apartment/"+url+"?building-age=-1&sort=sort_date",url)
        # just for counting ads in Divar
        #UrlScraper.count_ads_to_file("https://divar.ir/s/shiraz/buy-apartment/"+url+"?building-age=-1&sort=sort_date")

    UrlScraper.tearDown()
    print("Fetching data completed.")