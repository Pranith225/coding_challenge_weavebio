from neo4j import GraphDatabase


class Neo4jLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, entries):
        with self.driver.session() as session:
            for entry in entries:
                protein_name = entry['protein_name']
                gene_name = entry['gene_name']
                organism_name = entry['organism_name']
                reference_ids = entry['reference_ids']

                session.write_transaction(self._create_and_connect_nodes, protein_name, gene_name, organism_name, reference_ids)

    @staticmethod
    def _create_and_connect_nodes(tx, protein_name, gene_name, organism_name, reference_ids):
        tx.run("""
            MERGE (p:Protein {name: $protein_name})
            MERGE (g:Gene {name: $gene_name})
            MERGE (o:Organism {name: $organism_name})
            MERGE (p)-[:ENCODED_BY]->(g)
            MERGE (g)-[:PART_OF]->(o)
            WITH p, g
            UNWIND $reference_ids AS ref_id
            MERGE (r:Reference {id: ref_id})
            MERGE (g)-[:HAS_REFERENCE]->(r)
        """, protein_name=protein_name, gene_name=gene_name, organism_name=organism_name, reference_ids=reference_ids)
