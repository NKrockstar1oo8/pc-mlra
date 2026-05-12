"""
Response Assembler for PC-MLRA
Assembles complete responses from intents and knowledge
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import re

from src.intent_classifier import IntentClassifier
from src.knowledge_loader import KnowledgeBase
from src.template_engine import TemplateEngine

EMERGENCY_KEYWORDS = {
    "emergency",
    "critical",
    "accident",
    "unconscious",
    "bleeding",
    "severe pain",
    "life threatening",
    "serious injury",
    "immediate"
}

@dataclass
class ProofTrace:
    """Tracks the proof chain for a response"""
    query: str
    matched_intents: List[Tuple[str, float]]
    matched_clauses: List[Dict]
    template_used: str
    variables_used: List[str]
    normalized_query: str

    
    def to_dict(self) -> Dict:
        """Convert to dictionary for display"""
        return {
            "query": self.query,
            "normalized_query": self.normalized_query,
            "matched_intents": [
                {"intent": intent, "confidence": confidence}
                for intent, confidence in self.matched_intents
            ],
            "matched_clauses": [
                {
                    "id": clause["id"],
                    "title": clause["title"],
                    "citation": clause["citation_format"]
                }
                for clause in self.matched_clauses
            ],
            "template_used": self.template_used,
            "variables_filled": len(self.variables_used)
        }
        
    def format(self) -> str:
        """Format proof trace for display"""
        lines = []
        lines.append("**Proof Trace**")
        lines.append("=" * 50)
        lines.append(f"**Query:** {self.query}")
        lines.append("")
        lines.append("**Matched Intents:**")
        for intent, confidence in self.matched_intents:
            lines.append(f"  • {intent} (confidence: {confidence:.2f})")
        lines.append("")
        lines.append("**Legal Sources Cited:**")
        for clause in self.matched_clauses:
            lines.append(f"  • {clause['citation_format']} - {clause['title']}")
        lines.append("")
        lines.append("**Generation Method:**")
        lines.append(f"  Template: {self.template_used}")
        lines.append(f"  Variables filled: {len(self.variables_used)}")
        lines.append("=" * 50)
        return "\n".join(lines)

class ResponseAssembler:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.kb = KnowledgeBase()
        self.template_engine = TemplateEngine()
        
    def clean_query(self, query: str) -> str:
        """Clean user query for processing"""
        query = query.strip()
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query)
        return query
    
    def has_emergency_signal(self, query: str) -> bool:
        q = query.lower()
        return any(keyword in q for keyword in EMERGENCY_KEYWORDS)
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query"""
        # Remove common stop words
        stop_words = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
                     "you", "your", "yours", "yourself", "yourselves", "he", "him", 
                     "his", "himself", "she", "her", "hers", "herself", "it", "its", 
                     "itself", "they", "them", "their", "theirs", "themselves", 
                     "what", "which", "who", "whom", "this", "that", "these", 
                     "those", "am", "is", "are", "was", "were", "be", "been", 
                     "being", "have", "has", "had", "having", "do", "does", "did", 
                     "doing", "a", "an", "the", "and", "but", "if", "or", "because", 
                     "as", "until", "while", "of", "at", "by", "for", "with", 
                     "about", "against", "between", "into", "through", "during", 
                     "before", "after", "above", "below", "to", "from", "up", 
                     "down", "in", "out", "on", "off", "over", "under", "again", 
                     "further", "then", "once", "here", "there", "when", "where", 
                     "why", "how", "all", "any", "both", "each", "few", "more", 
                     "most", "other", "some", "such", "no", "nor", "not", "only", 
                     "own", "same", "so", "than", "too", "very", "s", "t", "can", 
                     "will", "just", "don", "should", "now"}
        
        words = query.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Also include phrases that might be important
        important_phrases = [
            "medical records", "emergency care", "informed consent", 
            "second opinion", "patient rights", "medical negligence",
            "overcharged", "without permission", "refused to give",
            "asked for payment", "shared information", "discriminated against"
        ]
        
        for phrase in important_phrases:
            if phrase in query.lower():
                keywords.append(phrase.replace(" ", "_"))
        
        return keywords[:10]  # Limit to 10 keywords
    
    def format_bullets(self, items):
        """
        Convert a list of strings into a bullet-formatted string.
        Deterministic formatting for templates.
        """
        if not items:
            return ""

        return "\n".join(
            f"• {item.replace('_', ' ').capitalize()}" for item in items
        )

    def select_template(self, intents: List[Tuple[str, float]], clauses: List[Dict]) -> str:
        if not intents or not clauses:
            return "TEMPLATE_NO_MATCH_FOUND"
        
        # Get all intent names
        intent_names = [i[0] for i in intents]
        
        # Check for patient_education in ANY of the matched intents
        if "patient_education" in intent_names:
            return "TEMPLATE_RIGHT_TO_PATIENT_EDUCATION"
        
        # Check for other high-priority intents
        if "emergency_care" in intent_names:
            return "TEMPLATE_RIGHT_TO_EMERGENCY_CARE"

        top_intent = intents[0][0]
        
        ## 🔒 FIX: Check patient_education FIRST before anything else
       # if top_intent == "patient_education":
        #    return "TEMPLATE_RIGHT_TO_PATIENT_EDUCATION"

       # # Map grievance_redressal to existing template (NHRC-17)
        #if top_intent in {"grievance_redressal", "how_to_complain", "complaint_procedure"}:
        #    return "TEMPLATE_SINGLE_CLAUSE"

        
        # Check for specialized templates based on intent
        specialized_templates = {
            "access_medical_records": "TEMPLATE_RIGHT_TO_RECORDS",
            "informed_consent": "TEMPLATE_RIGHT_TO_INFORMED_CONSENT",
            "emergency_care": "TEMPLATE_RIGHT_TO_EMERGENCY_CARE",
            "privacy_confidentiality": "TEMPLATE_RIGHT_TO_PRIVACY",
            "right_to_information": "TEMPLATE_RIGHT_TO_INFORMATION",
            "second_opinion": "TEMPLATE_RIGHT_TO_SECOND_OPINION",
            "patient_education": "TEMPLATE_RIGHT_TO_PATIENT_EDUCATION",
            "non_discrimination": "TEMPLATE_RIGHT_TO_NON_DISCRIMINATION",
            "transparent_pricing": "TEMPLATE_RIGHT_TO_TRANSPARENT_PRICING",
            "detained_for_payment": "TEMPLATE_RIGHT_TO_DISCHARGE_BODY",
            "body_withheld": "TEMPLATE_RIGHT_TO_DISCHARGE_BODY",
            "clinical_trial_rights": "TEMPLATE_RIGHT_TO_CLINICAL_TRIAL_PROTECTION",
            "biomedical_research": "TEMPLATE_RIGHT_TO_BIOMEDICAL_RESEARCH_PROTECTION",
            "research_rights": "TEMPLATE_RIGHT_TO_BIOMEDICAL_RESEARCH_PROTECTION"
        }

        if top_intent in specialized_templates:
            return specialized_templates[top_intent]
        
        # Default to single clause template
        return "TEMPLATE_SINGLE_CLAUSE"
    
    def prepare_context(self, template_id: str, intents: List[Tuple[str, float]], 
                       clauses: List[Dict], query: str = "") -> Dict:
        """Prepare context dictionary for template filling"""
        context = {
            "query": query,
            "query_keywords": ", ".join(self.extract_keywords(query)),
            "show_proof_trace": True,
            "show_exact_text": False  # Default to not showing exact legal text
        }
        
        if template_id == "TEMPLATE_SINGLE_CLAUSE" and clauses:
            # Primary clause (highest priority)
            clause = clauses[0]
            context.update({
                "title": clause.get("title", ""),
                "citation_format": clause.get("citation_format", ""),
                "exact_text": clause.get("exact_text", ""),
                "paraphrase": clause.get("paraphrase", ""),
                "rights_bulleted": clause.get("rights", []),
                "obligations_bulleted": clause.get("obligations", []),
                "exceptions_bulleted": clause.get("exceptions", []),
                "legal_references_bulleted": clause.get("legal_references", []),
                "timeframe_note": clause.get("timeframes", {})
            })
            
            # Add note about additional relevant rights if present
            if len(clauses) > 1:
                additional = [c.get("title", "") for c in clauses[1:3]]  # Max 2 additional
                context["additional_rights"] = additional
            
        elif template_id == "TEMPLATE_RIGHT_TO_PATIENT_EDUCATION" and clauses:
            clause = clauses[0]

            context["citation_format"] = clause.get("citation_format", "")
            context["paraphrase"] = clause.get("paraphrase", "")

            context["rights_bulleted"] = self.format_bullets(
                clause.get("rights", [])
            )

            context["obligations_bulleted"] = self.format_bullets(
                clause.get("obligations", [])
            )

        elif template_id == "TEMPLATE_RIGHT_TO_RECORDS" and clauses:
            # Find the right to records clause
            records_clause = next((c for c in clauses if c["id"] == "NHRC-2"), None)
            if not records_clause:
                records_clause = clauses[0]
            context.update({
                "citation_format": records_clause.get("citation_format", "")
            })
            
        elif template_id == "TEMPLATE_RIGHT_TO_PRIVACY" and clauses:
            privacy_clause = next((c for c in clauses if c["id"] == "NHRC-5"), None)
            if not privacy_clause:
                privacy_clause = clauses[0]
            context.update({
                "citation_format": privacy_clause.get("citation_format", "")
            })
        
        elif template_id == "TEMPLATE_RIGHT_TO_INFORMATION" and clauses:
            info_clause = next((c for c in clauses if c["id"] == "NHRC-1"), None)
            if not info_clause:
                info_clause = clauses[0]
            context.update({
                "citation_format": info_clause.get("citation_format", "")
            })
            
        elif template_id == "TEMPLATE_RIGHT_TO_EMERGENCY_CARE" and clauses:
            emergency_clause = next((c for c in clauses if c["id"] == "NHRC-3"), None)
            if not emergency_clause:
                emergency_clause = clauses[0]
            context.update({
                "citation_format": emergency_clause.get("citation_format", "")
            })
        
        elif template_id == "TEMPLATE_RIGHT_TO_SECOND_OPINION" and clauses:
            second_opinion_clause = next(
                (c for c in clauses if c["id"] == "NHRC-6"), None
            )
            if not second_opinion_clause:
                second_opinion_clause = clauses[0]

            context.update({
                "citation_format": second_opinion_clause.get("citation_format", "")
            })

        elif template_id == "TEMPLATE_RIGHT_TO_NON_DISCRIMINATION" and clauses:
            non_discrimination_clause = next(
                (c for c in clauses if c["id"] == "NHRC-8"), None
            )
            if not non_discrimination_clause:
                non_discrimination_clause = clauses[0]

            context.update({
                "citation_format": non_discrimination_clause.get("citation_format", "")
            })

        elif template_id == "TEMPLATE_RIGHT_TO_TRANSPARENT_PRICING" and clauses:
            pricing_clause = next(
                (c for c in clauses if c["id"] == "NHRC-7"), None
            )
            if not pricing_clause:
                pricing_clause = clauses[0]

            context.update({
                "citation_format": pricing_clause.get("citation_format", "")
            })

        elif template_id == "TEMPLATE_RIGHT_TO_DISCHARGE_BODY" and clauses:
            discharge_clause = next(
                (c for c in clauses if c["id"] == "NHRC-15"), None
            )
            if not discharge_clause:
                discharge_clause = clauses[0]
            context.update({
                "citation_format": discharge_clause.get("citation_format", ""),
                "paraphrase": discharge_clause.get("paraphrase", "")
            })

        elif template_id == "TEMPLATE_RIGHT_TO_CLINICAL_TRIAL_PROTECTION" and clauses:
            trial_clause = next(
                (c for c in clauses if c["id"] == "NHRC-13"), None
            )
            if not trial_clause:
                trial_clause = clauses[0]
            context.update({
                "citation_format": trial_clause.get("citation_format", ""),
                "paraphrase": trial_clause.get("paraphrase", ""),
                "rights_bulleted": self.format_bullets(trial_clause.get("rights", [])),
                "obligations_bulleted": self.format_bullets(trial_clause.get("obligations", [])),
                "legal_references_bulleted": trial_clause.get("legal_references", [])
            })

        elif template_id == "TEMPLATE_RIGHT_TO_BIOMEDICAL_RESEARCH_PROTECTION" and clauses:
            research_clause = next(
                (c for c in clauses if c["id"] == "NHRC-14"), None
            )
            if not research_clause:
                research_clause = clauses[0]
            context.update({
                "citation_format": research_clause.get("citation_format", ""),
                "paraphrase": research_clause.get("paraphrase", "")
            })

        elif template_id == "TEMPLATE_RIGHT_TO_INFORMED_CONSENT" and clauses:
            consent_clause = next(
                (c for c in clauses if c["id"] == "NHRC-4"), None
            )
            if not consent_clause:
                consent_clause = clauses[0]
            context.update({
                "citation_format": consent_clause.get("citation_format", "")
            })

        elif template_id == "TEMPLATE_NO_MATCH_FOUND":
            # Get some general rights for suggestions
            general_rights = self.kb.get_clauses_by_category("access_information")
            related_rights = [c["title"] for c in general_rights[:3]]
            context.update({
                "user_query": query,
                "related_rights_list": self.format_bullets(related_rights)
            })
            
        return context
    
    def generate_response(self, user_query: str, show_proof: bool = True) -> Tuple[str, ProofTrace]:
        """Generate complete response for user query"""
        # Clean query
        cleaned_query = self.clean_query(user_query)
        normalized_query = cleaned_query

        # Step 1: Intent classification
        intents, matched_indicators = self.classifier.classify(cleaned_query)
        
        # Filter out low confidence matches (noise)
        intents = [(i, s) for i, s in intents if s >= 0.3]
        intents = intents[:3]

        if not intents:
            # Return no match template
            template_id = "TEMPLATE_NO_MATCH_FOUND"
            context = self.prepare_context(template_id, [], [], cleaned_query)
            response = self.template_engine.fill_template(template_id, context)
            proof_trace = ProofTrace(
                query=user_query,
                normalized_query=normalized_query,
                matched_intents=[],
                matched_clauses=[],
                template_used=template_id,
                variables_used=[]
            )
            disclaimer = self.template_engine.fill_template("TEMPLATE_DISCLAIMER", context)
            response = f"{response}\n\n{disclaimer}"
            if show_proof:
                response += f"\n\n{proof_trace.format()}"
            return response, proof_trace
        
        # 🚑 EMERGENCY HARD GATE - Remove emergency intent if no emergency signal
        intents = [
            (intent, score)
            for intent, score in intents
            if not (
                intent == "emergency_care"
                and not self.has_emergency_signal(cleaned_query)
            )
        ]
        
        # 🔒 FIX: Boost emergency_care to top if present with high confidence
        emergency_intents = [(i, s) for i, s in intents if i == "emergency_care" and s >= 0.8]
        other_intents = [(i, s) for i, s in intents if i != "emergency_care"]
        
        if emergency_intents:
            intents = emergency_intents + other_intents
        
        # Keep top 3
        intents = intents[:3]

        # Step 2: Knowledge retrieval - collect clauses from ALL matched intents
        matched_clauses = []
        seen_clause_ids = set()
        
        for intent, _ in intents:
            clauses = self.kb.get_clauses_by_intent(intent)
            for clause in clauses:
                if clause["id"] not in seen_clause_ids:
                    seen_clause_ids.add(clause["id"])
                    matched_clauses.append(clause)
        
        # Remove duplicates while preserving order
        unique_clauses = []
        seen_ids = set()
        for clause in matched_clauses:
            if clause["id"] not in seen_ids:
                seen_ids.add(clause["id"])
                unique_clauses.append(clause)
        
        # Limit to prevent flooding (max 3 clauses)
        unique_clauses = unique_clauses[:3]
        
        # Step 3: Template selection
        template_id = self.select_template(intents, unique_clauses)

        # Step 4: Context preparation
        context = self.prepare_context(template_id, intents, unique_clauses, cleaned_query)
        context["matched_indicators"] = matched_indicators
        context["show_proof_trace"] = show_proof
        
        # Step 5: Template filling
        response = self.template_engine.fill_template(template_id, context)
        
        # Step 6: Add additional rights note if multiple clauses exist
        if len(unique_clauses) > 1 and "additional_rights" in context:
            additional_note = "\n\n**Also relevant to your situation:**\n"
            for title in context["additional_rights"]:
                additional_note += f"• {title}\n"
            response = response + additional_note
        
        # Step 7: Ethics awareness detection - based on INTENT only
        misconduct_intents = {
            "doctor_misbehavior",
            "kickback_commission",
            "advertising_issues",
            "prescription_issues",
            "doctor_absenteeism",
        }
        
        detected_misconduct = any(
            intent in misconduct_intents for intent, _ in intents
        )

        if detected_misconduct:
            bridge_note = (
                "\n\n---\n\n"
                "*Note:* Certain concerns in your query relate to **professional conduct**, "
                "which is governed separately from patient rights. While patient rights "
                "are defined under the NHRC Charter, professional behavior of doctors is "
                "regulated under the IMC Ethics Regulations.\n"
            )
            ethics_notice = (
                "\n\n---\n\n"
                "**Professional Conduct Standards (Awareness Only)**\n\n"
                "Medical professionals are required to maintain dignity, respect, "
                "and appropriate behavior toward patients. These duties are "
                "explicitly codified under the Indian Medical Council (IMC) Ethics Regulations.\n\n"
                "**Relevant Ethical Provisions:**\n"
                "• IMC Ethics Regulations, Section 1.1.1 – Upholding the dignity and honor of the profession\n"
                "• IMC Ethics Regulations, Section 1.1.2 – Respectful and humane conduct toward patients\n"
                "• IMC Ethics Regulations, Section 1.1.3 – Proper etiquette and professional behavior\n"
                "• IMC Ethics Regulations, Section 2.1 – Obligations to the sick\n\n"
                "This system does not determine misconduct, fault, or liability. "
                "It only provides awareness of formally defined professional standards."
            )
            response = f"{response}{bridge_note}{ethics_notice}"
            
        # Step 8: Add disclaimer
        disclaimer = self.template_engine.fill_template("TEMPLATE_DISCLAIMER", context)
        response = f"{response}\n\n{disclaimer}"
        
        # Step 9: Create proof trace
        proof_trace = ProofTrace(
            query=user_query,
            normalized_query=normalized_query,
            matched_intents=intents,
            matched_clauses=unique_clauses,
            template_used=template_id,
            variables_used=list(context.keys())
        )
        
        # Step 10: Add proof trace if requested
        if show_proof:
            proof_section = f"\n\n{proof_trace.format()}"
            response += proof_section
        
        return response, proof_trace
    
    def generate_detailed_response(self, clause_id: str) -> str:
        """Generate detailed response for a specific clause"""
        clause = self.kb.get_clause_by_id(clause_id)
        if not clause:
            return f"Clause '{clause_id}' not found."
        
        context = {
            "title": clause.get("title", ""),
            "citation_format": clause.get("citation_format", ""),
            "exact_text": clause.get("exact_text", ""),
            "paraphrase": clause.get("paraphrase", ""),
            "rights_bulleted": clause.get("rights", []),
            "obligations_bulleted": clause.get("obligations", []),
            "exceptions_bulleted": clause.get("exceptions", []),
            "legal_references_bulleted": clause.get("legal_references", []),
            "timeframe_note": clause.get("timeframes", {}),
            "show_exact_text": True,
            "show_proof_trace": True
        }
        
        response = self.template_engine.fill_template("TEMPLATE_SINGLE_CLAUSE", context)
        disclaimer = self.template_engine.fill_template("TEMPLATE_DISCLAIMER", context)
        
        return f"{response}\n\n{disclaimer}"

