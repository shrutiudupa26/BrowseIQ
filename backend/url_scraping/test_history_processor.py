import unittest
import os
from history_processor import process_history_urls
from langchain_processor import BrowseIQProcessor

class TestHistoryProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = BrowseIQProcessor()
    
    def test_process_history_urls(self):
        # Process URLs
        url_content_dict = process_history_urls()
        
        # Check if dictionary is not empty
        self.assertTrue(len(url_content_dict) > 0)
        
        # Check if files exist
        for url, filepath in url_content_dict.items():
            self.assertTrue(os.path.exists(filepath))
            
            # Check if files have content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertTrue(len(content) > 0)
    
    def tearDown(self):
        # Clean up test files
        for filepath in self.processor.url_content_map.values():
            if os.path.exists(filepath):
                os.remove(filepath)
        if os.path.exists(self.processor.content_dir):
            os.rmdir(self.processor.content_dir)

if __name__ == '__main__':
    unittest.main()