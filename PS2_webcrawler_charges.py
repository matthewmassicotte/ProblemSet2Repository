from bs4 import BeautifulSoup
import urllib.request

#created by Matthew Massicotte
#Changing something

import warnings
warnings.filterwarnings("ignore")

seed_url = "https://www.sec.gov/news/press-release"
urls = ["https://www.sec.gov/news/pressreleases"]    #queue of urls to crawl
seen = ["https://www.sec.gov/news/pressreleases"]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
containsCharges = []
texts= ["This is the seed url"] 

minChargesUrl = 20 #continue crawling until this many pages are found containing "covid"
print("Starting with url="+str(urls))
while len(urls) > 0 and len(containsCharges) < minChargesUrl:
    try:
        curr_url=urls.pop(0)
        curr_text=texts.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
    except:
        continue    
        
    soup = BeautifulSoup(webpage)
    text = soup.get_text().lower()#make lowercase
    
    #print url if "charges is anywhere in the webpage
    if ("charges" in text):
        containsCharges.append(curr_url)
        print(curr_url)
        print(curr_text)
        print()
        

    for tag in soup.find_all('a', href = True):
        urlText=tag.text
        childUrl = tag['href'] 
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        if seed_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            texts.append(urlText)
            seen.append(childUrl)

