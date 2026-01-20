#!/usr/bin/env python3
import json
from datetime import datetime

# Load the knowledge base
with open('data/structured/knowledge_base_complete.json', 'r') as f:
    data = json.load(f)

# Update metadata
data['metadata']['total_clauses'] = len(data['clauses'])
data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')

# Count NHRC and IMC clauses
nhrc_count = sum(1 for clause in data['clauses'] if clause['document_abbr'] == 'NHRC')
imc_count = sum(1 for clause in data['clauses'] if clause['document_abbr'] == 'IMC')

print(f"NHRC clauses: {nhrc_count}")
print(f"IMC clauses: {imc_count}")
print(f"Total clauses: {len(data['clauses'])}")

# Update description
data['metadata']['description'] = f"Complete knowledge base with {nhrc_count} NHRC patient rights and {imc_count} IMC doctor obligations"

# Save back
with open('data/structured/knowledge_base_complete.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Metadata updated successfully!")
