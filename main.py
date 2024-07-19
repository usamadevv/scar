import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QObject, pyqtSlot,QVariant
from PyQt5.QtWebChannel import QWebChannel
import os
from bs4 import BeautifulSoup
import openpyxl
from openpyxl import Workbook
import requests, lxml
from selenium import webdriver
import json
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pathlib import  Path
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import time

from fake_useragent import UserAgent

desktop_path = Path.home() / "Desktop"
PROXIES = {"http": "http://LUjkUDqmGjLfyejU:3zG9pHGluq1RiutT@geo.iproyal.com:12321",
"https": "http://LUjkUDqmGjLfyejU:3zG9pHGluq1RiutT@geo.iproyal.com:12321"}



# Faking real user visit.
import re
def calculate_text_size_in_mb(text):
    # Calculate the size of the text data in bytes
    bytes_size = len(text.encode('utf-8'))  # Assuming UTF-8 encoding

    # Convert bytes to megabytes
    mb_size = bytes_size / (1024 * 1024)

    return mb_size
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
def extract_phone_numbers(html_content):
    # Implement your extraction logic here
    # Example: searching for phone numbers with minimum length of 8 digits
     
    phone_regex = re.compile(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})')

    # Find all phone numbers matching the pattern
    phone_numbers = phone_regex.findall(html_content)
    if phone_numbers:
        return phone_numbers[0]  # Return the first phone number found
    else:
        return None  # Return None if no valid phone number found

def extract_text_from_html(html_content):
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text from the soup object
    text_content = soup.get_text(separator=' ', strip=True)

    return text_content
def extract_first_email_address(text):
    """
    Extracts the first email address (any domain) from the provided text.

    Args:
    text (str): The input text from which to extract the email address.

    Returns:
    str: The first extracted email address, or None if no email address is found.
    """
    # Regular expression pattern to match email addresses with any domain
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Search for the first match of the pattern in the text
    match = re.search(email_pattern, text)
    
    if match:
        return match.group(0)
    else:
        return None
def extract_first_gmail_address(text):
    """
    Extracts the first Gmail address from the provided text.

    Args:
    text (str): The input text from which to extract the Gmail address.

    Returns:
    str: The first extracted Gmail address, or None if no Gmail address is found.
    """
    # Regular expression pattern to match Gmail addresses
    gmail_pattern = r'\b[A-Za-z0-9._%+-]+@gmail\.com\b'
    
    # Search for the first match of the pattern in the text
    match = re.search(gmail_pattern, text)
    
    if match:
        return match.group(0)
    else:
        return None



script_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_dir, "indexa.html")
def remove_script_and_head(soup):
    # Remove all <script> tags and their contents
    for script in soup.find_all('script'):
        script.extract()

    # Remove the <head> section and its contents
    head_tag = soup.find('head')
    if head_tag:
        head_tag.extract()

    return soup
def should_skip_response(response):
    # Check if the response is empty or contains garbled data
    if not response.text.strip():  # Check if the text content is empty or whitespace
        return True
    
    # Additional checks based on content type or specific indicators
    content_type = response.headers.get('Content-Type', '').lower()
    if 'text' not in content_type:
        return True
    
    # Add more checks if needed based on response content
    
    return False

def calc(result):
                 a_tag = result.find('a', class_="business-name")
                 phone=''
                 title=''
                 category=''
                 street=''
                 linka=''
                 bdy=''
                 if a_tag:
                         # Find the <span> tag inside the <a> tag
                         span_tag = a_tag.find('span')
                         if span_tag:
                             # Get the text inside the <span> tag
                             span_text = span_tag.text.strip()
                             print(f"Text inside span: {span_text}")
                             title=span_text

    # Find the phone number inside <div> with class "call-number"
                 call_number_div = result.find('span', class_="call-number")
                 if call_number_div:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        phone_number_text = call_number_div.text
                        # Extract the actual phone number text from the inner text
                        print(f"Phone number: {phone_number_text}")
                        phone=phone_number_text
                 else:
                       print("No phone number found.")
                 streetaddress = result.find('span', class_="street-address")
                 if streetaddress:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        sta = streetaddress.text
                        # Extract the actual phone number text from the inner text
                        print(f"Phone number: {sta}")
                        street=sta
                 else:
                       print("No phone number found.")      
                 linkttag = result.find('a', class_="weblink-button")
                 
                 if linkttag:
                        
                             # Get the text inside the <span> tag
                             linka=linkttag.get('href')

                 categories_div = result.find('div', class_='categories')
                 if categories_div:
                     # Find all <a> tags within the div
                     category_links = categories_div.find_all('a')
    
                     # Extract and print the text of each category
                     for link in category_links:
                          category_name = link.text.strip()
                          print(category_name)
                          category=category+', '+category_name
                 else:
                    print("No categories found.")
                 bodies = result.find('p', class_='body')
                 if bodies:
                     # Find all <a> tags within the div
                     body = bodies.find('span')
                     if body:
                        bdy=body.text.strip()


    
                    
                 else:
                    print("No categories found.")

                 return {'phone':phone,'title':title,'category':category,'street':street,'link':linka,'bdy':bdy}


