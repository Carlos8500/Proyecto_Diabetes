from __future__ import annotations

from typing import Iterable


DISEASE_INFO = {
    "code": "diabetes_mellitus",
    "name": "Diabetes Mellitus",
    "summary": (
        "Enfermedad metabólica crónica caracterizada por niveles elevados de glucosa "
        "en sangre por alteraciones en la producción o uso de la insulina."
    ),
}

SYMPTOMS = [
    {
        "code": "sed_excesiva",
        "name": "Sed excesiva",
        "description": "Necesidad frecuente de beber agua incluso sin actividad física intensa.",
        "weight": 2,
    },
    {
        "code": "orina_frecuente",
        "name": "Orinar frecuentemente",
        "description": "Aumento notable de la frecuencia urinaria durante el día o la noche.",
        "weight": 2,
    },
    {
        "code": "hambre_constante",
        "name": "Hambre constante",
        "description": "Sensación persistente de hambre aun después de comer.",
        "weight": 1,
    },
    {
        "code": "cansancio_extremo",
        "name": "Cansancio extremo",
        "description": "Fatiga continua o sensación de agotamiento sin una causa evidente.",
        "weight": 1,
    },
    {
        "code": "vision_borrosa",
        "name": "Visión borrosa",
        "description": "Dificultad para enfocar o percibir imágenes con claridad.",
        "weight": 2,
    },
    {
        "code": "perdida_peso",
        "name": "Pérdida de peso sin explicación",
        "description": "Disminución de peso reciente sin dieta ni ejercicio que la justifiquen.",
        "weight": 2,
    },
]

SYMPTOM_LOOKUP = {symptom["code"]: symptom for symptom in SYMPTOMS}
SYMPTOM_ORDER = {symptom["code"]: index for index, symptom in enumerate(SYMPTOMS)}
KEY_SYMPTOMS = {"sed_excesiva", "orina_frecuente"}


def _has_all(selected: set[str], *codes: str) -> bool:
    return all(code in selected for code in codes)


RULES = [
    {
        "id": "regla_alta_poliuria_polidipsia",
        "name": "Regla de alta sospecha por síntomas cardinales",
        "risk_level": "Alto",
        "confidence_score": 0.92,
        "condition": lambda selected: len(selected) >= 4
        and _has_all(selected, "sed_excesiva", "orina_frecuente")
        and (
            "vision_borrosa" in selected
            or "perdida_peso" in selected
            or "hambre_constante" in selected
        ),
        "probable_diagnosis": (
            "Prediagnóstico alto de diabetes mellitus. Los síntomas cardinales se "
            "acompañan de manifestaciones compatibles con hiperglucemia sostenida."
        ),
        "explanation": (
            "La combinación de sed excesiva y micción frecuente junto con al menos "
            "dos síntomas adicionales aumenta la sospecha clínica."
        ),
    },
    {
        "id": "regla_alta_metabolica",
        "name": "Regla de alta sospecha metabólica",
        "risk_level": "Alto",
        "confidence_score": 0.88,
        "condition": lambda selected: _has_all(
            selected,
            "sed_excesiva",
            "orina_frecuente",
            "perdida_peso",
        ),
        "probable_diagnosis": (
            "Prediagnóstico alto de diabetes mellitus por síntomas metabólicos "
            "compatibles con alteraciones en el manejo de glucosa."
        ),
        "explanation": (
            "La presencia conjunta de polidipsia, poliuria y pérdida de peso sin "
            "causa aparente es una regla crítica del sistema."
        ),
    },
    {
        "id": "regla_moderada_central",
        "name": "Regla de sospecha moderada central",
        "risk_level": "Moderado",
        "confidence_score": 0.73,
        "condition": lambda selected: len(selected) >= 3
        and _has_all(selected, "sed_excesiva", "orina_frecuente"),
        "probable_diagnosis": (
            "Prediagnóstico moderado de diabetes mellitus. Existen síntomas clave, "
            "pero aún se requiere confirmación médica."
        ),
        "explanation": (
            "Sed excesiva y orina frecuente constituyen el núcleo de la inferencia; "
            "la presencia de un tercer síntoma eleva la sospecha."
        ),
    },
    {
        "id": "regla_moderada_funcional",
        "name": "Regla de sospecha moderada funcional",
        "risk_level": "Moderado",
        "confidence_score": 0.65,
        "condition": lambda selected: _has_all(
            selected,
            "hambre_constante",
            "cansancio_extremo",
            "vision_borrosa",
        ),
        "probable_diagnosis": (
            "Prediagnóstico moderado de diabetes mellitus por combinación de "
            "síntomas funcionales y visuales."
        ),
        "explanation": (
            "Aunque no están presentes todos los síntomas cardinales, el patrón "
            "sugiere evaluar niveles de glucosa."
        ),
    },
    {
        "id": "regla_baja_inicial",
        "name": "Regla de sospecha baja inicial",
        "risk_level": "Bajo",
        "confidence_score": 0.42,
        "condition": lambda selected: len(selected) >= 2,
        "probable_diagnosis": (
            "Sospecha baja de diabetes mellitus. Hay síntomas aislados, pero el "
            "patrón todavía es insuficiente."
        ),
        "explanation": (
            "Dos síntomas pueden justificar seguimiento, pero no constituyen una "
            "base fuerte para el prediagnóstico."
        ),
    },
]


