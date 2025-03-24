from newspaper import Article
from utils import get_final_url

class News:
    def __init__(self, title, link, published, mainText=None):
        self.title = title
        self.link = get_final_url(link)  # Get the actual article URL
        self.published = published
        self.mainText = self._getMainText(self.link) if mainText is None else mainText

    def __eq__(self, other):
        return self.link == other.link
    
    def __hash__(self):
        return hash(self.link)
    
    def __str__(self):
        return f"{self.title}\n{self.published}\n\n{self.mainText}"
    
    def _getMainText(self, link):
        """
        Extract the main article text from a webpage.
        Returns the extracted text or an error message if extraction fails.
        """
        try:
            # Create Article object
            article = Article(link)
            
            # Download and parse article
            article.download()
            article.parse()
            
            # Get the full text
            full_text = article.text
            # Optionally, you can also get other metadata
            title = article.title
            self.title = title if self.title is None else self.title
            publish_date = article.publish_date
            self.published = publish_date.strftime('%Y-%m-%d %H:%M:%S') if self.published is None else self.published
            
            return full_text
        
        except Exception as e:
            print(f"Error extracting article content: {str(e)}")
            return None

        
        # Recursively find all paragraph elements in the tree
        # def find_all_paragraphs(element):
        #     paragraphs = []
        #     # Base case: if element is a paragraph, add its text
        #     if element.name == 'p':
        #         text = element.get_text().strip()
        #         if text:
        #             paragraphs.append(text)
        #     # Recursive case: traverse children
        #     for child in element.children:
        #         if hasattr(child, 'children'):  # Only process elements, not text nodes
        #             paragraphs.extend(find_all_paragraphs(child))
        #     return paragraphs
        
        # try:
        #     # Use a modern browser User-Agent
        #     headers = {
        #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        #             'Accept-Language': 'en-US,en;q=0.9',
        #             'Accept-Encoding': 'gzip, deflate, br',
        #             'DNT': '1',
        #             'Connection': 'keep-alive',
        #             'Upgrade-Insecure-Requests': '1',
        #             'Sec-Fetch-Dest': 'document',
        #             'Sec-Fetch-Mode': 'navigate',
        #             'Sec-Fetch-Site': 'none',
        #             'Sec-Fetch-User': '?1',
        #             'Cache-Control': 'max-age=0',
        #             # Adding referer to look more like a real browser click
        #             'Referer': 'https://news.google.com/'
        #         }
            
        #     # Fetch the page with a reasonable timeout
        #     response = requests.get(link, headers=headers, timeout=15)
        #     response.raise_for_status()
            
        #     # Parse with BeautifulSoup
        #     soup = BeautifulSoup(response.text, 'html.parser')
            
        #     # Remove noise elements
        #     for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'iframe', 'aside', 'meta', 'noscript']):
        #         element.decompose()
            
        #     paragraphs = []
        #     # get all elements at the top level of the body
        #     for element in soup.find_all(['div', 'section']):
        #         paragraphs.extend(find_all_paragraphs(element))
            
        #     text = ' '.join(paragraphs)
        #     text = ' '.join(text.split())
            
        #     if not text:
        #         return "No article text found"
                
        #     return text


        #     # First try to find article content in common article containers
        #     main_content = None
        #     for container in ['article', '[role="article"]', 'main', '#main-content', '.article-body', '.post-content']:
        #         main_content = soup.select_one(container)
        #         if main_content and main_content.find_all('p'):
        #             break
            
        #     # If no article container found, use the body
        #     if not main_content or not main_content.find_all('p'):
        #         main_content = soup.body
            
        #     if not main_content:
        #         return "Could not find article content"
            
        #     # Extract text from paragraphs
        #     paragraphs = []
        #     for p in main_content.find_all('p'):
        #         text = p.get_text().strip()
        #         # Only include non-empty paragraphs and filter out common noise
        #         if text and not any(noise in text.lower() for noise in ['advertisement', 'copyright ©', 'all rights reserved']):
        #             paragraphs.append(text)
            
        #     # Join paragraphs and clean up whitespace
        #     text = ' '.join(paragraphs)
        #     text = ' '.join(text.split())
            
        #     if not text:
        #         return "No article text found"
                
        #     return text
            
        # except requests.RequestException as e:
        #     return f"Network error while fetching article: {str(e)}"
        # except Exception as e:
        #     return f"Error extracting article text: {str(e)}" 