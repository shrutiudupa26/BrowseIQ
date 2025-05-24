import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
import string
from langchain_processor import BrowseIQProcessor

class KeywordExtractor:
    def __init__(self):
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Initialize stopwords and common words to exclude
        self.stop_words = set(stopwords.words('english'))
        self.common_words = {
            'use', 'using', 'used', 'like', 'may', 'also', 'one', 'two', 'first',
            'new', 'click', 'get', 'see', 'help', 'make', 'can', 'please', 'many',
            'copyright', 'rights', 'reserved', 'privacy', 'policy', 'terms'
        }
        self.stop_words.update(self.common_words)

    def clean_text(self, text):
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text

    def extract_keywords(self, text, top_n=10):
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = word_tokenize(cleaned_text)
        
        # Remove stopwords and common words, and filter out short words
        keywords = [word for word in tokens 
                   if word not in self.stop_words 
                   and len(word) > 2 
                   and word.isalnum()]
        
        # Get frequency distribution
        fdist = FreqDist(keywords)
        
        # Get top N most common keywords
        top_keywords = [word for word, _ in fdist.most_common(top_n)]
        
        return top_keywords

    def process_url_contents(self, processor):
        # Create a new dictionary for URL keywords
        url_keywords = {}
        
        # Process each URL in the content map
        for url, filepath in processor.url_content_map.items():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract top keywords for this content
                keywords = self.extract_keywords(content)
                url_keywords[url] = keywords
            except Exception as e:
                print(f"Error processing {url}: {e}")
                url_keywords[url] = []
        
        return url_keywords

def main():
    # Initialize the processors
    browse_processor = BrowseIQProcessor()
    keyword_extractor = KeywordExtractor()
    
    # Example usage
    urls = ["https://example.com"]  # Add your URLs here
    browse_processor.process_urls(urls)
    
    # Get keywords for all processed URLs
    url_keywords = keyword_extractor.process_url_contents(browse_processor)
    
    # Print results
    for url, keywords in url_keywords.items():
        print(f"\nURL: {url}")
        print(f"Top Keywords: {', '.join(keywords)}")

if __name__ == '__main__':
    main()