import requests
import json
from bs4 import BeautifulSoup
import threading
from tqdm import tqdm
import urllib3
import concurrent.futures
BASE_URL=""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# links=["https://centralvista.gov.in/"]

links = json.load(open("actual_links.json", "r"))
print(f"Total links: {len(links)}")

# Thread-safe counter for progress tracking
processed_count = 0
counter_lock = threading.Lock()

def download_pdf(link):
    try:
        response = requests.get(link, stream=True)
        if response.status_code == 200:
            with open("data/"+link.split('/')[-1], 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return f"Downloaded {link}"
        else:
            return f"Failed to download {link}"
    except Exception as e:
        return f"Error downloading {link}: {str(e)}"

def process_link(link):
    global processed_count
    
    if link.endswith(".pdf"):
        result = download_pdf(link)
        with counter_lock:
            processed_count += 1
        return result

    try:
        # Make request to get the page content
        response = requests.get(BASE_URL + link, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        contents = ["URL: "+BASE_URL + link+soup.get_text(separator=' ', strip=True)]
        nav_links = soup.find_all('nav')
        li_links = soup.find_all('li')
        
        # Process sublinks in batches
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for link_element in [*nav_links, *li_links]:
                anchor_tags = link_element.find_all('a')
                for a in anchor_tags:
                    href = a.get('href')
                    
                    if href:
                        if href.startswith('/'):
                            full_url = BASE_URL + href
                        elif href.startswith('http'):
                            full_url = href
                        else:
                            continue
                            
                        futures.append(executor.submit(fetch_subpage, full_url))
            
            # Collect results from futures
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    contents.append(result)

        # Write collected content to file
        with open("data/"+link.replace("/", "_").replace("https:","").replace("http:","")+".txt", "w") as f:
            f.write("\n______+++++++_______\n".join(contents))
        
        with counter_lock:
            processed_count += 1
            
        return f"Processed {link}"

    except Exception as e:
        with counter_lock:
            processed_count += 1
        return f"Error processing {link}: {str(e)}"

def fetch_subpage(full_url):
    try:
        response = requests.get(full_url, verify=False)
        soup2 = BeautifulSoup(response.text, 'html.parser')
        page_text = soup2.get_text(separator=' ', strip=True)
        if page_text:
            return "URL: "+full_url+page_text
    except requests.RequestException:
        return None

# Process all links in parallel with progress bar
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_link, link) for link in links]
    
    with tqdm(total=len(links), desc="Processing links") as pbar:
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)
            pbar.update(1)
