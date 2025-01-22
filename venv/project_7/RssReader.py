import os
import feedparser
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Function to extract and save content from a single URL
def fetch_and_save_content(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the text content from the webpage
        content = soup.get_text(separator='\n', strip=True)

        folder_path = os.path.join(os.path.dirname(__file__))
        output_filename = f"output.txt"
        output_path = os.path.join(folder_path, output_filename)

        print(f"output file : "+output_path)
        # Write content to the output file
        with open(output_path, "a", encoding="utf-8") as file:
            file.write(f"URL: {link}\n")
            file.write(content)
            file.write("\n\n")
    except Exception as e:
        print(f"Error fetching {link}: {e}")

# Function to parse RSS and process links
def process_rss(rss_url):
    try:
        # Parse the RSS feed
        feed = feedparser.parse(rss_url)
        links = [entry.link for entry in feed.entries]

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            executor.map(fetch_and_save_content, links)

        print("Content extraction complete. Results saved to output.txt.")
    except Exception as e:
        print(f"Error processing RSS feed: {e}")

if __name__ == "__main__":
    # Example RSS URL
    rss_feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
    process_rss(rss_feed_url)
