from app.expert_system import evaluate_symptoms


def test_high_risk_rule_is_triggered():
    result = evaluate_symptoms(
        [
            "sed_excesiva",
            "orina_frecuente",
            "vision_borrosa",
            "perdida_peso",
        ]
    )

    assert result["risk_level"] == "Alto"
    assert result["matched_rule"] == "regla_alta_poliuria_polidipsia"


def test_moderate_rule_is_triggered():
    result = evaluate_symptoms(
        [
            "sed_excesiva",
            "orina_frecuente",
            "cansancio_extremo",
        ]
    )

    assert result["risk_level"] == "Moderado"


def test_no_evidence_when_no_valid_symptoms():
    result = evaluate_symptoms(["desconocido"])

    assert result["risk_level"] == "Sin evidencia"
    assert result["selected_count"] == 0
