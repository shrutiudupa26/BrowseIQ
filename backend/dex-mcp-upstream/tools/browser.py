"""Browser tools for interacting with the browser extension."""

from typing import Any, Dict
from context import Context
import json
from datetime import datetime
import os
# Add these imports at the top
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string


async def get_tabs_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Get all open browser tabs.
    
    Params: None
    """
    try:
        result = await context.send_socket_message("get_tabs", {})
        
        if not result or "tabs" not in result:
            return "No tabs found or unable to fetch tabs."
        
        tabs = result["tabs"]
        if not tabs:
            return "No open tabs found."
        
        # Format tabs into readable text
        tab_list = []
        for tab in tabs:
            tab_info = f"Tab {tab.get('id', 'Unknown')}: {tab.get('title', 'Untitled')}"
            if tab.get('url'):
                tab_info += f"\n  URL: {tab['url']}"
            tab_list.append(tab_info)
        
        return f"Found {len(tabs)} open tabs:\n\n" + "\n\n".join(tab_list)
        
    except Exception as e:
        return f"Error getting tabs: {str(e)}"


async def screenshot_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Take a screenshot of the active tab.
    
    Params: None
    """
    try:
        result = await context.send_socket_message("screenshot", {})
        
        if not result:
            return "Failed to take screenshot."
        
        if result.get("success"):
            return result
        else:
            return f"Failed to take screenshot: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"


async def navigate_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Navigate to a URL in active tab or specified tab.
    
    Params:
        url (str): Required - URL to navigate to
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "url" not in params:
        return "Error: URL parameter is required"
    
    url = params["url"]
    tab_id = params.get("tab_id")
    
    payload = {"url": url}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("navigate", payload)
        
        if not result:
            return f"Failed to navigate to {url}"
        
        if result.get("success"):
            message = result.get("message", f"Navigated to {url}")
            action = result.get("action", "go_to_url")
            return f"Successfully navigated to {url}\nAction: {action} - {message}"
        else:
            return f"Failed to navigate to {url}: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error navigating to {url}: {str(e)}"


async def select_tab_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Switch to a specific browser tab by ID.
    
    Params:
        tab_id (int): Required - Tab ID to switch to
    """
    if not params or "tab_id" not in params:
        return "Error: tab_id parameter is required"
    
    tab_id = params["tab_id"]
    
    try:
        result = await context.send_socket_message("select_tab", {"tab_id": tab_id})
        
        if not result:
            return f"Failed to select tab {tab_id}"
        
        if result.get("success"):
            message = result.get("message", "Tab selected")
            action = result.get("action", "select_tab")
            return f"Successfully switched to tab {tab_id}\nAction: {action} - {message}"
        else:
            return f"Failed to select tab {tab_id}: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error selecting tab {tab_id}: {str(e)}"


async def new_tab_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Create a new browser tab, optionally with a specific URL.
    
    Params:
        url (str): Optional - URL to open in new tab, defaults to blank tab
    """
    url = params.get("url") if params else None
    
    payload = {}
    if url:
        payload["url"] = url
    
    try:
        result = await context.send_socket_message("new_tab", payload)
        
        if not result:
            return "Failed to create new tab"
        
        if result.get("success"):
            tab_id = result.get("data", {}).get("id")
            message = result.get("message", "New tab created")
            action = result.get("action", "new_tab")
            
            if url:
                return f"Successfully created new tab (ID: {tab_id}) with URL: {url}\nAction: {action} - {message}"
            else:
                return f"Successfully created new tab (ID: {tab_id})\nAction: {action} - {message}"
        else:
            return f"Failed to create new tab: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error creating new tab: {str(e)}"