def _ordered_symptoms(selected: Iterable[str]) -> list[dict]:
    valid_codes = [code for code in selected if code in SYMPTOM_LOOKUP]
    return [
        SYMPTOM_LOOKUP[code]
        for code in sorted(valid_codes, key=lambda code: SYMPTOM_ORDER[code])
    ]


def _recommendations_for(risk_level: str) -> list[str]:
    base = [
        "Este resultado es orientativo y no sustituye una valoración médica profesional.",
        "Registrar la evolución de los síntomas y el momento en que aparecieron.",
    ]

    if risk_level == "Alto":
        return base + [
            "Acudir a consulta médica lo antes posible para realizar una prueba de glucosa.",
            "Evitar automedicarse y mantener hidratación adecuada.",
        ]

    if risk_level == "Moderado":
        return base + [
            "Solicitar una evaluación clínica y estudios de glucosa en ayuno o HbA1c.",
            "Monitorear si los síntomas aumentan en frecuencia o intensidad.",
        ]

    if risk_level == "Bajo":
        return base + [
            "Mantener observación de síntomas durante los próximos días.",
            "Buscar atención médica si aparecen sed excesiva y orina frecuente de forma conjunta.",
        ]

    return base + [
        "No hay suficiente evidencia para una inferencia. Si los síntomas aparecen, se debe repetir la evaluación.",
    ]


def evaluate_symptoms(selected_codes: Iterable[str]) -> dict:
    selected = {code for code in selected_codes if code in SYMPTOM_LOOKUP}
    ordered_symptoms = _ordered_symptoms(selected)
    total_weight = sum(symptom["weight"] for symptom in ordered_symptoms)
    matched_rule = next(
        (rule for rule in RULES if rule["condition"](selected)),
        {
            "id": "regla_sin_evidencia",
            "name": "Regla sin evidencia suficiente",
            "risk_level": "Sin evidencia",
            "confidence_score": 0.15,
            "probable_diagnosis": (
                "No hay suficientes síntomas para generar un prediagnóstico de diabetes mellitus."
            ),
            "explanation": (
                "El motor de inferencia necesita más síntomas compatibles para activar una regla clínica."
            ),
        },
    )

    missing_key_symptoms = [
        SYMPTOM_LOOKUP[code]["name"] for code in KEY_SYMPTOMS.difference(selected)
    ]

    return {
        "disease": DISEASE_INFO,
        "selected_symptoms": ordered_symptoms,
        "selected_count": len(ordered_symptoms),
        "symptom_weight": total_weight,
        "risk_level": matched_rule["risk_level"],
        "confidence_score": matched_rule["confidence_score"],
        "matched_rule": matched_rule["id"],
        "rule_name": matched_rule["name"],
        "probable_diagnosis": matched_rule["probable_diagnosis"],
        "explanation": matched_rule["explanation"],
        "missing_key_symptoms": missing_key_symptoms,
        "recommendations": _recommendations_for(matched_rule["risk_level"]),
    }

