import pandas as pd
from langchain_processor import BrowseIQProcessor
from datetime import datetime
import os

class HistoryProcessor:
    def __init__(self):
        self.processor = BrowseIQProcessor()
        self.urls_path = os.path.join('backend', 'data', 'urls.csv')
        self.visits_path = os.path.join('backend', 'data', 'visits.csv')

    def load_history(self):
        """Load and process browser history from CSV files"""
        try:
            # Read URLs from CSV
            urls_df = pd.read_csv(self.urls_path)
            
            # Remove duplicates and filter relevant columns
            unique_urls = urls_df.drop_duplicates(subset=['url'])
            processed_urls = unique_urls[['url', 'title', 'visit_count']]
            
            # Sort by visit count to prioritize frequently visited pages
            processed_urls = processed_urls.sort_values('visit_count', ascending=False)
            
            return processed_urls['url'].tolist(), processed_urls['title'].tolist()
        except Exception as e:
            print(f"Error loading history: {e}")
            return [], []

    def process_history(self):
        """Process browser history through the RAG pipeline"""
        urls, titles = self.load_history()
        if not urls:
            print("No URLs found in history")
            return

        print(f"Processing {len(urls)} unique URLs from browser history...")
        
        # Process URLs through LangChain pipeline
        self.processor.process_urls(urls)
        print("URLs processed and stored in vector database")

    def query_history(self, question: str) -> dict:
        """Query the processed history using the RAG chain"""
        try:
            return self.processor.query(question)
        except Exception as e:
            print(f"Error querying history: {e}")
            return {"answer": "Error processing query", "sources": []}

def main():
    processor = HistoryProcessor()
    processor.process_history()
    
    # Example query
    result = processor.query_history("What are my most frequently visited websites?")
    print("\nQuery Result:")
    print(result['answer'])

if __name__ == "__main__":
    main()