def calcbbb(result):
                 a_tag = result.find('a', class_="text-blue-medium css-1jw2l11 eou9tt70")
                 phone=''
                 title=''
                 category=''
                 street=''
                 linka=''
                 bdy=''
                 if a_tag:
                         # Find the <span> tag inside the <a> tag
                         span_tag = a_tag.find('span')
                         if span_tag:
                             # Get the text inside the <span> tag
                             span_text = span_tag.text.strip()
                             print(f"Text inside span: {span_text}")
                             title=span_text

    # Find the phone number inside <div> with class "call-number"
                 call_number_div = result.find('p', class_="bds-body css-1u1ibea eo3kxzw0")
                 if call_number_div:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        phone_number_text = call_number_div.find('a')
                        # Extract the actual phone number text from the inner text
                        print(f"Phone number: {phone_number_text}")
                        phone=phone_number_text.text.strip()
                 else:
                       print("No phone number found.")
                 streetaddress = result.find('p', class_="bds-body text-size-5 text-gray-70")
                 if streetaddress:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        street = streetaddress.get_text(separator=' ', strip=True)


                       
                 else:
                       print("No phone number found.")      
                 
                 if a_tag:
                        
                             # Get the text inside the <span> tag
                             linka=a_tag.get('href')

                 categories_div = result.find('p', class_='bds-body text-size-4 text-gray-70')
                 if categories_div:
                     # Find all <a> tags within the div
                     category_name = categories_div.text.strip()
                     category=category_name
                     bdy=category_name
                 else:
                    print("No categories found.")
           

                 return {'phone':phone,'title':title,'category':category,'street':street,'link':linka,'bdy':bdy}

def calcezlocal(result,keyword):
                 a_tag = result.find('h3', class_="fn org")
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
                             linka='https://ezlocal.com/'+str(span_tag.get('href'))

    # Find the phone number inside <div> with class "call-number"
                 call_number_div = result.find('strong')
                 if call_number_div:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                       
                        phone=call_number_div.text.strip()
                 else:
                       print("No phone number found.")
                 def has_address(tag):
                        return tag.name == 'p' and any(span_tag.name == 'span' for span_tag in tag.find_all('span'))
      
                 streetaddress = result.find('div',class_='col-md-9 col-xs-10 businessdetails').find(has_address)
                 if streetaddress:
                        # Find the inner text inside the <div> (assuming it contains the phone number)
                        street = streetaddress.get_text(separator=' ', strip=True)


                       
                 else:
                       print("No phone number found.")      
                 
         
                 category=keyword
                 bdy=keyword

                 return {'phone':phone,'title':title,'category':category,'street':street,'link':linka,'bdy':bdy}
                  
def process_page(town,state,keyword,page_number):
    
    links = []
    try:
        html = requests.get(f'https://cars.superpages.com/{town}-{state}/{keyword}?page={page_number}', headers=headers, proxies=PROXIES).text
        if "did not match any documents" in html:
            print(f"Search ended for page {page_number}")
            return links
    except Exception as e:
        print(f"Error fetching page {page_number}: {e}")
        return links
    time.sleep(2) 
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.find_all('div', class_="result")
    
    for result in search_results:
        js = calc(result)  # Assuming calc function is defined elsewhere
        links.append(js)

    print(f"Processed page {page_number}, found {len(search_results)} results.")
    return links
def process_page2(town,state,keyword,page_number):
    links = []
    
    try:
        html = requests.get(f'https://www.bbb.org/search?find_country=USA&find_loc={town}+{state.upper()}&find_text={keyword}&find_type=Category&page={page_number}', headers=headers, proxies=PROXIES).text
        if "did not match any documents" in html:
            print(f"Search ended for page {page_number}")
            return links
    except Exception as e:
        print(f"Error fetching page {page_number}: {e}")
        return links
    time.sleep(1) 
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.find_all('div', class_=re.compile(r'\bresult-item-ab\b'))
    
    for result in search_results:
        js = calcbbb(result)  # Assuming calc function is defined elsewhere
        links.append(js)

    print(f"Processed page {page_number}, found {len(search_results)} results.")
    return links
