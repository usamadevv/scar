   def pythonFunction(self,querystr):
          
           print('pythonasdsa')
           query = f'"{querystr}"'' "NC" -intitle:"profiles" -inurl:"dir/ " "@gmail.com"'
           links = [] # Initiate empty list to capture final results
            # Specify number of pages on google search, each page contains 10 #links
           n_pages = 5
           chrome_options = webdriver.ChromeOptions()
           chrome_options.add_argument("--headless")    
           driver = webdriver.Chrome()
           headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}
# Get the absolute path of the directory containing the script
           
           for page in range(1, n_pages):
                url = "http://www.google.com/search?q=" + query + "&start=" +      str((page - 1) * 10)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                 # soup = BeautifulSoup(r.text, 'html.parser')

                search = soup.find_all('div', class_="VwiC3b")
                searc2 = soup.find_all('div', class_="yuRUbf")

                searc3 = soup.find_all('h3', class_="LC20lb")
                print(search)
                for index,h in enumerate(search):
                         print(index)
                         print(search[index])
                         links.append({"meta":h.find('span').text,"link":searc2[index].a.get('href'),"title":searc3[index].text,"Email":extract_first_gmail_address(h.find('span').text)})

           for link in links:
               print(link)
           print(links) 
           return  links
