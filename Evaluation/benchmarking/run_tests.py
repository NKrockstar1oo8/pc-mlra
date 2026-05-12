from src.response_assembler import ResponseAssembler
import json

assembler = ResponseAssembler()

queries = [
    "doctor not giving my medical records",
    "hospital refused to provide discharge summary",
    "I asked for reports but they denied",
    "can I get my medical file copy",
    "hospital not sharing test results",

    "hospital refused emergency treatment",
    "they asked money before treating accident case",
    "doctor denied urgent care",
    "no treatment given in emergency",
    "patient was turned away in critical condition",

    "surgery done without my consent",
    "doctor did not explain risks before operation",
    "procedure performed without permission",
    "they forced me into surgery",
    "no consent taken before treatment",

    "doctor shared my medical information",
    "my reports were discussed publicly",
    "hospital leaked my HIV status",
    "no privacy during examination",
    "doctor told others about my condition",

    "doctor not allowing second opinion",
    "hospital refused to give records for second opinion",
    "can I consult another doctor",
    "they prevented me from getting second opinion",
    "doctor said I cannot go elsewhere",

    "hospital overcharged me",
    "bill is too high and unclear",
    "hidden charges added in bill",
    "they did not give itemized bill",
    "hospital charging extra money",

    "doctor refused treatment because of religion",
    "hospital discriminated based on HIV",
    "unequal treatment given to poor patient",
    "doctor treated me badly due to caste",
    "denied care because of illness",

    "hospital caused infection due to poor hygiene",
    "doctor made mistake in treatment",
    "unsafe equipment used",
    "patient harmed due to negligence",
    "poor safety in hospital",

    "doctor forced me to go to another hospital",
    "unnecessary referral for money",
    "hospital sending patients for commission",
    "referred me without reason",
    "doctor pushing me to specific clinic",

    "doctor behaved badly",
    "something wrong happened in hospital",
    "I feel cheated by hospital",
    "doctor shouted at me",
    "hospital not helping me"
]

results = []

for q in queries:
    response, proof = assembler.generate_response(q)

    results.append({
        "query": q,
        "intent": proof.matched_intents,
        "clauses": [c["id"] for c in proof.matched_clauses],
        "template": proof.template_used
    })

with open("pcmlra_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("✅ Done! All 50 queries executed automatically.")