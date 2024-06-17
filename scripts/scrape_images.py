import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse
import urllib.robotparser

def get_soup(url):
    """Fetches the content from the URL and returns a BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return BeautifulSoup(response.content, 'html.parser')

def get_image_urls(soup, base_url):
    """Extracts all image URLs from the BeautifulSoup object."""
    img_urls = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        img_url = urljoin(base_url, img_url)  # Handle relative URLs
        if is_valid_url(img_url):
            img_urls.append(img_url)
    return img_urls

def is_valid_url(url):
    """Checks if the URL is valid."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def download_image(url, folder_path):
    """Downloads the image from the URL to the specified folder."""
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_name = os.path.join(folder_path, os.path.basename(urlparse(url).path))
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

def is_scraping_allowed(base_url, user_agent='*'):
    """Checks if scraping is allowed on the website by reading its robots.txt file."""
    parsed_url = urlparse(base_url)
    robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", "/robots.txt")
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch(user_agent, base_url)
    except Exception as e:
        print(f"Could not fetch robots.txt: {e}")
        return False

def scrape_images(base_url, folder_path, delay=1.0):
    """Main function to scrape and download images from a website."""
    if not is_scraping_allowed(base_url):
        print(f"Scraping not allowed on {base_url}")
        return
    try:
        soup = get_soup(base_url)
        img_urls = get_image_urls(soup, base_url)
        for img_url in img_urls:
            download_image(img_url, folder_path)
            time.sleep(delay)  # Respect rate limits by delaying requests
    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")

if __name__ == "__main__":
    # Example usage
    website_url = 'https://www.shutterstock.com/search/granny-smith?image_type=photo'
    output_folder = '/content/drive/MyDrive/Colab Notebooks/scrape_images/apples/granny_smith'
    scrape_images(website_url, output_folder, delay=1.0)
