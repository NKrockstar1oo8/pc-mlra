"""
Configuration settings for PC-MLRA
"""

# Document sources
DOCUMENTS = {
    "nhrc_patient_charter": {
        "name": "NHRC Patient Charter",
        "abbreviation": "NHRC",
        "source": "data/raw_documents/nhrc_patient_charter.pdf"
    },
    "imc_ethics_code": {
        "name": "IMC Ethics Code",
        "abbreviation": "IMC", 
        "source": "data/raw_documents/imc_ethics_code.pdf"
    }
}

# Categories for rights classification
RIGHT_CATEGORIES = {
    "access_information": "Access & Information Rights",
    "consent_autonomy": "Consent & Autonomy Rights", 
    "privacy_confidentiality": "Privacy & Confidentiality Rights",
    "quality_safety": "Quality & Safety Rights",
    "redressal_complaint": "Redressal & Complaint Rights"
}

# Actors in the system
ACTORS = {
    "patient": "Patient/Healthcare Consumer",
    "doctor": "Doctor/Physician",
    "hospital": "Hospital/Healthcare Institution",
    "nurse": "Nursing Staff",
    "administrator": "Hospital Administrator"
}

# Response disclaimer
DISCLAIMER = """
---
**Disclaimer**: This system provides information about medical rights and obligations based on established documents. It does not constitute legal advice. For specific legal situations, consult a qualified legal professional.
"""