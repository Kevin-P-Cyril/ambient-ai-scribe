def recommend_icd(assessment):

    assessment = assessment.lower()

    icd_database = {
        "viral infection": {
            "code": "B34.9",
            "description": "Viral infection, unspecified"
        },
        "viral illness": {
            "code": "B34.9",
            "description": "Viral infection, unspecified"
        },
        "headache": {
            "code": "R51.9",
            "description": "Headache"
        },
        "fever": {
            "code": "R50.9",
            "description": "Fever, unspecified"
        },
        "febrile": {
            "code": "R50.9",
            "description": "Fever, unspecified"
        }
    }

    recommendations = []

    for keyword, data in icd_database.items():
        if keyword in assessment:
            recommendations.append(data)

    return recommendations