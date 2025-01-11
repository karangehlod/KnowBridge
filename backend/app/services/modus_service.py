import requests

MODUS_API_URL = "https://api.modusframework.com"

def translate_query(natural_language_query):
    response = requests.post(f"{MODUS_API_URL}/translate", json={"query": natural_language_query})
    response.raise_for_status()
    return response.json()["cypher_query"]

def execute_query(cypher_query):
    response = requests.post(f"{MODUS_API_URL}/execute", json={"query": cypher_query})
    response.raise_for_status()
    return response.json()["graph_data"]

def summarize_data(graph_data):
    response = requests.post(f"{MODUS_API_URL}/summarize", json={"data": graph_data})
    response.raise_for_status()
    return response.json()["summary"]
