from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from typing import List, Optional
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = SentenceTransformer('all-MiniLM-L6-v2')

# Establish connection to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Define the request model for user query
class UserQuery(BaseModel):
    question: str
    top_n: Optional[int] = 3  # Number of top results to return, default is 3

# Define your endpoint for querying FAQs
@app.post("/search/")
async def search_faqs(query: UserQuery):
    
    query_embedding = query_to_embedding(query.question)

    # Elasticsearch query
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": query_embedding}
            }
        }
    }

    try:
        # Perform the search
        response = es.search(
            index="university-info",  
            body={
                "query": script_query,
                "_source": ["section", "content"],  
                "size": query.top_n
            }
        )
        # Extract results
        results = [{"section": hit['_source']['section'], "content": hit['_source']['content'], "score": hit['_score']}
                   for hit in response['hits']['hits']]
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def query_to_embedding(query: str) -> List[float]:
    
    
    embedding = model.encode(query)
   
    return embedding.tolist() 
