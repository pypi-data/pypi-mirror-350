#!/usr/bin/env python3

import requests # type: ignore
import sys
import socks # type: ignore
import socket
import time
import random
from urllib.parse import quote_plus, urlparse, quote, urlencode, parse_qsl
from bs4 import BeautifulSoup # type: ignore

class TorSearcher:
    """Class for searching through Tor network."""
    
    def __init__(self):
        """Initialize the TorSearcher without connecting."""
        self.connected = False
        self.original_socket = None
    
    def connect(self):
        """Connect to the Tor network."""
        if self.connected:
            return True
            
        # Save the original socket implementation
        self.original_socket = socket.socket
        
        # Try common Tor ports
        ports = [9050, 9150]
        for port in ports:
            try:
                print(f"Trying to connect to Tor on port {port}...")
                socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", port)
                socket.socket = socks.socksocket
                
                # Verify Tor connection
                response = requests.get("https://check.torproject.org/", timeout=30)
                if "Congratulations. This browser is configured to use Tor." in response.text:
                    print(f"Successfully connected to Tor on port {port}")
                    self.connected = True
                    return True
            except Exception as e:
                print(f"Failed to connect on port {port}: {e}")
                socket.socket = self.original_socket
        
        print("Could not connect to Tor network")
        return False
    
    def disconnect(self):
        """Disconnect from Tor network and restore original socket."""
        if self.original_socket:
            socket.socket = self.original_socket
            self.connected = False
            print("Disconnected from Tor network")
    
    def get_random_user_agent(self):
        """Return a random user agent string to avoid detection."""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
        ]
        return random.choice(user_agents)
    
    def search(self, query, num_results=10, engine="duckduckgo"):
        """
        Perform a search through the specified engine.
        
        Args:
            query (str): Search query
            num_results (int): Maximum number of results to return
            engine (str): Search engine to use ("google", "duckduckgo", or "yandex")
            
        Returns:
            list: List of search results
        """
        if not self.connected:
            if not self.connect():
                return []
                
        print(f"Performing search on {engine}...")
        
        if engine.lower() == "google":
            results = self._google_search(query, num_results)
        elif engine.lower() == "yandex":
            results = self._yandex_search(query, num_results)
        else:  # Default to DuckDuckGo
            results = self._duckduckgo_search(query, num_results)
            
        return results
    
    def filter_urls(self, urls):
        """Filter out problematic URLs like ad redirects and overly complex URLs."""
        filtered_urls = []
        for url in urls:
            # Skip ad links which often cause issues
            if any(pattern in url for pattern in ['/y.js?ad_', 'aclick?', '/aclk?']):
                continue
            # Skip URLs with excessive parameters or length
            if len(url) > 500:
                continue
            filtered_urls.append(url)
        return filtered_urls
    
    def prepare_url(self, url):
        """Properly encode URL components to prevent malformed requests."""
        # Parse the URL
        parsed = urlparse(url)
        
        try:
            # Properly encode path
            path = quote(parsed.path)
            
            # Properly encode query parameters
            if parsed.query:
                try:
                    query_params = parse_qsl(parsed.query, keep_blank_values=True)
                    query = urlencode(query_params)
                except Exception:
                    # If parsing fails, use the original query
                    query = parsed.query
            else:
                query = ""
            
            # Reassemble the URL with proper encoding
            cleaned_url = f"{parsed.scheme}://{parsed.netloc}{path}"
            if query:
                cleaned_url += f"?{query}"
                
            return cleaned_url
        except Exception:
            # If any error occurs, return the original URL
            return url
    
    def request_with_retry(self, url, headers, max_retries=3):
        """Make a request with retry logic and exponential backoff."""
        cleaned_url = self.prepare_url(url)
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                
                response = requests.get(cleaned_url, headers=headers, timeout=30)
                return response
                
            except Exception as e:
                print(f"Attempt {attempt+1} failed for {url}: {str(e)}")
                if attempt == max_retries - 1:
                    # Last attempt failed
                    print(f"All {max_retries} attempts failed for {url}")
                    raise
        return None
    
    def _duckduckgo_search(self, query, num_results=10):
        """Perform a DuckDuckGo search."""
        encoded_query = quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            time.sleep(random.uniform(1, 3))
            response = self.request_with_retry(url, headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = []
                for result in soup.select('.result'):
                    title_elem = result.select_one('.result__title a')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    
                    # Get the real URL (DuckDuckGo uses redirects)
                    link = title_elem.get('href')
                    if '/redirect/' in link and 'uddg=' in link:
                        import urllib.parse
                        link = urllib.parse.unquote(link.split('uddg=')[1].split('&')[0])
                    
                    # Filter out problematic ad URLs
                    if any(pattern in link for pattern in ['/y.js?ad_', 'aclick?', '/aclk?']):
                        continue
                        
                    # Skip overly long URLs
                    if len(link) > 500:
                        continue
                    
                    snippet_elem = result.select_one('.result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                    
                    if len(results) >= num_results:
                        break
                        
                return results
            else:
                print(f"Error: DuckDuckGo returned status code {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error performing DuckDuckGo search: {e}")
            return []

    def _google_search(self, query, num_results=10):
        """Perform a Google search."""
        encoded_query = quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
        
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }
        
        try:
            response = self.request_with_retry(url, headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = []
                for result_div in soup.find_all('div', class_='tF2Cxc'):
                    title_elem = result_div.find('h3')
                    link_elem = result_div.find('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.text
                        link = link_elem['href']
                        
                        # Filter problematic URLs
                        if any(pattern in link for pattern in ['/y.js?ad_', 'aclick?', '/aclk?']):
                            continue
                            
                        # Skip overly long URLs
                        if len(link) > 500:
                            continue
                        
                        results.append({
                            'title': title,
                            'link': link
                        })
                        
                        if len(results) >= num_results:
                            break
                            
                return results
            else:
                print(f"Error: Google returned status code {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error performing Google search: {e}")
            return []

    def _yandex_search(self, query, num_results=10):
        """Perform a Yandex search."""
        encoded_query = quote_plus(query)
        urls = [
            f"https://yandex.com/search/?text={encoded_query}",
            f"https://yandex.ru/search/?text={encoded_query}"
        ]
        
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        for url in urls:
            try:
                time.sleep(random.uniform(1, 3))
                
                print(f"Trying Yandex search URL: {url}")
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    print(f"Received 200 OK from Yandex, parsing results...")
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    if "captcha" in response.text.lower() or soup.select_one('form.captcha'):
                        print("Yandex showing CAPTCHA page - Tor exit node may be blocked")
                        continue
                    
                    results = []
                    selectors = ['li.serp-item', '.serp-item', '.organic', '.search-result', '.g-card']
                    items = []
                    
                    for selector in selectors:
                        items = soup.select(selector)
                        if items:
                            print(f"Found {len(items)} potential results using selector '{selector}'")
                            break
                    
                    if not items:
                        print("Could not locate search results in Yandex response")
                        continue
                    
                    for result in items:
                        title_selectors = ['h2 a', '.organic__title-wrapper a', '.title a', '.OrganicTitle a']
                        title_elem = None
                        
                        for title_selector in title_selectors:
                            title_elem = result.select_one(title_selector)
                            if title_elem:
                                break
                                
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href')
                        
                        if not link.startswith('http'):
                            if '?' in link and 'url=' in link:
                                import urllib.parse
                                link = urllib.parse.unquote(link.split('url=')[1].split('&')[0])
                            elif '/r.search' in link or '/goto/' in link:
                                import urllib.parse
                                query_params = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
                                if 'text' in query_params:
                                    link = query_params['text'][0]
                        
                        snippet = ""
                        snippet_selectors = ['.text-container', '.organic__content', '.snippet', 
                                            '.organic__text', '.extended-text']
                        
                        for snippet_selector in snippet_selectors:
                            snippet_elem = result.select_one(snippet_selector)
                            if snippet_elem:
                                snippet = snippet_elem.get_text(strip=True)
                                break
                        
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
                        
                        if len(results) >= num_results:
                            break
                            
                    if results:
                        print(f"Successfully extracted {len(results)} results from Yandex")
                        return results
                else:
                    print(f"Error: Yandex returned status code {response.status_code}")
                        
            except Exception as e:
                print(f"Error performing Yandex search: {e}")
        
        print("All attempts to search Yandex failed")
        return []