import pandas as pd
from flask import Flask, request, jsonify
from langchain_processor import BrowseIQProcessor
from keyword_extractor import KeywordExtractor

app = Flask(__name__)
processor = BrowseIQProcessor()
keyword_extractor = KeywordExtractor()

@app.route('/api/history', methods=['POST'])
def receive_history():
    history_data = request.json
    
    # Convert to DataFrame
    history_df = pd.DataFrame(history_data)
    
    # Get unique URLs
    unique_urls = history_df['url'].unique()
    
    # Process URLs using the existing processor
    processor.process_urls(unique_urls)
    
    # Extract keywords for each URL
    url_keywords = keyword_extractor.process_url_contents(processor)
    
    return jsonify({
        'status': 'success',
        'processed_urls': len(unique_urls),
        'url_keywords': url_keywords
    })

if __name__ == '__main__':
    app.run(port=5000)