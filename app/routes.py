from __future__ import annotations

from decimal import Decimal

from flask import Blueprint, jsonify, render_template, request

from .expert_system import DISEASE_INFO, SYMPTOMS, evaluate_symptoms
from .models import Disease, Evaluation, EvaluationSymptom, Symptom, db


main_bp = Blueprint("main", __name__)


def _extract_symptoms(payload: dict) -> list[str]:
    symptoms = payload.get("symptoms", [])
    if isinstance(symptoms, str):
        return [item.strip() for item in symptoms.split(",") if item.strip()]
    if isinstance(symptoms, list):
        return [str(item).strip() for item in symptoms if str(item).strip()]
    return []


def _store_evaluation(result: dict, payload: dict) -> int | None:
    disease = Disease.query.filter_by(code=DISEASE_INFO["code"]).first()
    if disease is None:
        raise RuntimeError("Disease seed data is missing.")

    evaluation = Evaluation(
        disease_id=disease.id,
        patient_name=str(payload.get("patient_name", "")).strip() or None,
        risk_level=result["risk_level"],
        probable_diagnosis=result["probable_diagnosis"],
        confidence_score=Decimal(str(result["confidence_score"])),
        matched_rule=result["matched_rule"],
        notes=str(payload.get("notes", "")).strip() or None,
        selected_symptom_codes=", ".join(symptom["code"] for symptom in result["selected_symptoms"]),
        recommendations="\n".join(result["recommendations"]),
    )
    db.session.add(evaluation)
    db.session.flush()

    symptom_codes = [symptom["code"] for symptom in result["selected_symptoms"]]
    if symptom_codes:
        symptoms = Symptom.query.filter(Symptom.code.in_(symptom_codes)).all()
        for symptom in symptoms:
            db.session.add(
                EvaluationSymptom(
                    evaluation_id=evaluation.id,
                    symptom_id=symptom.id,
                )
            )

    db.session.commit()
    return evaluation.id


@main_bp.get("/")
def index():
    return render_template(
        "index.html",
        symptoms=SYMPTOMS,
        disease=DISEASE_INFO,
    )


@main_bp.get("/health")
def health():
    return jsonify({"status": "ok", "disease": DISEASE_INFO["name"]})


@main_bp.post("/api/evaluate")
def api_evaluate():
    payload = request.get_json(silent=True)
    if payload is None:
        payload = {
            "patient_name": request.form.get("patient_name", ""),
            "notes": request.form.get("notes", ""),
            "symptoms": request.form.getlist("symptoms"),
        }

    selected_symptoms = _extract_symptoms(payload)
    if not selected_symptoms:
        return jsonify({"error": "Debes seleccionar al menos un síntoma."}), 400

    result = evaluate_symptoms(selected_symptoms)

    try:
        evaluation_id = _store_evaluation(result, payload)
        storage_warning = None
    except Exception as exc:  # pragma: no cover - graceful degradation for misconfigured DB
        db.session.rollback()
        evaluation_id = None
        storage_warning = f"No se pudo registrar la evaluación en la base de datos: {exc}"

    response = {
        **result,
        "evaluation_id": evaluation_id,
        "storage_warning": storage_warning,
    }

    return jsonify(response)