async def close_tab_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Close a browser tab by ID, or close the active tab if no ID specified.
    
    Params:
        tab_id (int): Optional - Tab ID to close, defaults to active tab
    """
    tab_id = params.get("tab_id") if params else None
    
    payload = {}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("close_tab", payload)
        
        if not result:
            return f"Failed to close tab {tab_id if tab_id else '(active)'}"
        
        if result.get("success"):
            message = result.get("message", "Tab closed")
            action = result.get("action", "close_tab")
            return f"Successfully closed tab {tab_id if tab_id else '(active)'}\nAction: {action} - {message}"
        else:
            return f"Failed to close tab: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error closing tab: {str(e)}"


async def search_google_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Perform a Google search in active tab or specified tab.
    
    Params:
        query (str): Required - Search query text
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "query" not in params:
        return "Error: query parameter is required"
    
    query = params["query"]
    tab_id = params.get("tab_id")
    
    payload = {"query": query}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("search_google", payload)
        
        if not result:
            return f"Failed to search Google for '{query}'"
        
        if result.get("success"):
            message = result.get("message", f"Searched Google for {query}")
            action = result.get("action", "search_google")
            return f"Successfully searched Google for '{query}'\nAction: {action} - {message}"
        else:
            return f"Failed to search Google for '{query}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error searching Google for '{query}': {str(e)}"


async def click_element_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Click on a DOM element by its ID.
    
    Params:
        element_id (str): Required - Element ID to click
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "element_id" not in params:
        return "Error: element_id parameter is required"
    
    element_id = params["element_id"]
    tab_id = params.get("tab_id")
    
    payload = {"element_id": element_id}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("click_element", payload)
        
        if not result:
            return f"Failed to click element '{element_id}'"
        
        if result.get("success"):
            message = result.get("message", f"Clicked element '{element_id}'")
            action = result.get("action", "click_element")
            return f"Successfully clicked element '{element_id}'\nAction: {action} - {message}"
        else:
            return f"Failed to click element '{element_id}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error clicking element '{element_id}': {str(e)}"


async def input_text_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Type text into a DOM element by its ID.
    
    Params:
        element_id (str): Required - Element ID to type into
        text (str): Required - Text to input
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "element_id" not in params or "text" not in params:
        return "Error: element_id and text parameters are required"
    
    element_id = params["element_id"]
    text = params["text"]
    tab_id = params.get("tab_id")
    
    payload = {"element_id": element_id, "text": text}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("input_text", payload)
        
        if not result:
            return f"Failed to input text into element '{element_id}'"
        
        if result.get("success"):
            message = result.get("message", f"Input text into element '{element_id}'")
            action = result.get("action", "input_text")
            return f"Successfully input text '{text}' into element '{element_id}'\nAction: {action} - {message}"
        else:
            return f"Failed to input text into element '{element_id}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error inputting text into element '{element_id}': {str(e)}"


async def send_keys_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Send keyboard shortcuts or key combinations to the page.
    
    Params:
        keys (str): Required - Key combination (e.g. 'Ctrl+C', 'Enter', 'Tab')
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "keys" not in params:
        return "Error: keys parameter is required"
    
    keys = params["keys"]
    tab_id = params.get("tab_id")
    
    payload = {"keys": keys}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("send_keys", payload)
        
        if not result:
            return f"Failed to send keys '{keys}'"
        
        if result.get("success"):
            message = result.get("message", f"Sent keys '{keys}'")
            action = result.get("action", "send_keys")
            return f"Successfully sent keys '{keys}'\nAction: {action} - {message}"
        else:
            return f"Failed to send keys '{keys}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error sending keys '{keys}': {str(e)}"


async def grab_dom_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Get formatted DOM structure with XPath mappings for elements.
    
    Params:
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    tab_id = params.get("tab_id") if params else None
    
    payload = {}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("grab_dom", payload)
        
        if not result:
            return "Failed to grab DOM structure"
        
        if result.get("success"):
            return result
        else:
            return f"Failed to grab DOM: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error grabbing DOM: {str(e)}"


async def capture_with_highlights_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Take a screenshot with element highlights for better AI understanding.
    
    Params:
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    tab_id = params.get("tab_id") if params else None
    
    payload = {}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("capture_with_highlights", payload)
        
        if not result:
            return "Failed to capture screenshot with highlights"
        
        if result.get("success"):
            return result
        else:
            return f"Failed to capture screenshot with highlights: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error capturing screenshot with highlights: {str(e)}"


async def add_assistant_message_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Add an assistant message to the chat.
    
    Params:
        message (str): Required - Message to add to the chat
    """
    if not params or "message" not in params:
        return "Error: message parameter is required"
    
    message = params["message"]
    
    try:
        result = await context.send_socket_message("add_assistant_message", {"message": message})
        
        if not result:
            return f"Failed to add assistant message"
        
        if result.get("success"):
            return f"Successfully added assistant message: {message}"
        else:
            return f"Failed to add assistant message: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error adding assistant message: {str(e)}"


