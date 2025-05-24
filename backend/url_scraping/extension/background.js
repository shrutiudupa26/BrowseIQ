async function collectHistory() {
  const oneWeekAgo = new Date().getTime() - 7 * 24 * 60 * 60 * 1000;
  
  chrome.history.search({
    text: '',
    startTime: oneWeekAgo,
    maxResults: 10000
  }, async function(historyItems) {
    const historyData = [];
    
    for (const item of historyItems) {
      const visits = await new Promise(resolve => {
        chrome.history.getVisits({ url: item.url }, resolve);
      });
      
      historyData.push({
        url: item.url,
        title: item.title,
        visitCount: item.visitCount,
        lastVisitTime: item.lastVisitTime,
        visits: visits
      });
    }
    
    // Send to your backend
    await fetch('http://localhost:5000/api/history', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(historyData)
    });
  });
}

// Run when extension loads
collectHistory();