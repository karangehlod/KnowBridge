from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import init_db, get_db
from .models import Paper, Researcher, Topic, Experiment
from .schemas import PaperCreate, ResearcherCreate, TopicCreate, ExperimentCreate
from .crud import create_paper, create_researcher, create_topic, create_experiment
from .data_extraction import process_arxiv_data
from .graph_loader import GraphLoader
import openai
from services import neo4j_service, modus_service, openai_service
import modus

app = FastAPI()
modus_client = modus.Client()

class QueryRequest(BaseModel):
    query: str

class Query(BaseModel):
    user_query: str

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/papers/")
def add_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    return create_paper(db, paper)

@app.post("/researchers/")
def add_researcher(researcher: ResearcherCreate, db: Session = Depends(get_db)):
    return create_researcher(db, researcher)

@app.post("/topics/")
def add_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    return create_topic(db, topic)

@app.post("/experiments/")
def add_experiment(experiment: ExperimentCreate, db: Session = Depends(get_db)):
    return create_experiment(db, experiment)

@app.get("/extract/")
def extract_data(query: str, max_results: int = 10):
    papers = process_arxiv_data(query, max_results)
    return papers

@app.post("/load/")
def load_data_to_neo4j(query: str, max_results: int = 10):
    papers = process_arxiv_data(query, max_results)
    loader = GraphLoader("bolt://localhost:7687", "neo4j", "password")
    
    for paper in papers:
        paper_id = paper['id']
        title = paper['title']
        authors = paper['authors']
        topics = paper['categories']
        
        loader.create_paper(paper_id, title)
        
        for author in authors:
            author_id = author.replace(" ", "_")
            loader.create_researcher(author_id, author)
            loader.create_relationships(paper_id, author_id, None)
        
        for topic in topics:
            topic_id = topic.replace(" ", "_")
            loader.create_topic(topic_id, topic)
            loader.create_relationships(paper_id, None, topic_id)
    
    loader.close()
    return {"status": "Data loaded into Neo4j"}

@app.post("/run_cypher/")
def run_cypher_query(query: str):
    loader = GraphLoader("bolt://localhost:7687", "neo4j", "password")
    loader.run_cypher_query(query)
    loader.close()
    return {"status": "Cypher query executed"}

@app.post("/search")
async def search(request: QueryRequest):
    try:
        # Use Modus API to translate the query and execute it on Neo4j
        cypher_query = modus_service.translate_query(request.query)
        graph_data = modus_service.execute_query(cypher_query)
        
        # Use Modus API to summarize the data
        summary = modus_service.summarize_data(graph_data)
        
        return {"summary": summary, "graph": graph_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            model="gpt-4", 
            input=f"Summarize the following data: {graph_response}"
        )

        return {
            "cypher_query": cypher_query,
            "graph_response": graph_response,
            "summary": summary["result"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