async def query_history_by_date_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Query browsing history for a specific date and return matching items with summaries.
    
    Params:
        date (str): Required - Date in YYYY-MM-DD format or natural language (e.g., "May 22nd, 2025")
    """
    if not params or "date" not in params:
        return "Error: date parameter is required (format: YYYY-MM-DD or natural language like 'May 22nd, 2025')"
    
    date_str = params["date"]
    
    try:
        # Try to convert natural language dates to YYYY-MM-DD format
        date_conversions = {
            "may 22nd, 2025": "2025-05-22",
            "may 23rd, 2025": "2025-05-23", 
            "may 24th, 2025": "2025-05-24",
            "may 21st, 2025": "2025-05-21",
            "may 20th, 2025": "2025-05-20"
        }
        
        # Check if it's a natural language date
        normalized_date = date_str.lower().strip()
        if normalized_date in date_conversions:
            date_str = date_conversions[normalized_date]
        
        # Validate date format
        query_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Load history data from contents.json
        history_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "contents.json")
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        # Filter items for the specified date
        matching_items = []
        for item in history_data:
            item_date = datetime.strptime(item['timestamp'].split('T')[0], '%Y-%m-%d')
            if item_date.date() == query_date.date():
                matching_items.append({
                    'url': item['url'],
                    'timestamp': item['timestamp'],
                    'content': item['content'],
                    'no_of_visits': item['no_of_visits']
                })
        
        if not matching_items:
            return f"No browsing history found for {date_str}"
        
        # Generate summary
        summary = f"Found {len(matching_items)} pages visited on {date_str}:\n\n"
        for item in matching_items:
            # Extract the first 200 characters of content as a preview
            content_preview = item['content'][:200] + "..." if len(item['content']) > 200 else item['content']
            summary += f"URL: {item['url']}\n"
            summary += f"Visits: {item['no_of_visits']}\n"
            summary += f"Summary: {content_preview}\n\n"
        
        return summary
            
    except ValueError as e:
        return f"Error: Invalid date format. Please use YYYY-MM-DD format or natural language like 'May 22nd, 2025'. Error: {str(e)}"
    except Exception as e:
        return f"Error querying history: {str(e)}"


async def query_top_interests_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Query the browsing history to find the top 5 interests based on content analysis.
    
    Params: None - analyzes all available history
    """
    try:
        # Load history data from contents.json
        history_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "contents.json")
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
    
        # Initialize NLTK resources
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Initialize stopwords and common words to exclude
        stop_words = set(stopwords.words('english'))
        common_words = {
            'use', 'using', 'used', 'like', 'may', 'also', 'one', 'two', 'first',
            'new', 'click', 'get', 'see', 'help', 'make', 'can', 'please', 'many',
            'copyright', 'rights', 'reserved', 'privacy', 'policy', 'terms',
            'search', 'google', 'com', 'www', 'https', 'http', 'html', 'php'
        }
        stop_words.update(common_words)
    
        # Process all content and extract keywords
        all_keywords = []
        for item in history_data:
            if 'content' in item:
                # Clean and tokenize the text
                text = item['content'].lower()
                text = text.translate(str.maketrans('', '', string.punctuation))
                tokens = word_tokenize(text)
                
                # Filter tokens
                keywords = [word for word in tokens 
                           if word not in stop_words 
                           and len(word) > 2 
                           and word.isalnum()]
                all_keywords.extend(keywords)
    
        # Count frequencies and get top 5
        keyword_freq = Counter(all_keywords)
        top_interests = keyword_freq.most_common(5)
    
        if not top_interests:
            return "No significant interests found in browsing history"
    
        # Generate summary
        summary = "Your top 5 interests based on browsing history:\n\n"
        for keyword, count in top_interests:
            summary += f"• {keyword.title()}: mentioned {count} times\n"
    
        return summary
    
    except Exception as e:
        return f"Error analyzing interests: {str(e)}"