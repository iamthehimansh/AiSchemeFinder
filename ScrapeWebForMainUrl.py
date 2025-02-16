import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_pdf_urls(url):
    try:
        # Send GET request to the URL with SSL verification disabled
        response = requests.get(url, verify=False)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links in the page
        links = soup.find_all('a')
        
        pdf_urls = []
        for link in links:
            href = link.get('href')
            if href:
                # Make URL absolute if it's relative
                full_url = urljoin(url, href)
                
                # Check if URL contains 'pdf' or if the link text contains 'pdf'
                if ('pdf' in full_url.lower() or 
                    (link.text and 'pdf' in link.text.lower())):
                    pdf_urls.append(full_url)
        
        return pdf_urls
    
    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage
if __name__ == "__main__":
    target_url = "https://centralvista.gov.in/"  
    pdf_links = find_pdf_urls(target_url)
    
    print("Found PDF URLs:")
    for url in pdf_links:
        print(url)