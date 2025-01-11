from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import modus

app = FastAPI()
modus_client = Modus()

class Query(BaseModel):
    user_query: str

@app.post("/query")
async def process_query(query: Query):
    try:
        # Translate user input into Cypher query using Modus
        cypher_response = modus_client.models().call(
            model="cypher-translate", 
            input=query.user_query
        )
        cypher_query = cypher_response["result"]

        # Query Neo4j via Modus
        graph_response = modus_client.knowledge_graph().query(query=cypher_query)

        # Summarize results using Azure OpenAI (via Modus)
        summary = modus_client.models().call(
            model="gpt-4o", 
            input=f"Summarize the following data: {graph_response}"
        )

        return {
            "cypher_query": cypher_query,
            "graph_response": graph_response,
            "summary": summary["result"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
