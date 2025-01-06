import requests
from bs4 import BeautifulSoup
import time

def get_content_type(url):
    """
    Categorize the content type based on the URL.
    """
    if "pdf" in url.lower():
        return "PDF"
    elif "books.google.com" in url:
        return "Book"
    elif "youtube.com" in url:
        return "Video"
    elif "arxiv.org" in url:
        return "Research Paper"
    else:
        return "Article"

def summarize_article(url, sentences_count=3):
    """
    Summarize the content of an article by extracting the first few sentences.
    """
    try:
        print(f"Summarizing article: {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = " ".join(p.text for p in soup.find_all('p'))  # Extract all paragraphs
        if not text:
            print(f"No content found for {url}")
            return None
        sentences = text.split(". ")  # Split into sentences
        summary = ". ".join(sentences[:sentences_count])  # Take the first few sentences
        return summary
    except Exception as e:
        print(f"Summarization error for {url}: {e}")
        return None

def google_search(query):
    try:
        print("Searching Google...")
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='tF2Cxc'):
            title_element = result.find('h3')
            link_element = result.find('a')
            if title_element and link_element:
                title = title_element.text.strip()
                link = link_element['href']
                domain = link.split('/')[2]
                content_type = get_content_type(link)
                results.append({"title": title, "link": link, "source": domain, "type": content_type})
        print(f"Google results: {len(results)}")
        return results
    except Exception as e:
        print(f"Google search error: {e}")
        return []

def bing_search(query):
    try:
        print("Searching Bing...")
        url = f"https://www.bing.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('li', class_='b_algo'):
            title_element = result.find('h2')
            link_element = result.find('a')
            if title_element and link_element:
                title = title_element.text
                link = link_element['href']
                domain = link.split('/')[2]
                content_type = get_content_type(link)
                results.append({"title": title, "link": link, "source": domain, "type": content_type})
        print(f"Bing results: {len(results)}")
        return results
    except Exception as e:
        print(f"Bing search error: {e}")
        return []

def duckduckgo_search(query):
    try:
        print("Searching DuckDuckGo...")
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='result'):
            title_element = result.find('h2')
            link_element = result.find('a', class_='result__url')
            if title_element and link_element:
                title = title_element.text
                link = link_element['href']
                domain = link.split('/')[2]
                content_type = get_content_type(link)
                results.append({"title": title, "link": link, "source": domain, "type": content_type})
        print(f"DuckDuckGo results: {len(results)}")
        return results
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return []

def pubmed_search(query):
    try:
        print("Searching PubMed...")
        url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='docsum-content'):
            title_element = result.find('a', class_='docsum-title')
            link_element = result.find('a', class_='docsum-title')
            if title_element and link_element:
                title = title_element.text.strip()
                link = "https://pubmed.ncbi.nlm.nih.gov" + link_element['href']
                content_type = get_content_type(link)
                results.append({"title": title, "link": link, "source": "PubMed", "type": content_type})
        print(f"PubMed results: {len(results)}")
        return results
    except Exception as e:
        print(f"PubMed search error: {e}")
        return []

def google_scholar_search(query):
    try:
        print("Searching Google Scholar...")
        url = f"https://scholar.google.com/scholar?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='gs_ri'):
            title_element = result.find('h3', class_='gs_rt')
            link_element = result.find('a')
            if title_element and link_element:
                title = title_element.text
                link = link_element['href']
                content_type = get_content_type(link)
                results.append({"title": title, "link": link, "source": "Google Scholar", "type": content_type})
        print(f"Google Scholar results: {len(results)}")
        return results
    except Exception as e:
        print(f"Google Scholar search error: {e}")
        return []

def arxiv_search(query):
    try:
        print("Searching arXiv...")
        url = f"https://arxiv.org/search/?query={query}&searchtype=all&source=header"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('li', class_='arxiv-result'):
            title_element = result.find('p', class_='title')
            link_element = result.find('a', title='Abstract')
            if title_element and link_element:
                title = title_element.text.strip()
                link = "https://arxiv.org" + link_element['href']
                content_type = get_content_type(link)
                results.append({"title": title, "link": link, "source": "arXiv", "type": content_type})
        print(f"arXiv results: {len(results)}")
        return results
    except Exception as e:
        print(f"arXiv search error: {e}")
        return []

def multi_search(query):
    """
    Perform a search across multiple search engines and combine the results.
    """
    print("Starting multi-search...")
    # Get results from all search engines
    google_results = google_search(query)
    time.sleep(2)  # Add a delay to avoid being blocked
    bing_results = bing_search(query)
    time.sleep(2)  # Add a delay to avoid being blocked
    duckduckgo_results = duckduckgo_search(query)
    time.sleep(2)
    pubmed_results = pubmed_search(query)
    time.sleep(2)
    scholar_results = google_scholar_search(query)
    time.sleep(2)
    arxiv_results = arxiv_search(query)

    # Combine results
    all_results = google_results + bing_results + duckduckgo_results + pubmed_results + scholar_results + arxiv_results
    print(f"Total results before deduplication: {len(all_results)}")

    # Remove duplicates based on the link
    unique_results = []
    seen_links = set()
    for result in all_results:
        if result["link"] not in seen_links:
            unique_results.append(result)
            seen_links.add(result["link"])

    # Sort results by source
    sorted_results = sorted(unique_results, key=lambda x: x["source"])
    print(f"Total unique results: {len(sorted_results)}")
    return sorted_results