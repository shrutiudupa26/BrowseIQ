import pandas as pd
import json
import os
from flask import Flask, request, jsonify
from langchain_processor import BrowseIQProcessor
from keyword_extractor import KeywordExtractor
from datetime import datetime

app = Flask(__name__)
processor = BrowseIQProcessor() # This processor handles content extraction and saving to .txt
keyword_extractor = KeywordExtractor()

# Define the directory to save JSON files
OUTPUT_DIR = 'processed_history'

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/api/history', methods=['POST'])
def receive_history():
    history_data = request.json
    processor = BrowseIQProcessor()
    
    # Process URLs and get content
    processor.process_urls([entry['url'] for entry in history_data])
    
    # Group history by URL and filter out entries with no content
    url_data = {}
    for entry in history_data:
        url = entry['url']
        content = processor.get_url_content(url)
        
        # Skip URLs with no content
        if not content:
            print(f"Skipping {url} - no content available")
            continue
            
        if url not in url_data:
            url_data[url] = {
                'url': url,
                'timestamp': datetime.fromtimestamp(entry['lastVisitTime']/1000).isoformat() + 'Z',
                'no_of_visits': 1,
                'content': content
            }
        else:
            url_data[url]['no_of_visits'] += 1
            # Keep the most recent timestamp
            current_timestamp = datetime.fromtimestamp(entry['lastVisitTime']/1000).isoformat() + 'Z'
            if current_timestamp > url_data[url]['timestamp']:
                url_data[url]['timestamp'] = current_timestamp
    
    # Convert to list and sort by timestamp
    processed_history = sorted(url_data.values(), key=lambda x: x['timestamp'], reverse=True)
    
    # Save to JSON file
    output_path = os.path.join('processed_history', 'history_output.json')
    os.makedirs('processed_history', exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(processed_history, f, indent=2)
    
    print(f"Saved processed history to {os.path.abspath(output_path)}")
    
    return jsonify(processed_history)

if __name__ == '__main__':
    app.run(port=5000)