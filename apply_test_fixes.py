import json

# Load your file
with open('knowledge_base.json', 'r') as f:
    data = json.load(f)

# Count current clauses
nhrc_count = sum(1 for c in data['clauses'] if c['document'] == 'NHRC')
imc_count = sum(1 for c in data['clauses'] if c['document'] == 'IMC')
print(f"Current: NHRC={nhrc_count}, IMC={imc_count}, Total={nhrc_count + imc_count}")

# Find duplicate IDs
ids = [c['id'] for c in data['clauses']]
duplicates = set([id for id in ids if ids.count(id) > 1])
print(f"Duplicate IDs: {duplicates}")

# Find IMC clauses with wrong IDs
print("\nIMC clauses that need fixing:")
for clause in data['clauses']:
    if clause['document'] == 'IMC':
        # Check for duplicate pattern issues
        if clause['id'] in ['IMC-1.2', 'IMC-6.8']:
            print(f"  ❌ Remove duplicate: {clause['id']} - {clause['title'][:50]}...")
        
        # Check category issues
        if clause['id'] == 'IMC-5.2' and clause['category'] != 'public_health':
            print(f"  ⚠ Fix category for IMC-5.2: change '{clause['category']}' to 'public_health'")
        if clause['id'] == 'IMC-7.22' and clause['category'] != 'research_ethics':
            print(f"  ⚠ Fix category for IMC-7.22: change '{clause['category']}' to 'research_ethics'")

print(f"\nYou need to have exactly 29 IMC clauses.")
print(f"You currently have {imc_count} IMC clauses.")
print(f"You need to remove {imc_count - 29} IMC clauses.")

# Update metadata
data['metadata']['version'] = "3.1.0"
data['metadata']['total_clauses'] = nhrc_count + 29  # Should be 46

print(f"\n✅ After fixing:")
print(f"  Version: {data['metadata']['version']}")
print(f"  Total clauses should be: 46 (17 NHRC + 29 IMC)")