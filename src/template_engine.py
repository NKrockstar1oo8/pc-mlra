"""
Template Engine for PC-MLRA
Deterministic template-based response generation
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ComponentType(Enum):
    HEADER = "header"
    CITATION = "citation"
    EXACT_TEXT = "exact_text"
    PARAPHRASE = "paraphrase"
    RIGHTS_LIST = "rights_list"
    OBLIGATIONS_LIST = "obligations_list"
    EXCEPTIONS = "exceptions"
    LEGAL_REFERENCES = "legal_references"
    TIMEFRAME_NOTE = "timeframe_note"
    ACTIONABLE_ADVICE = "actionable_advice"
    MESSAGE = "message"
    SUGGESTIONS = "suggestions"
    CLARIFICATION_REQUEST = "clarification_request"
    DIVIDER = "divider"
    DISCLAIMER = "disclaimer"
    INTRODUCTION = "introduction"
    SUMMARY = "summary"
    CLAUSES_LIST = "clauses_list"

@dataclass
class TemplateComponent:
    type: ComponentType
    text: str
    condition: Optional[str] = None
    style: Optional[str] = None

class TemplateEngine:
    def __init__(self, template_file: str = "data/templates/response_templates.json"):
        self.templates = self._load_templates(template_file)
        
    def _load_templates(self, template_file: str) -> Dict:
        """Load templates from JSON file"""
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Template file not found: {template_file}")
            return {"templates": {}}
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get a specific template by ID"""
        return self.templates.get("templates", {}).get(template_id)
    
    def format_bulleted_list(self, items: List[str]) -> str:
        """Format a list of items as bullet points"""
        if not items:
            return "None specified"
        return "\n".join([f"• {item}" for item in items])
    
    def format_legal_references(self, references: List[str]) -> str:
        """Format legal references"""
        if not references:
            return "No additional references"
        return "\n".join([f"• {ref}" for ref in references])
    
    def format_timeframe_note(self, timeframes: Dict) -> str:
        """Format timeframe information"""
        if not timeframes:
            return ""
        notes = []
        for key, value in timeframes.items():
            notes.append(f"{key.replace('_', ' ').title()}: {value}")
        return "; ".join(notes)
    
    def process_condition(self, condition: str, context: Dict) -> bool:
        """Evaluate a condition based on context"""
        if not condition:
            return True
        
        conditions = {
            "has_rights": lambda ctx: bool(ctx.get("rights")),
            "has_obligations": lambda ctx: bool(ctx.get("obligations")),
            "has_exceptions": lambda ctx: bool(ctx.get("exceptions")),
            "has_legal_references": lambda ctx: bool(ctx.get("legal_references")),
            "has_timeframes": lambda ctx: bool(ctx.get("timeframes")),
            "show_exact_text": lambda ctx: ctx.get("show_exact_text", False),
            "show_proof_trace": lambda ctx: ctx.get("show_proof_trace", True)
        }
        
        if condition in conditions:
            return conditions[condition](context)
        
        # Handle custom conditions
        if condition.startswith("has_"):
            key = condition[4:]  # Remove "has_"
            return bool(context.get(key))
        
        return True
    
    def fill_template(self, template_id: str, context: Dict) -> str:
        """Fill a template with context data"""
        template = self.get_template(template_id)
        if not template:
            return f"Template '{template_id}' not found."
        
        components = template.get("components", [])
        result_parts = []
        
        for component in components:
            # Check condition
            condition = component.get("condition")
            if not self.process_condition(condition, context):
                continue
            
            # Get component text
            component_text = component.get("text", "")
            
            # Replace variables in component text
            filled_text = self._replace_variables(component_text, context, component.get("type"))
            
            # Apply styling if needed
            filled_text = self._apply_styling(filled_text, component.get("style"))
            
            if filled_text:
                result_parts.append(filled_text)
        
        return "\n\n".join(result_parts)
    
    def _replace_variables(self, text: str, context: Dict, component_type: str) -> str:
        """Replace variables in text with context values"""
        # Find all variables in the format {variable_name}
        variables = re.findall(r'\{(\w+)\}', text)
        
        for var in variables:
            value = self._get_variable_value(var, context, component_type)
            text = text.replace(f"{{{var}}}", str(value))
        
        return text
    
    def _get_variable_value(self, var: str, context: Dict, component_type: str) -> str:
        """Get the value for a variable, with formatting if needed"""
        value = context.get(var, "")
        
        # Apply formatting based on variable type
        if var.endswith("_bulleted"):
            if isinstance(value, list):
                return self.format_bulleted_list(value)
        
        elif var == "legal_references_bulleted":
            if isinstance(value, list):
                return self.format_legal_references(value)
        
        elif var == "timeframe_note":
            if isinstance(value, dict):
                return self.format_timeframe_note(value)
        
        elif var == "rights" and isinstance(value, list):
            # Convert right codes to readable text
            readable_rights = []
            for right in value:
                readable = right.replace("_", " ").title()
                readable_rights.append(readable)
            return ", ".join(readable_rights)
        
        elif var == "obligations" and isinstance(value, list):
            # Convert obligation codes to readable text
            readable_obligations = []
            for obligation in value:
                readable = obligation.replace("_", " ").title()
                readable_obligations.append(readable)
            return ", ".join(readable_obligations)
        
        elif var == "exceptions" and isinstance(value, list):
            # Convert exception codes to readable text
            readable_exceptions = []
            for exception in value:
                readable = exception.replace("_", " ").title()
                readable_exceptions.append(readable)
            return ", ".join(readable_exceptions)
        
        return str(value) if value is not None else ""
    
    def _apply_styling(self, text: str, style: Optional[str]) -> str:
        """Apply text styling"""
        if not style:
            return text
        
        styles = {
            "h1": lambda t: f"# {t}",
            "h2": lambda t: f"## {t}",
            "h3": lambda t: f"### {t}",
            "bold": lambda t: f"**{t}**",
            "italic": lambda t: f"*{t}*"
        }
        
        if style in styles:
            return styles[style](text)
        
        return text
    
    def generate_clause_summary(self, clause: Dict) -> str:
        """Generate a summary of a clause for use in lists"""
        summary_template = "**{title}** ({document} Section {section})\n{paraphrase}\n"
        
        context = {
            "title": clause.get("title", ""),
            "document": clause.get("document_abbr", ""),
            "section": clause.get("section", ""),
            "paraphrase": clause.get("paraphrase", "")
        }
        
        return self._replace_variables(summary_template, context, "clause_summary")
    
    def generate_multiple_clauses_list(self, clauses: List[Dict]) -> str:
        """Generate a formatted list of multiple clauses"""
        if not clauses:
            return "No relevant clauses found."
        
        clause_summaries = []
        for clause in clauses:
            summary = self.generate_clause_summary(clause)
            clause_summaries.append(summary)
        
        return "\n---\n".join(clause_summaries)


