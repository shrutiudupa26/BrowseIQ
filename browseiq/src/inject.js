// Create a div and append to body
const container = document.createElement('div');
container.id = 'my-react-root';
document.body.appendChild(container);

// Load React app script
const script = document.createElement('script');
script.src = chrome.runtime.getURL('static/js/main.js'); // adjust path for Safari if needed
script.type = 'text/javascript';
document.body.appendChild(script);
