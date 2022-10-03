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

minChargesUrl = 20 #continue crawling until this many pages are found containing "covid"
print("Starting with url="+str(urls))
while len(urls) > 0 and len(containsCharges) < minChargesUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
    except:
        continue    
        
    soup = BeautifulSoup(webpage)
    text = soup.get_text().lower()
    
    #print url if "charges is anywhere in the webpage
    if ("charges" in text):
        containsCharges.append(curr_url)
        print(curr_url)
        print()
        
        #print the title and body of the article
        for div in soup.findAll('h1', {'class': "article-title"}  ):
            print(div.text.strip())
            print()
        for div in soup.findAll('div', {'class': "article-body"}  ):
            print(div.text.strip())
            print("\n \n")

    for tag in soup.find_all('a', href = True):
        childUrl = tag['href'] 
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        if seed_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

