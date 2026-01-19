"""
Deterministic Intent Classifier for PC-MLRA
Updated with all 17 NHRC rights and IMC provisions
"""

import re
from typing import List, Dict, Tuple

class IntentClassifier:
    def __init__(self):
        self.intents = self._load_intents()
        
    def _load_intents(self) -> Dict:
        """Load predefined intents with keywords and patterns"""
        return {
            # NHRC Rights-based intents
            "right_to_information": {
                "keywords": ["information", "diagnosis", "explain", "tell me", "what is wrong", "condition", "treatment options"],
                "verbs": ["explain", "inform", "tell", "describe", "clarify"],
                "negative_patterns": ["didn't explain", "no information", "not telling", "refused to tell"],
                "description": "Right to information about diagnosis and treatment",
                "category": "access_information"
            },
            "access_medical_records": {
                "keywords": ["report", "record", "document", "medical file", "test result", "discharge summary", "case papers"],
                "verbs": ["get", "access", "obtain", "want", "need", "request", "copy"],
                "negative_patterns": ["refused to give", "denied access", "won't provide", "not giving"],
                "description": "Right to access medical records and reports",
                "category": "access_information"
            },
            "emergency_care": {
                "keywords": ["emergency", "urgent", "accident", "critical", "immediate", "life threatening"],
                "verbs": ["refused", "denied", "asked for payment", "demand money"],
                "negative_patterns": ["refused emergency", "asked for advance", "demanded payment", "turned away"],
                "description": "Right to emergency medical care without advance payment",
                "category": "quality_safety"
            },
            "informed_consent": {
                "keywords": ["consent", "permission", "agree", "explain", "procedure", "surgery", "operation", "risk"],
                "verbs": ["force", "pressure", "make", "without asking", "didn't tell", "performed without"],
                "negative_patterns": ["without consent", "no permission", "didn't ask", "forced me", "no explanation"],
                "description": "Right to informed consent before procedures",
                "category": "consent_autonomy"
            },
            "privacy_confidentiality": {
                "keywords": ["privacy", "confidential", "secret", "information", "data", "details", "told others"],
                "verbs": ["share", "disclose", "tell", "leak", "reveal", "expose"],
                "negative_patterns": ["shared my information", "told others", "breached privacy", "leaked"],
                "description": "Right to privacy and confidentiality",
                "category": "privacy_confidentiality"
            },
            "dignity_respect": {
                "keywords": ["dignity", "respect", "female attendant", "examination", "male doctor"],
                "verbs": ["disrespect", "humiliate", "embarrass", "examine without"],
                "negative_patterns": ["no female attendant", "examined alone", "disrespected", "humiliated"],
                "description": "Right to dignity and privacy during examination",
                "category": "privacy_confidentiality"
            },
            "second_opinion": {
                "keywords": ["second opinion", "another doctor", "consult", "different doctor", "get opinion"],
                "verbs": ["refused", "denied", "prevent", "stop", "not allow"],
                "negative_patterns": ["won't allow second opinion", "refused records", "denied second opinion"],
                "description": "Right to seek second opinion",
                "category": "quality_safety"
            },
            "transparent_pricing": {
                "keywords": ["bill", "cost", "price", "charge", "expensive", "payment", "money", "rates", "overcharge"],
                "verbs": ["overcharge", "overbill", "cheat", "fraud", "scam", "hide costs"],
                "negative_patterns": ["overcharged", "bill too high", "unfair charges", "cheated", "hidden costs"],
                "description": "Right to transparent pricing and itemized bills",
                "category": "access_information"
            },
            "non_discrimination": {
                "keywords": ["discriminate", "HIV", "caste", "religion", "gender", "age", "sexual", "poor", "rich"],
                "verbs": ["discriminate", "treat differently", "refuse because", "deny because"],
                "negative_patterns": ["discriminated against", "treated differently", "refused because"],
                "description": "Right to non-discrimination in treatment",
                "category": "quality_safety"
            },
            "medical_negligence": {
                "keywords": ["negligence", "mistake", "error", "wrong treatment", "complication", "infection", "dirty"],
                "verbs": ["neglect", "mistreat", "harm", "injure", "cause"],
                "negative_patterns": ["negligent", "made mistake", "caused infection", "unsafe"],
                "description": "Right to safety and quality care",
                "category": "quality_safety"
            },
            "treatment_choice": {
                "keywords": ["choice", "alternative", "option", "refuse treatment", "against medical advice"],
                "verbs": ["force", "pressure", "refuse to allow", "deny choice"],
                "negative_patterns": ["forced treatment", "no choice", "refused alternative"],
                "description": "Right to choose treatment options",
                "category": "consent_autonomy"
            },
            "pharmacy_choice": {
                "keywords": ["pharmacy", "medicine", "chemist", "buy medicines", "purchase drugs"],
                "verbs": ["force", "pressure", "insist", "make buy"],
                "negative_patterns": ["forced to buy", "must purchase here", "insisted on hospital pharmacy"],
                "description": "Right to choose pharmacy for medicines",
                "category": "consent_autonomy"
            },
            "referral_issues": {
                "keywords": ["referral", "transfer", "send to", "recommend", "specialist", "kickback", "commission"],
                "verbs": ["force", "pressure", "refer unnecessarily", "get commission"],
                "negative_patterns": ["forced referral", "unnecessary referral", "getting commission"],
                "description": "Right to proper referral without commercial influence",
                "category": "quality_safety"
            },
            "clinical_trial_rights": {
                "keywords": ["clinical trial", "research", "experiment", "study participant", "trial"],
                "verbs": ["force", "pressure", "mislead", "not explain"],
                "negative_patterns": ["forced into trial", "no consent for trial", "trial without explanation"],
                "description": "Rights of clinical trial participants",
                "category": "consent_autonomy"
            },
            "detention_for_payment": {
                "keywords": ["detain", "keep", "hold", "discharge", "body", "dead", "corpse", "payment dispute"],
                "verbs": ["detain", "hold", "keep", "refuse to release"],
                "negative_patterns": ["detained for payment", "won't release body", "held for bill"],
                "description": "Right to discharge and release of dead body",
                "category": "access_information"
            },
            "patient_education": {
                "keywords": ["educate", "teach", "learn", "information", "how to", "instructions"],
                "verbs": ["not explain", "not teach", "no instructions"],
                "negative_patterns": ["no education", "didn't explain", "no instructions"],
                "description": "Right to patient education",
                "category": "access_information"
            },
            "grievance_redressal": {
                "keywords": ["complain", "complaint", "grievance", "redressal", "feedback", "lodge complaint"],
                "verbs": ["refuse to accept", "ignore", "not respond", "dismiss"],
                "negative_patterns": ["won't accept complaint", "no grievance mechanism", "ignored complaint"],
                "description": "Right to grievance redressal",
                "category": "redressal_complaint"
            },
            
            # IMC-specific intents
            "doctor_misbehavior": {
                "keywords": ["abuse", "shout", "rude", "disrespectful", "yell", "insult", "arrogant", "unprofessional"],
                "verbs": ["misbehave", "abused", "shouted", "insulted", "humiliated"],
                "negative_patterns": ["shouted at me", "abused me", "was rude", "disrespected"],
                "description": "Doctor's professional misconduct",
                "category": "quality_safety"
            },
            "doctor_absenteeism": {
                "keywords": ["absent", "not available", "not present", "away", "on leave", "duty hours"],
                "verbs": ["absent", "away", "not come", "miss"],
                "negative_patterns": ["doctor not available", "absent during duty", "not present"],
                "description": "Doctor absenteeism during duty hours",
                "category": "quality_safety"
            },
            "advertising_issues": {
                "keywords": ["advertise", "publicity", "claim", "boast", "self promotion", "sign board"],
                "verbs": ["advertise", "claim", "boast", "promote"],
                "negative_patterns": ["false advertisement", "boasting", "exaggerated claims"],
                "description": "Unethical advertising by doctors",
                "category": "professional_conduct"
            },
            "kickback_commission": {
                "keywords": ["commission", "kickback", "bribe", "referral fee", "incentive", "gift"],
                "verbs": ["take", "receive", "give", "offer"],
                "negative_patterns": ["taking commission", "getting kickback", "bribed"],
                "description": "Receiving commissions or kickbacks",
                "category": "professional_conduct"
            },
            "euthanasia": {
                "keywords": ["euthanasia", "mercy killing", "end life", "withdraw treatment", "life support"],
                "verbs": ["perform", "practice", "do", "carry out"],
                "negative_patterns": ["performed euthanasia", "ended life"],
                "description": "Issues related to euthanasia",
                "category": "professional_conduct"
            },
            "sex_determination": {
                "keywords": ["sex determination", "female foeticide", "gender test", "abortion", "foetus"],
                "verbs": ["perform", "do", "conduct", "carry out"],
                "negative_patterns": ["did sex determination", "female foeticide"],
                "description": "Illegal sex determination tests",
                "category": "professional_conduct"
            },
            "prescription_issues": {
                "keywords": ["prescription", "medicine", "drug", "generic", "brand", "unnecessary", "overprescribe"],
                "verbs": ["prescribe", "give", "recommend", "suggest"],
                "negative_patterns": ["unnecessary prescription", "overprescribed", "wrong medicine"],
                "description": "Issues with medical prescriptions",
                "category": "professional_conduct"
            }
        }
    
    def clean_query(self, query: str) -> str:
        """Clean and normalize the user query"""
        query = query.lower().strip()
        query = re.sub(r'[^\w\s]', ' ', query)  # Remove punctuation
        query = re.sub(r'\s+', ' ', query)  # Normalize whitespace
        return query
    
    def classify(self, query: str) -> List[Tuple[str, float]]:
        """
        Classify query into one or more intents
        Returns list of (intent, confidence_score)
        """
        cleaned_query = self.clean_query(query)
        words = cleaned_query.split()
        
        scores = {}
        
        for intent_name, intent_data in self.intents.items():
            score = 0
            
            # Check for keywords
            for keyword in intent_data["keywords"]:
                if keyword in cleaned_query:
                    score += 2
            
            # Check for negative patterns (strong indicator)
            for pattern in intent_data["negative_patterns"]:
                if pattern in cleaned_query:
                    score += 3
            
            # Check for verbs
            for verb in intent_data.get("verbs", []):
                if verb in cleaned_query:
                    score += 1
            
            if score > 0:
                scores[intent_name] = min(score / 6.0, 1.0)  # Normalize to 0-1
        
        # Sort by confidence score
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_intents[:3]  # Return top 3 intents
    
    def get_intent_details(self, intent_name: str) -> Dict:
        """Get detailed information about a specific intent"""
        return self.intents.get(intent_name, {})
    
    def get_intents_by_category(self, category: str) -> List[str]:
        """Get all intents belonging to a specific category"""
        return [intent for intent, data in self.intents.items() 
                if data.get("category") == category]


# Quick test function
def test_classifier():
    classifier = IntentClassifier()
    
    test_queries = [
        "I want my medical reports but doctor refused to give",
        "Doctor performed surgery without my consent",
        "The doctor shouted at me and was very rude",
        "Hospital shared my information with others",
        "I was overcharged for my treatment",
        "They refused emergency treatment asking for advance payment",
        "Doctor forced me to buy medicines from hospital pharmacy",
        "Hospital detained me for not paying bill",
        "Doctor didn't explain risks before surgery",
        "They discriminated against me because of my HIV status"
    ]
    
    print("Testing Intent Classifier:")
    print("=" * 70)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        intents = classifier.classify(query)
        for intent, confidence in intents:
            details = classifier.get_intent_details(intent)
            print(f"  - {intent}: {confidence:.2f} ({details['description']})")


if __name__ == "__main__":
    test_classifier()