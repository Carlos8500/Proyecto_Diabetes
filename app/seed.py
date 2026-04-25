from __future__ import annotations

from .expert_system import DISEASE_INFO, SYMPTOMS
from .models import Disease, Symptom, db


def seed_reference_data() -> None:
    disease = Disease.query.filter_by(code=DISEASE_INFO["code"]).first()

    if disease is None:
        disease = Disease(
            code=DISEASE_INFO["code"],
            name=DISEASE_INFO["name"],
            description=DISEASE_INFO["summary"],
        )
        db.session.add(disease)
        db.session.flush()
    else:
        disease.name = DISEASE_INFO["name"]
        disease.description = DISEASE_INFO["summary"]

    existing_symptoms = {symptom.code: symptom for symptom in Symptom.query.all()}

    for item in SYMPTOMS:
        symptom = existing_symptoms.get(item["code"])
        if symptom is None:
            symptom = Symptom(
                disease_id=disease.id,
                code=item["code"],
                name=item["name"],
                description=item["description"],
                weight=item["weight"],
            )
            db.session.add(symptom)
            continue

        symptom.disease_id = disease.id
        symptom.name = item["name"]
        symptom.description = item["description"]
        symptom.weight = item["weight"]

    db.session.commit()

