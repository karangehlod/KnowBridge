# Cross-Domain Research Insight Finder

## Objective

Build a web application that uses Knowledge Graphs and AI to connect disparate research insights, facilitating scientific discovery across disciplines.

## Key Features

1. **Natural Language Query Interface**: Users can ask questions like "What are the latest breakthroughs in quantum computing for drug discovery?"
2. **Knowledge Graph Integration**: Use Neo4j or Dgraph to store and query data relationships.
3. **AI-Powered Summarization**: Use GPT (via Modus) to process user queries and summarize results.
4. **Interactive Visualization**: Visualize research relationships with tools like D3.js or Cytoscape.js.

## Setup

### Backend

1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `uvicorn app.main:app --reload`

### Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the application: `npm start`

### Docker

1. Ensure Docker is installed and running.
2. Run `docker-compose up --build` to start both the backend and frontend services.

## Testing

1. Navigate to the `backend` directory.
2. Run tests: `pytest`
