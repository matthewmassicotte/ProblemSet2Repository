from bs4 import BeautifulSoup
import urllib.request

#created by Matthew Massicotte

import warnings
warnings.filterwarnings("ignore")

seed_url = "https://www.federalreserve.gov/newsevents/pressreleases"

urls = [seed_url+".htm"]    #queue of urls to crawl
seen = [seed_url+".htm"]    #stack of urls seen so far
opened = []         
containsCovid = []

minCovidUrl = 25 #continue crawling until this many pages are found containing "covid"
print("Starting with url="+str(urls))
while len(urls) > 0 and len(containsCovid) < minCovidUrl:

    try:
        curr_url=urls.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
    except:
        continue    
        
    soup = BeautifulSoup(webpage)
    text = soup.get_text().lower()
    
    if ("covid" in text):
        containsCovid.append(curr_url)

    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        if seed_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)


print("List of seen URLs:")
for covid_url in containsCovid:
    print(covid_url)