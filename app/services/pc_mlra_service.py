"""
PC-MLRA Core Service
"""
import os
import sys
import traceback
from typing import Dict, Any, List, Optional

class PCMLRAService:
    """Service wrapper for PC-MLRA core functionality"""
    
    def __init__(self):
        """Initialize PC-MLRA system"""
        self.console = None
        self.initialized = False
        self._initialize()
    
    def _initialize(self):
        """Initialize the PC-MLRA core system"""
        try:
            # Add src directory to path
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            src_dir = os.path.join(current_dir, 'src')
            
            if src_dir not in sys.path:
                sys.path.insert(0, src_dir)
            
            # Import PC-MLRA
            from src.main import PCMLRAConsole
            
            # Initialize
            self.console = PCMLRAConsole()
            self.initialized = True
            
            # Quick test
            test_response = self.console.process_query("Can I get my medical reports?")
            
            return True
            
        except ImportError as e:
            print(f"Import error: {e}")
            return False
        except Exception as e:
            print(f"Initialization error: {e}")
            traceback.print_exc()
            return False
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query"""
        if not self.initialized or not self.console:
            return {
                'response': 'PC-MLRA system not available',
                'intent': 'system_error',
                'confidence': 0.0
            }
        
        try:
            result = self.console.process_query(query)
            
            if isinstance(result, dict):
                return result
            else:
                return {
                    'response': str(result),
                    'intent': 'general_query',
                    'confidence': 1.0
                }
                
        except Exception as e:
            print(f"Query processing error: {e}")
            return {
                'response': f'Error processing query: {str(e)}',
                'intent': 'error',
                'confidence': 0.0
            }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        if not self.initialized or not self.console:
            return self._get_demo_stats()
        
        try:
            # Get metadata from knowledge base
            metadata = self.console.kb.get_metadata()
            
            # Get all clauses
            clauses = self.console.kb.get_all_clauses()
            
            # Count by category
            categories = {}
            for clause in clauses:
                category = clause.get("category", "uncategorized")
                categories[category] = categories.get(category, 0) + 1
            
            # Format categories
            formatted_categories = {}
            for cat, count in categories.items():
                readable_name = cat.replace('_', ' ').title()
                formatted_categories[readable_name] = count
            
            return {
                'system_name': metadata.get('system_name', 'PC-MLRA'),
                'version': metadata.get('version', '1.0.0'),
                'total_clauses': len(clauses),
                'documents': [
                    'NHRC Patient Charter (2019)',
                    'IMC Ethics Regulations (2002)'
                ],
                'categories': formatted_categories,
                'system_status': 'operational'
            }
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            return self._get_demo_stats()
    
    def search_knowledge(self, keyword: str) -> Dict[str, Any]:
        """Search the knowledge base"""
        if not self.initialized or not self.console:
            return {
                'query': keyword,
                'results': [],
                'total': 0,
                'note': 'PC-MLRA core not loaded'
            }
        
        try:
            results = self.console.kb.search_clauses_by_keyword(keyword)
            
            # Format results
            formatted_results = []
            for clause in results[:20]:  # Limit to 20 results
                formatted_results.append({
                    'id': clause.get('id', ''),
                    'title': clause.get('title', ''),
                    'document': clause.get('document_abbr', ''),
                    'section': clause.get('section', ''),
                    'category': clause.get('category', '').replace('_', ' ').title(),
                    'summary': clause.get('paraphrase', '')[:200] + '...' if clause.get('paraphrase') else ''
                })
            
            return {
                'query': keyword,
                'results': formatted_results,
                'total': len(results)
            }
            
        except Exception as e:
            print(f"Error searching knowledge: {e}")
            return {
                'query': keyword,
                'results': [],
                'total': 0,
                'error': str(e)
            }
    
    def _get_demo_stats(self) -> Dict[str, Any]:
        """Get demo statistics when core is not available"""
        return {
            'system_name': 'PC-MLRA (Demo Mode)',
            'version': '1.0.0',
            'total_clauses': 46,
            'documents': [
                'NHRC Patient Charter (2019)',
                'IMC Ethics Regulations (2002)'
            ],
            'categories': {
                'Access Information': 8,
                'Consent Autonomy': 12,
                'Privacy Confidentiality': 9,
                'Quality Safety': 10,
                'Redressal Complaint': 7,
                'Professional Conduct': 8,
                'Transparency Rates': 6,
                'Continuity Care': 5,
                'Emergency Care': 4,
                'Research Education': 4,
                'Non Discrimination': 4
            },
            'system_status': 'demo_mode'
        }
