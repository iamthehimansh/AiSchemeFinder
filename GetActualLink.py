import requests
import json
from bs4 import BeautifulSoup
import threading
from queue import Queue
BASE_URL = "https://www.india.gov.in"
links = json.load(open("links.json", "r"))
actual_links = []
link_lock = threading.Lock()

def process_link(link, results_queue):
    try:
        response = requests.get(BASE_URL + link)
        soup = BeautifulSoup(response.text, 'html.parser')
        # find frist element with class "field-content"
        element = soup.find('h3', class_='field-content')
        if element:
            # find all anchor tags inside the element
            anchor_tags = element.find_all('a')
            # extract the href attribute from each anchor tag
            for tag in anchor_tags:
                href = tag.get('href')
                print(href)
                if href:
                    results_queue.put(href)
        print(f"Done {href}")
    except Exception as e:
        print(f"Error processing {link}: {str(e)}")

# Create a queue to store results
results_queue = Queue()

# Create and start threads
threads = []
batch_size = 10  # Number of concurrent threads
for i in range(0, len(links), batch_size):
    batch = links[i:i + batch_size]
    thread_batch = []
    for link in batch:
        print(f"Processing {link}")
        thread = threading.Thread(target=process_link, args=(link, results_queue))
        thread.start()
        thread_batch.append(thread)
    
    # Wait for all threads in this batch to complete
    for thread in thread_batch:
        thread.join()

# Collect all results from the queue
while not results_queue.empty():
    actual_links.append(results_queue.get())

json.dump(actual_links, open("actual_links.json", "w"))


# BASE_URL="https://www.india.gov.in"
# links=json.load(open("links.json","r"))
# actual_links=[]
# for link in links:
#     print(link)
#     response = requests.get(BASE_URL + link)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # find frist element with class "field-content"
#     element = soup.find('h3', class_='field-content')
#     # find all anchor tags inside the element
#     anchor_tags = element.find_all('a')
#     # extract the href attribute from each anchor tag
#     for tag in anchor_tags:
#         href = tag.get('href')
#         print(href)
#         if href:
#             actual_links.append(href)