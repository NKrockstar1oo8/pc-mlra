"""
Deterministic Intent Classifier for PC-MLRA
Updated with all 17 NHRC rights and IMC provisions
"""

import re
from typing import List, Dict, Tuple

class IntentClassifier:
    """
    Deterministic rule-based intent classifier.
    NHRC intents are priority-governed.
    """
    INTENT_PRIORITY = [
        # 🔴 Absolute protections
        "detained_for_payment",        # NHRC-15
        "body_withheld",               # NHRC-15

        # 🔴 Research protections
        "clinical_trial_rights",       # NHRC-13
        "biomedical_research",         # NHRC-14
        "research_rights",             # NHRC-14

        # 🔴 Emergency overrides autonomy
        "emergency_care",              # NHRC-3

        # 🔴 Referral integrity (IMPORTANT)
        "proper_referral",             # NHRC-12
        "referral_issues",             # NHRC-12
        "kickback_commission",         # NHRC-12

        # 🟡 Autonomy & choice
        "choice_of_source",            # NHRC-11
        "treatment_choice",            # NHRC-10
        "second_opinion",              # NHRC-6

        # 🟡 Equality & safety
        "non_discrimination",          # NHRC-8
        "patient_safety",              # NHRC-9

        # 🟡 Consent & education
        "patient_education",           # NHRC-16
        "informed_consent",            # NHRC-4
        
        # 🟢 Generic fallback
        "right_to_information"         # NHRC-1
    ]

    def __init__(self):
        self.intents = self._load_intents()
        
    def _load_intents(self) -> Dict:
        """Load predefined intents with keywords and patterns"""
        return {
            
            # NHRC Rights-based intents
            "biomedical_research": {
                "keywords": [
                    "biomedical research",
                    "health research",
                    "medical research",
                    "human research"
                ],
                "verbs": ["conducted", "involved", "participated"],
                "negative_patterns": [
                    "without ethics approval",
                    "no ethics committee",
                    "no consent"
                ],
                "description": "Rights related to biomedical and health research",
                "category": "consent_autonomy"
            },

            "research_rights": {
                "keywords": [
                    "ethics committee",
                    "informed consent",
                    "vulnerable",
                    "research participant",
                    "compensation"
                ],
                "verbs": ["forced", "enrolled", "participated"],
                "negative_patterns": [
                    "forced into research",
                    "no consent",
                    "not compensated"
                ],
                "description": "Protection of participants in biomedical research",
                "category": "consent_autonomy"
            },

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
                "negative_patterns": ["overcharged", "bill too high", "unfair charges", "cheated", "hidden costs", "charging too much", "extra charges added", "paid more than expected"],
                "description": "Right to transparent pricing and itemized bills",
                "category": "access_information"
            },
            "choice_of_source": {
                "keywords": [
                    "pharmacy", "chemist", "medicine",
                    "lab", "diagnostic", "test",
                    "outside", "anywhere", "choice"
                ],
                "verbs": [
                    "force", "compel", "restrict",
                    "deny", "insist", "pressure"
                ],
                "negative_patterns": [
                    "forced to buy",
                    "told to buy here only",
                    "not allowed outside",
                    "refused lab choice",
                    "forced pharmacy"
                ],
                "description": "Right to choose pharmacy or diagnostic center",
                "category": "consent_autonomy"
            },
            "non_discrimination": {
                "keywords": ["HIV status", "hiv", "AIDS", "aids", "positive", "disease based", "illness based", "discrimination","discriminated", "unequal", "unfair", "biased", "bias", "treated differently", "denied because", "refused because", "discriminate", "HIV", "caste", "religion", "gender", "age", "sexual", "poor", "rich"],
                "verbs": ["discriminate", "treat differently", "refuse because", "deny because"],
                "negative_patterns": ["denied care due to HIV", "refused treatment due to HIV", "because of HIV", "because of my illness", "because of my disease", "refused treatment because", "denied care because", "discriminated against", "treated unfairly", "discriminated against", "treated differently", "refused because"],
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
            "proper_referral": {
                "keywords": [
                    "referral", "transfer", "sent to another hospital",
                    "higher center", "continuity of care"
                ],
                "verbs": [
                    "referred", "transferred", "shifted"
                ],
                "negative_patterns": [
                    "forced referral",
                    "referral for commission",
                    "sent for money",
                    "commercial referral"
                ],
                "description": "Right to proper referral and continuity of care",
                "category": "quality_safety"
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
            "trial_compensation": {
                "keywords": [
                    "adverse effect", "side effect", "injury",
                    "compensation", "death during trial", "harm"
                ],
                "verbs": [
                    "suffered", "injured", "died", "affected"
                ],
                "negative_patterns": [
                    "no compensation", "refused compensation",
                    "denied treatment after trial"
                ],
                "description": "Compensation and care for injuries during clinical trials",
                "category": "consent_autonomy"
            },
            "treatment_choice": {
                "keywords": [
                    "against meical advice",
                    "alternative",
                    "choice",
                    "offer",
                    "alternative treatment",
                    "other treatment",
                    "treatment options",
                    "ayurveda",
                    "homeopathy",
                    "ayush",
                    "different treatment"
                ],
                "verbs": [
                    "choose",
                    "opt",
                    "prefer"
                ],
                "negative_patterns": [
                    "not allowed to choose treatment",
                    "doctor forced treatment"
                ],
                "description": "Right to choose between available treatment options",
                "category": "autonomy"
            },
            "patient_education": {
                "keywords": [
                    "education",
                    "health education",
                    "patient education",
                    "insurance",
                    "grievance",
                    "rights and responsibilities",
                    "health scheme",
                    "ayushman",
                    "insurance scheme"
                ],
                "verbs": [
                    "educate",
                    "explain",
                    "inform",
                    "tell"
                ],
                "negative_patterns": [
                    "not given education",
                    "not educated",
                    "never educated",
                    "did not explain",
                    "did not inform",
                    "no health education",
                    "not told my rights"
                ],
                "description": "Right to patient education under NHRC-16",
                "category": "access_information"
            },
            "patient_safety": {
                "keywords": ["unsafe", "infection", "hygiene", "dirty ward", "medical error", "unsafe care", "poor safety", "hospital negligence"],
                "verbs": ["infected", "neglected", "ignored safety", "used unclean equipment"],
                "negative_patterns": ["caught infection in hospital", "unsafe treatment","poor quality care"],
                "description": "Right to safe and quality medical care",
                "category": "quality_safety"
            },
            "grievance_redressal": {
                "keywords": ["mechanism", "complain", "complaint", "grievance", "redressal", "feedback", "lodge complaint"],
                "verbs": ["file", "lodge", "refuse to accept", "ignore", "not respond", "dismiss"],
                "negative_patterns": ["won't accept complaint", "no grievance mechanism", "ignored complaint", "complaint ignored", "no response to complaint"],
                "description": "Right to be heard and seek redressal",
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
            "detained_for_payment": {
                "keywords": [
                    "detain", "detained", "discharge", "not discharging",
                    "refused discharge", "held", "held in hospital",
                    "not allowed to leave", "cannot leave",
                    "payment dispute", "bill pending", "payment pending"
                ],
                "verbs": ["detain", "hold", "refuse"],
                "negative_patterns": [
                    "not discharging",
                    "not discharging due to bill",
                    "detained for payment",
                    "asked to pay before discharge",
                    "because bill is pending",
                    "held because bill"
                ],
                "description": "Illegal detention of patient for payment or billing dispute",
                "category": "quality_safety"
            },

            "body_withheld": {
                "keywords": [
                    "dead body", "body", "mortuary", "released body", "hand over body"
                ],
                "verbs": ["withhold", "refuse", "detain"],
                "negative_patterns": [
                    "not giving body",
                    "body withheld for payment",
                    "asked to pay before body"
                ],
                "description": "Dead body withheld due to payment dispute",
                "category": "access_information"
            },
            "advertising_issues": {
                "keywords": ["advertise", "publicity", "claim", "boast", "self promotion", "sign board"],
                "verbs": ["advertise", "claim", "boast", "promote"],
                "negative_patterns": ["false advertisement", "boasting", "exaggerated claims"],
                "description": "Unethical advertising by doctors",
                "category": "professional_conduct"
            },
            "kickback_commission": {
                "keywords": ["commission", "kickback", "referral money"],
                "verbs": ["received commission", "paid commission"],
                "negative_patterns": ["took commission", "illegal commission"],
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
                "keywords": ["prescription", "drug", "medicine"],
                "verbs": ["illegal prescription", "wrong prescription"],
                "negative_patterns": ["forged prescription"],
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
        # 🔒 HARD LEGAL OVERRIDE: Commercial referral beats choice-of-source
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
        def priority_key(item):
            intent, score = item
            try:
                priority = self.INTENT_PRIORITY.index(intent)
            except ValueError:
                priority = len(self.INTENT_PRIORITY)
            return (priority, -score)

        # Sort by NHRC priority + confidence
        sorted_intents = sorted(scores.items(), key=priority_key)

        # 🔒 HARD LEGAL OVERRIDES (Statutory hierarchy)
        intent_names = [i[0] for i in sorted_intents]
        
        # 🔒 HARD LEGAL OVERRIDE — NHRC-15 beats pricing & records
        if any(i in intent_names for i in {"detained_for_payment", "body_withheld"}):
            sorted_intents.sort(
                key=lambda x: 0 if x[0] in {"detained_for_payment", "body_withheld"} else 1
            )

        # NHRC-13 (Clinical Trials) highest
        if "clinical_trial_rights" in intent_names:
            sorted_intents.sort(
                key=lambda x: 0 if x[0] == "clinical_trial_rights" else 1
            )

        # NHRC-14 (Biomedical Research) next
        elif any(i in intent_names for i in {"biomedical_research", "research_rights"}):
            sorted_intents.sort(
                key=lambda x: 0 if x[0] in {"biomedical_research", "research_rights"} else 1
            )

        # NHRC-12 beats NHRC-11
        elif any(i in intent_names for i in {"kickback_commission", "referral_issues", "proper_referral"}):
            sorted_intents.sort(
                key=lambda x: 0 if x[0] in {"kickback_commission", "referral_issues", "proper_referral"} else 1
            )

        return sorted_intents[:3]

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