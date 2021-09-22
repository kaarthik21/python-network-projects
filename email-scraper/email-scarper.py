from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re

user_url = str(input('Enter full Target URL To Scan: '))
urls = deque([user_url])
# deque to append and pop elements on both ends

scraped_urls = set()
emails = set()
# set is a mutable set of immutable items

count = 0
try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)
        # Adding the scanned URL to scraped_urls

        parts = urllib.parse.urlsplit(url)
        # urllib.parse will separate the contents of the full url to combine strings back to url
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        # rfind is used to get the highest index value in a substring and gives -1 if not found, find is used to find the first substring found from index 0 
        print('[%d] Processing %s' % (count, url))
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
                
except KeyboardInterrupt:
    print('[-] Closing!')

for mail in emails:
    print(mail)
