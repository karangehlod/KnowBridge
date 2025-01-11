from neo4j import GraphDatabase

class GraphLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_paper(self, paper_id, title):
        with self.driver.session() as session:
            session.write_transaction(self._create_paper, paper_id, title)

    def create_researcher(self, researcher_id, name):
        with self.driver.session() as session:
            session.write_transaction(self._create_researcher, researcher_id, name)

    def create_topic(self, topic_id, name):
        with self.driver.session() as session:
            session.write_transaction(self._create_topic, topic_id, name)

    def create_relationships(self, paper_id, researcher_id, topic_id):
        with self.driver.session() as session:
            session.write_transaction(self._create_relationships, paper_id, researcher_id, topic_id)

    @staticmethod
    def _create_paper(tx, paper_id, title):
        tx.run("CREATE (p:Paper {id: $paper_id, title: $title})", paper_id=paper_id, title=title)

    @staticmethod
    def _create_researcher(tx, researcher_id, name):
        tx.run("CREATE (r:Researcher {id: $researcher_id, name: $name})", researcher_id=researcher_id, name=name)

    @staticmethod
    def _create_topic(tx, topic_id, name):
        tx.run("CREATE (t:Topic {id: $topic_id, name: $name})", topic_id=topic_id, name=name)

    @staticmethod
    def _create_relationships(tx, paper_id, researcher_id, topic_id):
        tx.run("MATCH (p:Paper {id: $paper_id}), (r:Researcher {id: $researcher_id}), (t:Topic {id: $topic_id}) "
               "CREATE (p)-[:PUBLISHED_BY]->(r) "
               "CREATE (p)-[:RELATED_TO]->(t)",
               paper_id=paper_id, researcher_id=researcher_id, topic_id=topic_id)

    def run_cypher_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record.data() for record in result]

    @staticmethod
    def _run_cypher_query(tx, query):
        tx.run(query)

# Example usage
# loader = GraphLoader("bolt://localhost:7687", "neo4j", "password")
# loader.create_paper("P1", "Quantum Computing for Protein Folding")
# loader.create_researcher("R1", "Dr. Smith")
# loader.create_topic("T1", "Quantum Computing")
# loader.create_relationships("P1", "R1", "T1")
# loader.run_cypher_query("""
# CREATE (p:Paper {id: "P1", title: "Quantum Computing for Protein Folding"})
# CREATE (r:Researcher {id: "R1", name: "Dr. Smith"})
# CREATE (t:Topic {id: "T1", name: "Quantum Computing"})
# CREATE (p)-[:PUBLISHED_BY]->(r)
# CREATE (p)-[:RELATED_TO]->(t)
# """)
# loader.close()
