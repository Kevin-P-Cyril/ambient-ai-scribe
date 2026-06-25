from icd_rag_search import get_icd_codes

def generate_final_report(soap_note):
    """
    soap_note = dict from Week 2 output
    """

    assessment = soap_note["Assessment"]

    icd_results = get_icd_codes(assessment)

    soap_note["ICD_10_Codes"] = icd_results

    return soap_note


# TEST SAMPLE
if __name__ == "__main__":
    sample_soap = {
        "Subjective": "Patient has frequent urination and thirst",
        "Objective": "High blood sugar levels",
        "Assessment": "Possible diabetes mellitus with kidney complications",
        "Plan": "Start insulin therapy and monitor glucose"
    }

    result = generate_final_report(sample_soap)

    print("\nFINAL OUTPUT:\n")
    print(result)