# Test function
def test_template_engine():
    """Test the template engine with sample data"""
    engine = TemplateEngine()
    
    print("Template Engine Test")
    print("=" * 70)
    
    # Test 1: Single clause template
    print("\n1. Testing Single Clause Template:")
    
    sample_clause = {
        "title": "Right to Access Medical Records",
        "citation_format": "NHRC Charter, Right 2",
        "exact_text": "Every patient or his caregiver has the right to access originals/copies of case papers...",
        "paraphrase": "Patients can get copies of their medical documents within specified timeframes.",
        "rights": ["access_medical_records", "obtain_documents", "discharge_summary"],
        "obligations": ["hospital_provide_records", "doctor_maintain_records"],
        "exceptions": ["ongoing_legal_cases"],
        "legal_references": [
            "Annexure 8 of standards for Hospital level 1",
            "MCI Code of Ethics section 1.3.2"
        ],
        "timeframes": {
            "during_admission": "preferably within 24 hours",
            "after_discharge": "within 72 hours"
        }
    }
    
    context = {
        "title": sample_clause["title"],
        "citation_format": sample_clause["citation_format"],
        "exact_text": sample_clause["exact_text"],
        "paraphrase": sample_clause["paraphrase"],
        "rights_bulleted": sample_clause["rights"],
        "obligations_bulleted": sample_clause["obligations"],
        "exceptions_bulleted": sample_clause["exceptions"],
        "legal_references_bulleted": sample_clause["legal_references"],
        "timeframe_note": sample_clause["timeframes"],
        "show_exact_text": True
    }
    
    result = engine.fill_template("TEMPLATE_SINGLE_CLAUSE", context)
    print(result[:500] + "...")  # Show first 500 chars
    
    # Test 2: Specialized template
    print("\n2. Testing Specialized Right to Records Template:")
    
    context2 = {
        "citation_format": "NHRC Charter, Right 2"
    }
    
    result2 = engine.fill_template("TEMPLATE_RIGHT_TO_RECORDS", context2)
    print(result2[:300] + "...")
    
    # Test 3: No match template
    print("\n3. Testing No Match Template:")
    
    context3 = {
        "user_query": "can hospital keep my belongings",
        "related_rights_list": ["Right to Information", "Right to Privacy", "Right to Safety"]
    }
    
    result3 = engine.fill_template("TEMPLATE_NO_MATCH_FOUND", context3)
    print(result3)
    
    # Test 4: Formatting functions
    print("\n4. Testing Formatting Functions:")
    
    items = ["First item", "Second item", "Third item"]
    bulleted = engine.format_bulleted_list(items)
    print(f"Bulleted list:\n{bulleted}")
    
    # Test 5: Clause summary
    print("\n5. Testing Clause Summary Generation:")
    
    clause_summary = engine.generate_clause_summary(sample_clause)
    print(clause_summary)
    
    return engine


if __name__ == "__main__":
    engine = test_template_engine()