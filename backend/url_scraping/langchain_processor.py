from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import hashlib
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

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
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10, verify=True)
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

    def process_urls(self, urls):
        """Process URLs and store content in text files"""
        documents = []
        
        for url in urls:
            if not self.is_valid_url(url):
                print(f"Skipping invalid URL: {url}")
                continue

            try:
                # Extract and store content
                content = self.extract_content(url)
                if not content:
                    continue

                # Create safe filename and save content
                filename = self.sanitize_filename(url)
                filepath = os.path.join(self.content_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.url_content_map[url] = filepath
                
                # Process for vector store
                loader = WebBaseLoader(url)
                documents.extend(loader.load())
                
            except Exception as e:
                print(f"Error processing {url}: {e}")

        if documents:
            splits = self.text_splitter.split_documents(documents)
            self.vector_store = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory="./chroma_db"
            )

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