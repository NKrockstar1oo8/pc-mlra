"""
Main Application Entry Point for PC-MLRA
Command-line interface for testing
"""

import sys
import os

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.response_assembler import ResponseAssembler
from src.knowledge_loader import KnowledgeBase

class PCMLRAConsole:
    def __init__(self):
        self.assembler = ResponseAssembler()
        self.kb = KnowledgeBase()
        self.show_proof = True
        
    def display_banner(self):
        """Display application banner"""
        banner = """
╔═════════════════════════════════════════════════════════╗
║      PROOF-CARRYING MEDICAL-LEGAL RIGHTS ADVISOR        ║
║               (PC-MLRA) - v1.0.0                        ║
║                                                         ║
║  A Deterministic, Zero-Hallucination System             ║
║  for Medical Rights Awareness                           ║
╚═════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    def display_help(self):
        """Display help information"""
        help_text = """
Available Commands:
  ? or help          - Show this help
  quit or exit       - Exit the application
  proof on/off       - Toggle proof trace display
  list rights        - List all patient rights
  list categories    - List all rights categories
  search <keyword>   - Search for rights by keyword
  clause <id>        - Show detailed information for a clause
  stats              - Show system statistics
  clear              - Clear screen
        """
        print(help_text)
    
    def display_stats(self):
        """Display system statistics"""
        metadata = self.kb.get_metadata()
        clauses = self.kb.get_all_clauses()
        
        # Count by category
        categories = {}
        for clause in clauses:
            category = clause.get("category", "uncategorized")
            categories[category] = categories.get(category, 0) + 1
        
        print("\nSystem Statistics:")
        print("=" * 50)
        print(f"System: {metadata.get('system_name', 'PC-MLRA')}")
        print(f"Version: {metadata.get('version', '1.0.0')}")
        print(f"Total Clauses: {metadata.get('total_clauses', len(clauses))}")
        print(f"Source Documents: 2 (NHRC Charter + IMC Ethics Code)")
        print("\nClauses by Category:")
        for category, count in sorted(categories.items()):
            readable_category = category.replace("_", " ").title()
            print(f"  {readable_category}: {count}")
        print("=" * 50)
    
    def list_rights(self):
        """List all patient rights"""
        clauses = self.kb.get_all_clauses()
        
        print("\nPatient Rights Catalog:")
        print("=" * 70)
        
        for clause in clauses:
            print(f"\n{clause['id']}: {clause['title']}")
            print(f"  Document: {clause['document_abbr']} Section {clause['section']}")
            print(f"  Category: {clause['category'].replace('_', ' ').title()}")
            print(f"  Summary: {clause['paraphrase'][:100]}...")
        
        print(f"\nTotal: {len(clauses)} rights documented")
        print("=" * 70)
    
    def list_categories(self):
        """List all rights categories with examples"""
        categories = {
            "access_information": "Access & Information Rights",
            "consent_autonomy": "Consent & Autonomy Rights",
            "privacy_confidentiality": "Privacy & Confidentiality Rights",
            "quality_safety": "Quality & Safety Rights",
            "redressal_complaint": "Redressal & Complaint Rights"
        }
        
        print("\nRights Categories:")
        print("=" * 50)
        
        for cat_id, cat_name in categories.items():
            clauses = self.kb.get_clauses_by_category(cat_id)
            print(f"\n{cat_name}:")
            print(f"  Contains {len(clauses)} rights")
            print("  Examples:")
            for clause in clauses[:3]:  # Show first 3 examples
                print(f"    • {clause['title']}")
        
        print("=" * 50)
    
    def search_rights(self, keyword: str):
        """Search for rights by keyword"""
        results = self.kb.search_clauses_by_keyword(keyword)
        
        print(f"\nSearch Results for '{keyword}':")
        print("=" * 70)
        
        if not results:
            print("No rights found matching your search.")
            return
        
        for clause in results:
            print(f"\n{clause['id']}: {clause['title']}")
            print(f"  {clause['paraphrase'][:150]}...")
            print(f"  [Type 'clause {clause['id']}' for details]")
        
        print(f"\nFound {len(results)} matching rights")
        print("=" * 70)
    
    def show_clause_details(self, clause_id: str):
        """Show detailed information for a specific clause"""
        response = self.assembler.generate_detailed_response(clause_id)
        print(response)
    
    def process_query(self, query: str):
        """Process a user query and return response"""
        if not query.strip():
            return None
        
        # Handle commands
        if query.lower() in ['?', 'help']:
            self.display_help()
            return None
        elif query.lower() in ['quit', 'exit']:
            print("Thank you for using PC-MLRA. Goodbye!")
            sys.exit(0)
        elif query.lower().startswith('proof '):
            mode = query.lower().split()[1]
            if mode == 'on':
                self.show_proof = True
                print("Proof trace display: ON")
            elif mode == 'off':
                self.show_proof = False
                print("Proof trace display: OFF")
            return None
        elif query.lower() == 'list rights':
            self.list_rights()
            return None
        elif query.lower() == 'list categories':
            self.list_categories()
            return None
        elif query.lower() == 'stats':
            self.display_stats()
            return None
        elif query.lower().startswith('search '):
            keyword = query[7:].strip()
            self.search_rights(keyword)
            return None
        elif query.lower().startswith('clause '):
            clause_id = query[7:].strip()
            self.show_clause_details(clause_id)
            return None
        elif query.lower() == 'clear':
            print("\n" * 50)
            return None
        
        # Handle regular query
        response, proof_trace = self.assembler.generate_response(query, self.show_proof)
        return response
    
    def run(self):
        """Run the console application"""
        self.display_banner()
        print("Type '?' for help, 'quit' to exit\n")
        
        while True:
            try:
                query = input("\n> ")
                response = self.process_query(query)
                if response:
                    print(f"\n{response}")
            except KeyboardInterrupt:
                print("\n\nThank you for using PC-MLRA. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again or type '?' for help.")

def main():
    """Main function"""
    app = PCMLRAConsole()
    app.run()

if __name__ == "__main__":
    main()