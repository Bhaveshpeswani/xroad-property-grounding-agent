import json
import csv
from langchain_ollama import OllamaLLM

MODEL_NAME = "llama3"
SERVICE_NAME = "Äriregister erakonnaNimekiri_v1"
JSON_FILE = "Äriregister_erakonnaNimekiri_v1.json"

llm = OllamaLLM(model=MODEL_NAME, temperature=0)

with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open("properties.txt", "r", encoding="utf-8") as f:
    properties = [line.strip() for line in f if line.strip()]

with open(JSON_FILE, "r", encoding="utf-8") as f:
    service_json = json.load(f)

json_snippet = json.dumps(service_json, indent=2)[:2000]

def safe_json_parse(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except:
        return None

def deterministic_override(prop, classification, groundable):
    prop_lower = prop.lower()

    # RULE 1
    if prop_lower.startswith("paring."):
        return "Technical/API parameter", "No"

    # RULE 2
    if "lehekylg" in prop_lower:
        return "Derived/metadata", "No"

    # RULE 3
    if "isikukood" in prop_lower:
        return "Sensitive personal data", "No"

    # RULE 4
    if "eesnimi" in prop_lower or "perenimi" in prop_lower:
        return "Real-world entity", "Yes"

    # RULE 5
    if "kpv" in prop_lower or "aeg" in prop_lower:
        return "Real-world entity", "Yes"

    # RULE 6
    if "kood" in prop_lower:
        return "Real-world entity", "Yes"

    return classification, groundable

with open("results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Property",
        "Semantic Meaning",
        "Final Classification",
        "Final Empirically Groundable",
        "Suggested Keywords",
        "LLM Confidence"
    ])

    for prop in properties:
        print(f"Analyzing: {prop}")

        prompt = f"""
{SYSTEM_PROMPT}

Data Service Name:
{SERVICE_NAME}

Service JSON Structure Snippet:
{json_snippet}

Property to analyze:
{prop}
"""

        response = llm.invoke(prompt)
        data = safe_json_parse(response)

        if data:
            llm_class = data.get("classification", "Uncertain")
            llm_ground = data.get("empirically_groundable", "No")

            final_class, final_ground = deterministic_override(
                prop,
                llm_class,
                llm_ground
            )

            writer.writerow([
                prop,
                data.get("semantic_meaning"),
                final_class,
                final_ground,
                data.get("suggested_keywords"),
                data.get("confidence")
            ])
        else:
            print("JSON parsing failed.")

print("Done. Check results.csv")
