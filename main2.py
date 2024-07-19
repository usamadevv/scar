from bs4 import BeautifulSoup

import requests
import re

# Faking real user visit.
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
def pythonFunction(self,querystr):
    links=[]
    
    for page in range(5):
       params = {'q': '"Staffing" "NC" -intitle:"profiles" -inurl:"dir/ " "@gmail.com"','start': page * 10}

       # Fetch the HTML content of the search results page.
       html = requests.get(f'https://www.google.com/search', headers=headers, params=params).text
       # Parse the HTML content using BeautifulSoup.
       soup = BeautifulSoup(html, 'html.parser')
       print(html)
       search_results = soup.find_all('div', class_="yuRUbf")
       print(search_results)

       search = soup.find_all('div', class_="VwiC3b")
       searc2 = soup.find_all('div', class_="yuRUbf")

       searc3 = soup.find_all('h3', class_="LC20lb")
       # Select elements using CSS selectors.
       for index,h in enumerate(search):
                         print(index)
                         print(search[index])
                         links.append({"meta":h.find('span').text,"link":searc2[index].a.get('href'),"title":searc3[index].text,"Email":extract_first_gmail_address(h.find('span').text)})
    print(links)
    print(len(links))       


