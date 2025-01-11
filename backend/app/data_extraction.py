import requests
import spacy
import xml.etree.ElementTree as ET

nlp = spacy.load('en_core_web_sm')

def fetch_arxiv_data(query, max_results=10):
    url = f'http://export.arxiv.org/api/query?search_query={query}&max_results={max_results}'
    response = requests.get(url)
    return response.text

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def process_arxiv_data(query, max_results=10):
    data = fetch_arxiv_data(query, max_results)
    papers = parse_arxiv_xml(data)
    for paper in papers:
        entities = extract_entities(paper['summary'])
        paper['entities'] = entities
    return papers

def parse_arxiv_xml(xml_data):
    root = ET.fromstring(xml_data)
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        published = entry.find('{http://www.w3.org/2005/Atom}published').text
        papers.append({
            'title': title,
            'summary': summary,
            'authors': authors,
            'published': published
        })
    return papers
