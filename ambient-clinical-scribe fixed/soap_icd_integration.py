from icd_rag_search import get_icd_codes


def generate_final_report(soap_note):
    """soap_note: dict with 'subjective'/'objective'/'assessment'/'plan' keys
    (the shape produced by soap_generator.generate_soap)."""

    assessment = soap_note.get("assessment") or soap_note.get("Assessment", "")

    icd_results = get_icd_codes(assessment)

    soap_note["icd_10_codes"] = icd_results

    return soap_note


# TEST SAMPLE
if __name__ == "__main__":
    sample_soap = {
        "subjective": "Patient has frequent urination and thirst",
        "objective": "High blood sugar levels",
        "assessment": "Possible diabetes mellitus with kidney complications",
        "plan": "Start insulin therapy and monitor glucose",
    }

    result = generate_final_report(sample_soap)

    print("\nFINAL OUTPUT:\n")
    print(result)