import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

global parsed_url 
global unparsed_url 
parsed_url = set()
unparsed_url = set()

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_page_content(url, wait_time=5):
    driver = setup_driver()
    driver.get(url)
    time.sleep(wait_time)
    page_source = driver.page_source
    driver.quit()
    return page_source

def parse_url(url, save_links = True):
    global parsed_url 
    global unparsed_url 

    try:
        print(f"worning on {url}")
        if url not in parsed_url:
            html_content = get_page_content(url)
            parse_text_content(html_content, url)
            links = get_all_links_from_page(html_content)
            print("links",links)
            if save_links: 
                for link in links:
                    if link.startswith('http') | link.startswith('https'):
                        unparsed_url.update([link])
    except Exception as e:
        print(f"An error occurred: {e}")

    
def get_all_links_from_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Example: Extract all links
    links = soup.find_all("a")
    links_href = [a.get('href') for a in links]
    return links_href

def parse_text_content(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Example: Extract main body
    main = soup.find_all("main")
    main_text = ""
    for el in main:
        main_text += el.get_text()
    
    #save to file
    write_info_to_file(url, main_text)

def write_info_to_file(url,text): 
    global parsed_url 
    file_name = url[8:].replace("/", "_")
    with open(f'parsed_info\{file_name}.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    parsed_url.update(url)
    
    

def main():
    
    global unparsed_url 
    starting_url = "https://www.gov.pl/web/gov/uslugi-dla-obywatela"  # Replace with the actual URL
    parse_url(starting_url)

    #second layer
    print("unparsed_url",unparsed_url)  
    second_layer = unparsed_url.copy()
    for link in second_layer:
        parse_url(link)
    
    #final layer
    final_layer = unparsed_url.copy()
    for link in final_layer:
        parse_url(link, False)



    #links = get_all_links_from_page(starting_url, all_links)[:5]
    #print(len(links))
    #all_links = set(links)
    #for link in links:
        #if link.startswith('http'):
            #all_links.update(get_all_links_from_page(link, all_links)[:5])
    #print(all_links)
    #parsed_data = parse_text_content(content)
    
    # Print or process the parsed data
    #for item in parsed_data:
        #href = item.get('href')
        #print(href)

if __name__ == "__main__":
    main()