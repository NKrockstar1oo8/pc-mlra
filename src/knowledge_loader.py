"""
Knowledge Base Loader for PC-MLRA
Loads and manages the structured knowledge base
"""

import json
from typing import Dict, List, Optional, Any

class KnowledgeBase:
    def __init__(self, knowledge_file: str = "data/structured/knowledge_base_complete.json"):
        self.knowledge_file = knowledge_file
        self.data = self._load_knowledge_base()
        self.clauses_by_id = {clause["id"]: clause for clause in self.data["clauses"]}
        self.clauses_by_intent = self._index_by_intent()
        self.clauses_by_right = self._index_by_right()
        
    def _load_knowledge_base(self) -> Dict:
        """Load the knowledge base from JSON file"""
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Knowledge base file not found: {self.knowledge_file}")
            return {"clauses": []}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from: {self.knowledge_file}")
            return {"clauses": []}
    
    def _index_by_intent(self) -> Dict[str, List[Dict]]:
        """Create index of clauses by intent_match"""
        index = {}
        for clause in self.data.get("clauses", []):
            for intent in clause.get("intent_match", []):
                if intent not in index:
                    index[intent] = []
                index[intent].append(clause)
        return index
    
    def _index_by_right(self) -> Dict[str, List[Dict]]:
        """Create index of clauses by rights"""
        index = {}
        for clause in self.data.get("clauses", []):
            for right in clause.get("rights", []):
                if right not in index:
                    index[right] = []
                index[right].append(clause)
        return index
    
    def get_clause_by_id(self, clause_id: str) -> Optional[Dict]:
        """Get a specific clause by its ID"""
        return self.clauses_by_id.get(clause_id)
    
    def get_clauses_by_intent(self, intent: str) -> List[Dict]:
        """Get all clauses matching a specific intent"""
        return self.clauses_by_intent.get(intent, [])
    
    def get_clauses_by_right(self, right: str) -> List[Dict]:
        """Get all clauses containing a specific right"""
        return self.clauses_by_right.get(right, [])
    
    def get_all_clauses(self) -> List[Dict]:
        """Get all clauses in the knowledge base"""
        return self.data.get("clauses", [])
    
    def get_metadata(self) -> Dict:
        """Get system metadata"""
        return self.data.get("metadata", {})
    
    def get_documents_info(self) -> Dict:
        """Get information about source documents"""
        return self.data.get("documents", {})
    
    def get_relationships(self) -> List[Dict]:
        """Get all relationships between rights and obligations"""
        return self.data.get("relationships", [])
    
    def search_clauses_by_keyword(self, keyword: str) -> List[Dict]:
        """Search clauses by keyword"""
        keyword = keyword.lower()
        results = []
        for clause in self.data.get("clauses", []):
            # Search in keywords list
            if any(keyword in kw.lower() for kw in clause.get("keywords", [])):
                results.append(clause)
            # Search in title and text
            elif (keyword in clause.get("title", "").lower() or 
                  keyword in clause.get("exact_text", "").lower() or
                  keyword in clause.get("paraphrase", "").lower()):
                results.append(clause)
        return results
    
    def get_clauses_by_category(self, category: str) -> List[Dict]:
        """Get all clauses in a specific category"""
        return [clause for clause in self.data.get("clauses", []) 
                if clause.get("category") == category]
    
    def get_rights_for_actor(self, actor: str) -> List[Dict]:
        """Get all rights for a specific actor (patient, doctor, hospital)"""
        rights = []
        for clause in self.data.get("clauses", []):
            if actor in clause.get("actors", []):
                # Extract rights from this clause
                for right_name in clause.get("rights", []):
                    right_info = {
                        "right": right_name,
                        "clause_id": clause["id"],
                        "title": clause["title"],
                        "document": clause["document_abbr"],
                        "section": clause["section"]
                    }
                    rights.append(right_info)
        return rights
    
    def get_obligations_for_actor(self, actor: str) -> List[Dict]:
        """Get all obligations for a specific actor"""
        obligations = []
        for clause in self.data.get("clauses", []):
            if actor in clause.get("actors", []):
                # Extract obligations from this clause
                for obligation_name in clause.get("obligations", []):
                    obligation_info = {
                        "obligation": obligation_name,
                        "clause_id": clause["id"],
                        "title": clause["title"],
                        "document": clause["document_abbr"],
                        "section": clause["section"]
                    }
                    obligations.append(obligation_info)  # FIXED: was 'rights', should be 'obligations'
        return obligations

# Test function
def test_knowledge_base():
    kb = KnowledgeBase()
    
    print("Knowledge Base Loader Test")
    print("=" * 70)
    
    # Test metadata
    metadata = kb.get_metadata()
    print(f"\nSystem: {metadata.get('system_name')}")
    print(f"Version: {metadata.get('version')}")
    print(f"Total Clauses: {metadata.get('total_clauses')}")
    
    # Test clause retrieval
    clause = kb.get_clause_by_id("NHRC-1")
    if clause:
        print(f"\nSample Clause (NHRC-1):")
        print(f"Title: {clause['title']}")
        print(f"Document: {clause['document_abbr']} Section {clause['section']}")
        print(f"Rights: {', '.join(clause['rights'][:3])}...")
    
    # Test intent search
    print(f"\nClauses matching 'access_medical_records':")
    clauses = kb.get_clauses_by_intent("access_medical_records")
    for c in clauses:
        print(f"  - {c['id']}: {c['title']}")
    
    # Test category search
    print(f"\nClauses in 'access_information' category:")
    category_clauses = kb.get_clauses_by_category("access_information")
    for c in category_clauses[:3]:  # Show first 3
        print(f"  - {c['id']}: {c['title']}")
    
    # Test keyword search
    print(f"\nSearch results for 'emergency':")
    search_results = kb.search_clauses_by_keyword("emergency")
    for c in search_results:
        print(f"  - {c['id']}: {c['title']}")
    
    # Test actor rights
    print(f"\nRights for 'patient':")
    patient_rights = kb.get_rights_for_actor("patient")
    for right in patient_rights[:5]:  # Show first 5
        print(f"  - {right['right']} (from {right['clause_id']})")
    
    return kb


if __name__ == "__main__":
    kb = test_knowledge_base()