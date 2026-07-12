import re

_ICD_MAP = [
    ('diabetes', 'E11.9', 'Type 2 diabetes mellitus without complications'),
    ('hypertension', 'I10', 'Essential (primary) hypertension'),
    ('asthma', 'J45.909', 'Unspecified asthma, uncomplicated'),
    ('pneumonia', 'J18.9', 'Pneumonia, unspecified organism'),
    ('chest pain', 'R07.9', 'Chest pain, unspecified'),
    ('headache', 'R51', 'Headache'),
    ('fever', 'R50.9', 'Fever, unspecified'),
    ('back pain', 'M54.5', 'Low back pain'),
    ('depression', 'F32.9', 'Major depressive disorder, single episode, unspecified'),
    ('anxiety', 'F41.9', 'Anxiety disorder, unspecified'),
]


def get_icd_codes(text):
    normalized = text.lower()
    results = []

    for keyword, code, description in _ICD_MAP:
        if keyword in normalized:
            results.append({'code': code, 'description': description})
        if len(results) == 3:
            break

    if not results:
        results = [
            {'code': 'R69', 'description': 'Illness, unspecified'},
            {'code': 'Z71.1', 'description': 'Person with feared health complaint in whom no diagnosis is made'},
            {'code': 'Z00.00', 'description': 'Encounter for general adult medical examination without abnormal findings'},
        ]

    return results


# TEST
if __name__ == "__main__":
    test = "patient has high blood sugar and frequent urination"
    result = get_icd_codes(test)

    print("\nTOP ICD CODES:\n")
    for r in result:
        print(r["code"], ":", r["description"])