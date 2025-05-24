from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from history_processor import HistoryProcessor
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BrowseIQ API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processor
processor = HistoryProcessor()

class Query(BaseModel):
    question: str

class ProcessURLsRequest(BaseModel):
    urls: List[str]

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None

@app.post("/process-history")
async def process_history():
    """Process all URLs from browser history"""
    try:
        processor.process_history()
        return {"status": "success", "message": "History processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-urls")
async def process_urls(request: ProcessURLsRequest):
    """Process specific URLs"""
    try:
        processor.processor.process_urls(request.urls)
        return {"status": "success", "message": f"Processed {len(request.urls)} URLs"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_history(query: Query):
    """Query processed history"""
    try:
        result = processor.query_history(query.question)
        return QueryResponse(
            answer=result['answer'],
            sources=result.get('source_documents', [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)