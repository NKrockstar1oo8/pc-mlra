"""
Demo Service for when PC-MLRA core is not available
"""
from typing import Dict, Any

class DemoService:
    """Demo service for fallback functionality"""
    
    @staticmethod
    def process_query(query: str) -> Dict[str, Any]:
        """Process query in demo mode"""
        demo_responses = {
            "Can I get my medical reports?": "Yes, you have the right to access your medical records and reports. This is established in the NHRC Patient Charter 2019.",
            "Doctor was rude to me": "Doctors are expected to maintain professional conduct. The IMC Ethics Regulations 2002 outline obligations regarding respectful behavior.",
            "I need a second opinion": "You have the right to seek a second opinion from another healthcare provider.",
            "Hospital is charging too much": "Hospitals should provide transparent billing. Patients have rights regarding fair and itemized charges.",
            "Can I choose my own pharmacy?": "Yes, you generally have the right to choose your pharmacy or source for medications.",
            "hi": "Hello! I'm PC-MLRA, your Medical Legal Rights Advisor. How can I help you today?",
            "hello": "Hello! I'm PC-MLRA, your Medical Legal Rights Advisor. How can I help you today?",
            "help": "I can help you understand your medical rights and doctor obligations. Try asking about medical records, consent, billing, or doctor behavior.",
        }
        
        query_lower = query.lower()
        for key in demo_responses:
            if key.lower() in query_lower or query_lower in key.lower():
                return {
                    'response': demo_responses[key],
                    'intent': 'demo_match',
                    'confidence': 0.8
                }
        
        return {
            'response': f"I understand you're asking about '{query}'. In the full PC-MLRA system, I would provide specific legal references from the NHRC Patient Charter 2019 and IMC Ethics Regulations 2002.",
            'intent': 'demo_general',
            'confidence': 0.3
        }
    
    @staticmethod
    def get_system_stats() -> Dict[str, Any]:
        """Get demo system statistics"""
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
    
    @staticmethod
    def search_knowledge(keyword: str) -> Dict[str, Any]:
        """Demo search functionality"""
        return {
            'query': keyword,
            'results': [],
            'total': 0,
            'note': 'PC-MLRA core not loaded. Search unavailable in demo mode.'
        }
