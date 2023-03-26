import xml.etree.ElementTree as ET


def parse_uniprot_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    entries = []
    for entry in root.findall('{http://uniprot.org/uniprot}entry'):
        protein = entry.find('{http://uniprot.org/uniprot}protein')
        gene = entry.find('{http://uniprot.org/uniprot}gene')
        organism = entry.find('{http://uniprot.org/uniprot}organism')
        references = entry.findall('{http://uniprot.org/uniprot}reference')

        protein_name = protein.find('{http://uniprot.org/uniprot}recommendedName/{http://uniprot.org/uniprot}fullName').text
        gene_name = gene.find('{http://uniprot.org/uniprot}name').text
        organism_name = organism.find('{http://uniprot.org/uniprot}name').text
        reference_ids = [ref.get('id') for ref in references]

        entries.append({
            'protein_name': protein_name,
            'gene_name': gene_name,
            'organism_name': organism_name,
            'reference_ids': reference_ids
        })

    return entries