# Test function
def test_response_assembler():
    """Test the complete response assembler"""
    assembler = ResponseAssembler()
    
    print("Response Assembler Test")
    print("=" * 70)
    
    test_queries = [
        "doctor refused to give my medical reports",
        "hospital asked for advance payment in emergency",
        "surgery done without my permission",
        "doctor shared my information with others",
        "can i get a second opinion from another doctor",
        "they overcharged me for treatment",
        "what are my rights as a patient"
    ]
    
    for i, query in enumerate(test_queries):
        print(f"\n{'='*70}")
        print(f"Test {i+1}: '{query}'")
        print(f"{'='*70}\n")
        
        response, proof_trace = assembler.generate_response(query, show_proof=True)
        print(response)
        
        # Show proof trace in compact form
        print("\n" + "=" * 50)
        print("Proof Trace Summary:")
        trace_dict = proof_trace.to_dict()
        print(f"Matched intents: {len(trace_dict['matched_intents'])}")
        print(f"Matched clauses: {len(trace_dict['matched_clauses'])}")
        print(f"Template used: {trace_dict['template_used']}")
        print("=" * 50)
        
        # Pause between tests
        if i < len(test_queries) - 1:
            input("\nPress Enter for next test...")
    
    # Test detailed response
    print(f"\n{'='*70}")
    print("Testing Detailed Response for NHRC-2:")
    print(f"{'='*70}\n")
    
    detailed_response = assembler.generate_detailed_response("NHRC-2")
    print(detailed_response[:800] + "...")
    
    return assembler


if __name__ == "__main__":
    assembler = test_response_assembler()