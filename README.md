# X-Road Property Grounding Agent

## Project Purpose
This project supports my Master’s thesis research on extracting real-life value distributions from Estonian X-Road data services to inform synthetic e-Government data generation.

The goal is to develop and evaluate a systematic approach for:
* **Interpreting** X-Road service property descriptions.
* **Identifying** corresponding real-world open datasets.
* **Deriving** empirical assign counts.
* **Documenting** grounding traceability.

### Service Analyzed
The primary service analyzed in this repository is:
* **Äriregister `erakonnaNimekiri_v1`** (Political party registry data service)

---

## How Semantic Meanings Are Derived
Property semantic meanings are derived using a locally deployed LLM (**Llama3 via Ollama**)

The model is constrained with a strict system prompt to:
* Interpret the property strictly within the provided JSON structure.
* Avoid hallucinating unrelated domains.
* Prefer literal Estonian linguistic interpretation.
* Respect hierarchical structure (e.g., `keha.liikmed.item.eesnimi`)

> **Note:** The LLM output is not accepted automatically, All interpretations are manually validated before empirical grounding.

---

## How Grounding Is Performed
For each property, the following process is applied:

1.  The semantic meaning is identified.
2.  Estonian and English search keywords are generated.
3.  The **Estonian Open Data Portal** is searched.
4.  Potential datasets are evaluated manually.
5.  Filtering steps are documented.
6.  Real-world value distributions are observed.
7.  Assign count suggestions are derived.

### Example Grounding
* **Property:** Political party registry code (`keha.kood`)
* **Source:** The ERJK open dataset was used.
* **Observation:** Filtering 2025 data showed **13 political parties** reporting income.
* **Suggestion:** Assign 13 unique values in the range of `^\d{1,8}$`.

All filtering steps and links are documented in the **Property Grounding Document**.

---

## Limitations
* **API Metadata:** Some properties represent technical metadata and are not empirically groundable.
* **Sensitive Data:** Some properties represent protected personal data (e.g., personal ID codes).
* **Data Granularity:** Open datasets may not expose exact submission dates, only reporting periods.
* **Manual Validation:** LLM interpretation may require manual correction; the approach is currently semi-automated.

---

## Repository Contents

* `agent.py` - LLM-based semantic interpretation script
* `prompt.txt` - Controlled system prompt
* `properties.txt` - Property list input file
* `results.csv` - Classification output
* `Property_Grounding_Document.pdf` - Full grounding documentation
