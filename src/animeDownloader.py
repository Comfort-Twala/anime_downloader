import json
from typing import Dict
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


animeSite = "https://animixplay.to"
headers = {"User-Agent":"Mozilla/5.0"}


def getEpisodes(link):
    epLinks = {}
    #make req
    res = requests.get(link, headers=headers,allow_redirects=True, )
    soup = BeautifulSoup(res.content, "html.parser")

    ##get link to each ep
    #get content of the ep div
    for i in soup.find('div', id="epslistplace"):
        epLinks = json.loads(i)

    
    return epLinks

    
   

#downlod each spcified ep
def downloadEp(link):
    #browser setup
    webOptions = webdriver.FirefoxOptions()
    webOptions.headless = True
    #save file to path defined for recent download with value 2
    webOptions.set_preference("browser.download.folderList",2)
    #disable display Download Manager window with false value
    webOptions.set_preference("browser.download.manager.showWhenStarting", False)
    #download location
    webOptions.set_preference("browser.download.dir","C:\\Users\\cebos\\Documents")
    #MIME set to save file to disk without asking file type to used to open file
    #webOptions.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")
    webOptions.set_preference("browser.download.useDownloadDir", True)
    
    downloadpage = "https://gogoplay1.com/download?id="

    try:

        #get id
        idpos = link.find("id")
        id =  link[idpos+3:41]
        downloadpage = downloadpage + id
        res = requests.get(downloadpage, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")

        #get dowload link, 1st one 360p-> low size
        dLink = ''
        for i in  soup.find("div", {"class":"dowload"}).find_all('a', href=True):
            dLink = i['href']
        
       
        print(downloadpage)
        try:
            driver = webdriver.Firefox(options=webOptions)
            driver.maximize_window()
            driver.get(downloadpage)
            downloadB = driver.find_element(By.CLASS_NAME, "dowload")
            downloadB.click()
            print(driver.current_url)
        except:
            print("Error downloading")
    except:
        print("Error")
    
    

def main():
    print("Anime Downloader v0\n******************")
    
    
    epLinks = getEpisodes("https://animixplay.to/v1/getsuyoubi-no-tawawa-2")

    if(epLinks):
        #print stats
        print(f"Total Episodes: {epLinks.get('eptotal')}")
        
        #confirm download
        eptoDownload = input("Download all episodes? enter yes or range (eg 1-5): ")
        if(eptoDownload):
              if(eptoDownload=="yes"):
                  for link in range(len(epLinks)):
                      downloadEp(epLinks.get(str(link)))
              else:
                #range specified
                for link in range(int(eptoDownload[0]), int(eptoDownload[2])):
                    downloadEp(epLinks.get(str(link)))
        else:
            print("Download cancelled, Thanks")
    else:
        print("No episodes found")





main()


