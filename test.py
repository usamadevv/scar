import math
import urllib.parse
           
PROXIES = {"http": "http://LUjkUDqmGjLfyejU:3zG9pHGluq1RiutT@geo.iproyal.com:12321",
"https": "http://LUjkUDqmGjLfyejU:3zG9pHGluq1RiutT@geo.iproyal.com:12321"}

import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
import requests
links=[]
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def calcmanta(result,keyword):
                 a_tag = result.find('div', class_="font-serif text-lg overflow-wrap text-gray-900 flex justify-between")
                 phone=''
                 title=''
                 category=''
                 street=''
                 linka=''
                 bdy=''
                 if a_tag:
                         # Find the <span> tag inside the <a> tag
                         span_tag = a_tag.find('a')
                         if span_tag:
                             # Get the text inside the <span> tag
                             span_text = span_tag.text.strip()
                             print(f"Text inside span: {span_text}")
                             title=span_text
    # Find the phone number inside <div> with class "call-number"
                 call_number_div = result.find('div',class_='hidden md:flex items-start mt-2')
                 if call_number_div:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        p=call_number_div.find('div')
                        if p:
                               phone=p.text.strip()
                       
                        
                 else:
                       print("No phone number found.")
                 webdiv = result.find('a',class_='cursor-pointer hover:underline')
                 if webdiv:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        p=webdiv.get('href')
                        if p:
                               parsed_url = urllib.parse.urlparse(p)
                               linka = parsed_url.netloc
                       
                        
                 else:
                       print("No phone number found.")
                 streetaddress = result.find('div',class_='flex items-start mt-1 md:mt-3')
                 if streetaddress:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        st2=streetaddress.find('div')

                        street = st2.get_text(separator=' ', strip=True)


                       
                 else:
                       print("No phone number found.")    
                 streetaddress = result.find('div',class_='flex items-start mt-1 md:mt-3')
                 if streetaddress:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        st2=streetaddress.find('div')

                        street = st2.get_text(separator=' ', strip=True)


                       
                 else:
                       print("No phone number found.") 
                 body = result.find('div',class_='border-t border-gray-200 mt-4 pt-4 px-20 text-gray-800 clamp lines-2 text-gray-800')
                 if body:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                       

                        bdy = body.text.strip()


                       
                 else:
                       print("No phone number found.")  
                 cty = result.find('div',class_='hidden md:flex flex-col w-3/5 pl-4 text-gray-500')
                 if cty:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                       

                        ctyall = cty.findall('span',class_="text-gray-800")
                        for ct in ctyall:
                               category=category+ct


                       
                 else:
                       print("No phone number found.")      
                 
         
                 

                 return {'phone':phone,'title':title,'category':category,'street':street,'link':linka,'bdy':bdy}
      
def ass():
          try:
               html = requests.get(f'https://www.manta.com/search?search=plumber&context=industry&search_source=nav&city=Raleigh&state=North%20Carolina&country=United%20States&pt=35.8324%2C-78.6438&device=desktop&screenResolution=1680x1050', headers={'User-Agent': get_random_user_agent()}, proxies=PROXIES).text
               if "did not match any documents" in html:
                print("Search ended")
                return []
          except Exception as e:

              print(e)
              print('error')  
              return[]
    
           # Parse the HTML content using BeautifulSoup.
          soup = BeautifulSoup(html, 'html.parser')
          search_results = soup.find_all('div', class_="md:rounded bg-white border-b border-primary-light-v1 px-3 py-4 md:p-6 md:mt-4")
          print(search_results)
          for result in search_results:
                 js= calcmanta(result,'hvac')
                 links.append(js)
        

          print(links)
          print(len(links)) 

ass()