def process_page3(town,state,keyword,page_number):
    links = []
    
    try:
        html = requests.get(f'https://ezlocal.com/{state}/{town}/{keyword}:p={page_number}', headers=headers, proxies=PROXIES).text
        if "did not match any documents" in html:
            print(f"Search ended for page {page_number}")
            return links
    except Exception as e:
        print(f"Error fetching page {page_number}: {e}")
        return links
    time.sleep(1) 
    soup = BeautifulSoup(html, 'html.parser')
    search_results = soup.find_all('div', class_="result vcard row")
    
    for result in search_results:
        js = calcezlocal(result)  # Assuming calc function is defined elsewhere
        links.append(js)

    print(f"Processed page {page_number}, found {len(search_results)} results.")
    return links

class Backend(QObject):
    @pyqtSlot(str,str,str,int,result=QVariant)
    def squarepagescheck(self,keyword,state,town,ik):
           print(f"{town}-{state}/{keyword}")
           links=[]
           try:
               html = requests.get(f'https://cars.superpages.com/{town}-{state}/{keyword}?page=1', headers=headers, proxies=PROXIES).text
               if "did not match any documents" in html:
                print("Search ended")
                return []
           except:
              print('error')  
              return links
    
           # Parse the HTML content using BeautifulSoup.
           soup = BeautifulSoup(html, 'html.parser')

           print(html)

           paginat = soup.find('div', class_="pagination")
           paginat2 = paginat.find('span')
           last_number_str = paginat2.text.strip().split()[-1]
           total_items = int(last_number_str)
           ceiling_value = math.ceil(total_items / 30)
            # Parse the HTML content using BeautifulSoup
           print(html)
           search_results = soup.find_all('div', class_="result")
           print(search_results)
           for result in search_results:
                 js= calc(result)
                 links.append(js)
           print(links)
           print(len(links))
           return {"links":links,"size":total_items,"pages":ceiling_value}        
 
    @pyqtSlot(str,str,str,int,result=QVariant)
    def squarepages(self,keyword,state,town,ik):
           print(f"{town}-{state}/{keyword}")
           links=[]
           try:
               html = requests.get(f'https://cars.superpages.com/{town}-{state}/{keyword}?page=1', headers=headers, proxies=PROXIES).text
               if "did not match any documents" in html:
                print("Search ended")
                return []
           except Exception as e:
              print(e)
              print('error')  
              return links
    
           # Parse the HTML content using BeautifulSoup.
           soup = BeautifulSoup(html, 'html.parser')

           print(html)

           paginat = soup.find('div', class_="pagination")
           paginat2 = paginat.find('span')
           last_number_str = paginat2.text.strip().split()[-1]
           total_items = int(last_number_str)
           ceiling_value = math.ceil(total_items / 30)
            # Parse the HTML content using BeautifulSoup
           print(html)
           search_results = soup.find_all('div', class_="result")
           print(search_results)
           for result in search_results:
                 js= calc(result)
                 links.append(js)
           max_threads = 4
           with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    future_to_page = {executor.submit(process_page,town,state,keyword, page_number): page_number for page_number in range(2, ceiling_value)}
                    for future in as_completed(future_to_page):
                                 page_number = future_to_page[future]
                                 try:
                                   page_links = future.result()
                                   if page_links:
                                      links.extend(page_links)
                                 except Exception as e:
                                      print(f"Exception occurred for page {page_number}: {e}")
                                 time.sleep(2)





     
           print(links)
           print(len(links))
           return links        
 
    @pyqtSlot(str,str,str,int,result=QVariant)
    def bbbsite(self,keyword,state,town,ik):
           links=[]
           print(f"{town}-{state}/{keyword}")
           try:
               html = requests.get(f'https://www.bbb.org/search?find_country=USA&find_loc={town}+{state.upper()}&find_text={keyword}&find_type=Category&page=1', headers=headers, proxies=PROXIES).text
               if "did not match any documents" in html:
                print("Search ended")
                return []
           except:
              print('error')  
              return[]
    
            # Parse the HTML content using BeautifulSoup.
           soup = BeautifulSoup(html, 'html.parser')
           search_results = soup.find_all('div', class_=re.compile(r'\bresult-item-ab\b'))
           print(search_results)
           for result in search_results:
                 js= calcbbb(result)
                 links.append(js)
           max_threads=4
           with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    future_to_page = {executor.submit(process_page2,town,state,keyword, page_number): page_number for page_number in range(2, 15)}
                    for future in as_completed(future_to_page):
                                 page_number = future_to_page[future]
                                 try:
                                   page_links = future.result()
                                   if page_links:
                                      links.extend(page_links)
                                 except Exception as e:
                                      print(f"Exception occurred for page {page_number}: {e}")
                                 time.sleep(2)



           print(links)
           print(len(links))
           return links 

    @pyqtSlot(str,str,str,int,result=QVariant)
    def ezscrape(self,keyword,state,town,ik):
           links=[]
           print(f"{town}-{state}/{keyword}")
           try:
               html = requests.get(f'https://ezlocal.com/{state}/{town}/{keyword}', headers=headers, proxies=PROXIES).text
               if "did not match any documents" in html:
                print("Search ended")
                return []
           except:
              print('error')  
              return[]
    
            # Parse the HTML content using BeautifulSoup.
           soup = BeautifulSoup(html, 'html.parser')
           search_results = soup.find_all('div', class_="result vcard row")
           paginat = soup.find('div', class_="sortMe")
           paginat2 = paginat.find('strong')
           last_number_str = paginat2.text.strip().split()[-1]
           total_items = int(last_number_str)
           ceiling_value = math.ceil(total_items / 50)
           print(search_results)
           for result in search_results:
                 js= calcezlocal(result,keyword)
                 links.append(js)

           max_threads=4
           with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    future_to_page = {executor.submit(process_page3,town,state,keyword, page_number): page_number for page_number in range(2, ceiling_value)}
                    for future in as_completed(future_to_page):
                                 page_number = future_to_page[future]
                                 try:
                                   page_links = future.result()
                                   if page_links:
                                      links.extend(page_links)
                                 except Exception as e:
                                      print(f"Exception occurred for page {page_number}: {e}")
                                 time.sleep(2)



           print(links)
           print(len(links))
           return links 
    @pyqtSlot(str,str,result=str)
    def login(self,email,passw):
         
         response = requests.post('http://13.59.30.246:3000/api/login2', json={"email":email,"password":passw}, headers=headers)
         resa=response.json()
         fr= json.dumps(resa)
         
         
         return fr
    @pyqtSlot(str,int,result=str)
    def updateleads(self,_id,count):
         
         response = requests.post('http://13.59.30.246:3000/api/updateleads', json={"count":count,"_id":_id}, headers=headers)
         resa=response.json()
         fr= json.dumps(resa)
         
         
         return fr

         





    @pyqtSlot(list,str)

    
    def pythonFunction2sq(self,globallinks,querystr):
             qr=querystr.split('234')
             excel_file_path = desktop_path / f"{qr[0]}_{qr[1]}.xlsx"
             column_mapping = {
    'title': 'Company',
      'category':'Category',
          'street' :'Address',
               'phone' :'Phone',
                    'link': 'Website',  # Rename 'Link' to 'URL'
    'bdy': 'Description',  # Rename 'Description' to 'Page Description'
 
    
    
       # Rename 'Category' to 'Type'
}

          

             
             # Create a DataFrame
            
             df = pd.DataFrame(globallinks)
             df = df[list(column_mapping.keys())]
             df.columns = [column_mapping[col] for col in df.columns]
             with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
                  df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # Get the xlsxwriter workbook and worksheet objects
                  workbook = writer.book
                  worksheet = writer.sheets['Sheet1']
    
    # Freeze the first row
                  worksheet.freeze_panes(1, 0)  # Freeze the first row
    
    # Set column width
                  worksheet.set_column(0, len(df.columns) - 1, width=40)
    
    # Format for the first row (header row)
                  header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'center',
        'fg_color': '#A0BCE8',  # Light red background
        'border': 1
    })
    
    # Apply the header format
                  for col_num, value in enumerate(df.columns.values):
                          worksheet.write(0, col_num, value, header_format)

    # Save the Excel file
                  writer._save()



