# Update these imports
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import hashlib
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import time

load_dotenv()

class BrowseIQProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.llm = ChatOpenAI(temperature=0.7)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.vector_store = None
        self.url_content_map = {}
        self.content_dir = "url_contents"
        
        # Create content directory if it doesn't exist
        if not os.path.exists(self.content_dir):
            os.makedirs(self.content_dir)

    def is_valid_url(self, url: str) -> bool:
        """Validate URL format and scheme"""
        try:
            result = urlparse(url)
            return all([result.scheme in ['http', 'https'], result.netloc])
        except:
            return False

    def sanitize_filename(self, url: str) -> str:
        """Create a safe filename from URL"""
        # Create a hash of the URL for a unique, safe filename
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
        return f"url_content_{url_hash}.txt"

    def extract_content(self, url: str) -> str:
        """Safely extract content from URL with error handling"""
        # First try our standalone function for Google searches
        from urllib.parse import parse_qs, urlparse
        if 'google.com/search' in url or 'google.com?q=' in url:
            try:
                parsed = urlparse(url)
                params = parse_qs(parsed.query)
                if 'q' in params:
                    search_terms = params['q'][0]
                    print(f"Detected Google search, returning terms: {search_terms}")
                    return f"Google search: {search_terms}"
            except Exception as e:
                print(f"Error parsing Google URL: {e}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
            
            # Follow redirects and get final URL
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=15, verify=True, allow_redirects=True)
            
            # Check if this is a search engine result page
            if 'google.com/search' in response.url:
                # Extract actual result links from search page
                soup = BeautifulSoup(response.text, 'html.parser')
                result_links = [a['href'] for a in soup.select('a[href^="/url?"]') 
                              if 'url=' in a['href']]
                
                if result_links:
                    # Get content from first result
                    first_result = result_links[0].split('url=')[1].split('&')[0]
                    response = session.get(first_result, headers=headers, timeout=15, verify=True)
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up text
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            return '\n'.join(lines)
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return ""

    def process_urls(self, urls, batch_size=5, delay_seconds=1):
        """Process URLs and store content in text files"""
        documents = []
        
        for i, url in enumerate(urls):
            if not self.is_valid_url(url):
                continue
                
            try:
                content = self.extract_content(url)
                if not content:
                    print(f"Skipping {url} - no content available")
                    continue
                
                # Save content to file
                filename = self.sanitize_filename(url)
                filepath = os.path.join(self.content_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.url_content_map[url] = filepath
                
                # Process for vector store in batches
                loader = WebBaseLoader(url)
                documents.extend(loader.load())
                
                # Process batch and add delay
                if (i+1) % batch_size == 0 or i == len(urls)-1:
                    if documents:
                        splits = self.text_splitter.split_documents(documents)
                        self.vector_store = Chroma.from_documents(
                            documents=splits,
                            embedding=self.embeddings,
                            persist_directory="./chroma_db"
                        )
                        documents = []  # Reset for next batch
                        time.sleep(delay_seconds)  # Add delay between batches
            
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue

    def get_url_content(self, url: str) -> str:
        """Safely retrieve content for a URL"""
        if url in self.url_content_map and os.path.exists(self.url_content_map[url]):
            try:
                with open(self.url_content_map[url], 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading content file for {url}: {e}")
        return ""

    def create_rag_chain(self):
        """Create a RAG chain for querying the processed content"""
        if not self.vector_store:
            raise ValueError("No documents have been processed yet")

        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

    def query(self, question: str):
        """Query the RAG chain with a question"""
        chain = self.create_rag_chain()
        return chain({"question": question})
    