CREATE TABLE IF NOT EXISTS diseases (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS symptoms (
    id SERIAL PRIMARY KEY,
    disease_id INTEGER NOT NULL REFERENCES diseases(id) ON DELETE CASCADE,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    weight INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    disease_id INTEGER NOT NULL REFERENCES diseases(id),
    patient_name VARCHAR(120),
    risk_level VARCHAR(20) NOT NULL,
    probable_diagnosis TEXT NOT NULL,
    confidence_score NUMERIC(5, 2) NOT NULL,
    matched_rule VARCHAR(80) NOT NULL,
    notes TEXT,
    selected_symptom_codes TEXT NOT NULL,
    recommendations TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evaluation_symptoms (
    evaluation_id INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    symptom_id INTEGER NOT NULL REFERENCES symptoms(id) ON DELETE CASCADE,
    PRIMARY KEY (evaluation_id, symptom_id)
);

INSERT INTO diseases (code, name, description)
VALUES (
    'diabetes_mellitus',
    'Diabetes Mellitus',
    'Enfermedad metabólica crónica caracterizada por niveles elevados de glucosa en sangre por alteraciones en la producción o uso de la insulina.'
)
ON CONFLICT (code) DO UPDATE
SET
    name = EXCLUDED.name,
    description = EXCLUDED.description;

INSERT INTO symptoms (disease_id, code, name, description, weight)
SELECT
    d.id,
    v.code,
    v.name,
    v.description,
    v.weight
FROM diseases d
CROSS JOIN (
    VALUES
        ('sed_excesiva', 'Sed excesiva', 'Necesidad frecuente de beber agua incluso sin actividad física intensa.', 2),
        ('orina_frecuente', 'Orinar frecuentemente', 'Aumento notable de la frecuencia urinaria durante el día o la noche.', 2),
        ('hambre_constante', 'Hambre constante', 'Sensación persistente de hambre aun después de comer.', 1),
        ('cansancio_extremo', 'Cansancio extremo', 'Fatiga continua o sensación de agotamiento sin una causa evidente.', 1),
        ('vision_borrosa', 'Visión borrosa', 'Dificultad para enfocar o percibir imágenes con claridad.', 2),
        ('perdida_peso', 'Pérdida de peso sin explicación', 'Disminución de peso reciente sin dieta ni ejercicio que la justifiquen.', 2)
) AS v(code, name, description, weight)
WHERE d.code = 'diabetes_mellitus'
ON CONFLICT (code) DO UPDATE
SET
    disease_id = EXCLUDED.disease_id,
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    weight = EXCLUDED.weight;