# Create a Pandas Excel writer using XlsxWriter as the engine
          

    @pyqtSlot(list,str)

    
    def pythonFunction2(self,globallinks,querystr):
             qr=querystr.split('234')
             excel_file_path = desktop_path / f"{qr[0]}_{qr[1]}.xlsx"
             
             

             df = pd.DataFrame(globallinks).to_excel(excel_file_path, index=False)

    @pyqtSlot(str,str,str,str,int,result=QVariant)

    def pythonFunction(self,querystr,phone,email,site,i):
     size=0
     links=[]
     print(i)
     qr=querystr.split('234')
     query=""
     if site == 'not' and phone == 'not' and email=='not':
          query = f'"{qr[0]}"' f' "{qr[1]}"' 
     elif site == 'not' and phone == 'not' and email!='not': 
          query = f'"{qr[0]}"' f' "{qr[1]}"' '  "@gmail.com"' 
     elif site == 'not' and phone != 'not' and email=='not': 
          query = f'"{qr[0]}"' f' "{qr[1]}"' ' "Phone"'  
     elif site == 'not' and phone != 'not' and email!='not': 
          query = f'"{qr[0]}"' f' "{qr[1]}"' ' "Phone" "@gmail.com"'  
     elif site != 'not' and phone == 'not' and email=='not':
          query = f'"{qr[0]}"' f' "{qr[1]}" 'f'"site:{site}"'  
     elif site != 'not' and phone == 'not' and email!='not': 
          query = f'"{qr[0]}"' f' "{qr[1]}"' '  "@gmail.com" ' f'"site:{site}"'  
     elif site != 'not' and phone != 'not' and email=='not': 
          query = f'"{qr[0]}"' f' "{qr[1]}"' ' "Phone" ' f'"site:{site}"' 
     elif site != 'not' and phone != 'not' and email!='not': 
          query = f'"{qr[0]}"' f' "{qr[1]}"' ' "Phone" "@gmail.com" 'f'"site:{site}"' 
     else: 
          query = f'"{qr[0]}"' f' "{qr[1]}"' ' "Phone" "@gmail.com"' 


     
     print(query)
     params = {'q':  query,'start': i * 10}
     # Fetch the HTML content of the search results page.s = requests.session(



     try:
       html = requests.get(f'https://www.google.com/search', headers=headers, proxies=PROXIES, params=params).text
       if "did not match any documents" in html:
         print("Search ended")
         return []
     except:
          print('error')  
          return[]
    
     # Parse the HTML content using BeautifulSoup.
     soup = BeautifulSoup(html, 'html.parser')
     print(html)
     search_results = soup.find_all('div', class_="yuRUbf")
     print(search_results)
     size =size+ calculate_text_size_in_mb(html)

     search = soup.find_all('div', class_="VwiC3b")
     searc2 = soup.find_all('div', class_="yuRUbf")

     searc3 = soup.find_all('h3', class_="LC20lb")
     # Select elements using CSS selectors.
     for index,h in enumerate(search):
                         print(index)
                         print(search[index])
                         links.append({"meta":h.find('span').text,"industry":qr[0],"area":qr[1],"link":searc2[index].a.get('href'),"title":searc3[index].text,"Email":extract_first_gmail_address(h.find('span').text),"Phone":extract_phone_numbers(h.find('span').text)})
     print(links)
     print(len(links)) 
     '''
     for index, link_obj in enumerate(links):
       link = link_obj['link']  # Access the 'link' key in each dictionary
       print(link)
       if link.lower().endswith('.pdf'):
            print(f"Skipping {link} because it is a PDF")
            continue
       try:
        headersa = {'User-Agent': get_random_user_agent()}


        response = requests.get(link,headers=headersa, timeout=4)  # Timeout set to 3 seconds
        response.raise_for_status()
        if response.status_code == 200:
            response.encoding='utf-8'
            if not response.text.strip():  # Check if the text content is empty or whitespace
                print(f"Skipping {link} due to unreadable or unexpected data")
                continue
            

        
            html_content = response.text
            size =size+ calculate_text_size_in_mb(html)

            # Create BeautifulSoup object
           

            soupx = BeautifulSoup(html_content, 'html.parser')
            soupx = remove_script_and_head(soupx)
            clean_html = str(soupx)
            print(clean_html)

            text_content = extract_text_from_html(clean_html)
            print(text_content)

            phone_number = extract_phone_numbers(text_content)
            email=extract_first_email_address(text_content)
            # Store the extracted phone number back into the JSON object
            links[index]['Phone'] = phone_number
            links[index]['Email'] = email
            print(phone_number)
        else:
            print(f"Failed to fetch URL: {link}. Status code: {response.status_code}")
       except requests.exceptions.Timeout:
             print(f"Timeout occurred while fetching URL: {link}")
       except requests.exceptions.RequestException as e:
             print(f"Error fetching URL: {link}. Exception: {e}") 
     '''

     print(len(links))    

     print(size)
     return links      


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('HTML with PyQt5')
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)


        

        # Set window size and position
        

        # Create a QWebEngineView to host the HTML file
        self.webview = QWebEngineView()

        # Load the external HTML file
        self.webview.setUrl(QUrl.fromLocalFile(html_file_path))

        # Set up communication between HTML and Python
        self.backend = Backend()
        self.web_channel = QWebChannel()
        self.web_channel.registerObject('backend', self.backend)
        self.webview.page().setWebChannel(self.web_channel)

        # Add the webview to the layout
        self.layout.addWidget(self.webview)

        # Set the central widget
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
   
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
