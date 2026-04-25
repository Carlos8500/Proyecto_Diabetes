from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()


class Disease(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    symptoms = db.relationship("Symptom", back_populates="disease", cascade="all, delete-orphan")
    evaluations = db.relationship("Evaluation", back_populates="disease")


class Symptom(db.Model):
    __tablename__ = "symptoms"

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey("diseases.id"), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    disease = db.relationship("Disease", back_populates="symptoms")
    evaluation_links = db.relationship("EvaluationSymptom", back_populates="symptom")


class Evaluation(db.Model):
    __tablename__ = "evaluations"

    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey("diseases.id"), nullable=False)
    patient_name = db.Column(db.String(120), nullable=True)
    risk_level = db.Column(db.String(20), nullable=False)
    probable_diagnosis = db.Column(db.Text, nullable=False)
    confidence_score = db.Column(db.Numeric(5, 2), nullable=False)
    matched_rule = db.Column(db.String(80), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    selected_symptom_codes = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    disease = db.relationship("Disease", back_populates="evaluations")
    symptom_links = db.relationship(
        "EvaluationSymptom",
        back_populates="evaluation",
        cascade="all, delete-orphan",
    )


class EvaluationSymptom(db.Model):
    __tablename__ = "evaluation_symptoms"

    evaluation_id = db.Column(
        db.Integer,
        db.ForeignKey("evaluations.id", ondelete="CASCADE"),
        primary_key=True,
    )
    symptom_id = db.Column(
        db.Integer,
        db.ForeignKey("symptoms.id", ondelete="CASCADE"),
        primary_key=True,
    )

    evaluation = db.relationship("Evaluation", back_populates="symptom_links")
    symptom = db.relationship("Symptom", back_populates="evaluation_links")

