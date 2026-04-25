<<<<<<< HEAD
# Proyecto_Diabetes
Sistema experto, para deteccion de diabetes
=======
# Sistema Experto para Detección Temprana de Diabetes Mellitus

Aplicación web construida con Python, Flask y PostgreSQL para evaluar síntomas iniciales de diabetes mellitus mediante un motor de inferencia basado en reglas `if-then`.

## Qué hace el sistema

- Permite seleccionar síntomas iniciales desde una interfaz web.
- Evalúa la combinación de síntomas con reglas clínicas simples.
- Genera un prediagnóstico orientativo con nivel de riesgo, explicación y recomendaciones.
- Registra cada consulta en la base de datos para mantener historial.
- Expone una API REST para procesar síntomas en formato JSON.

## Síntomas considerados

- Sed excesiva
- Orinar frecuentemente
- Hambre constante
- Cansancio extremo
- Visión borrosa
- Pérdida de peso sin explicación

## Reglas de inferencia

El sistema utiliza una base de conocimiento definida con listas y diccionarios en `app/expert_system.py`.

Ejemplos de reglas:

- Si hay `sed_excesiva` + `orina_frecuente` + al menos dos síntomas adicionales, entonces el riesgo es `Alto`.
- Si hay `sed_excesiva` + `orina_frecuente` + un tercer síntoma, entonces el riesgo es `Moderado`.
- Si solo hay dos síntomas aislados, entonces el riesgo es `Bajo`.

## Tecnologías

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- HTML, CSS y JavaScript
- Docker Compose para levantar la base de datos rápidamente

## Estructura del proyecto

```text
PrologTris/
├── app/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── expert_system.py
│   ├── models.py
│   ├── routes.py
│   └── seed.py
├── database/
│   └── init.sql
├── tests/
│   └── test_expert_system.py
├── .env.example
├── docker-compose.yml
├── README.md
├── requirements.txt
└── run.py
```

## Configuración rápida

### 1. Crear entorno virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y ajustar los valores si hace falta:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=replace-with-a-secure-key
DATABASE_URL=postgresql+psycopg://expert_user:expert_pass@localhost:5432/diabetes_expert_db
```

### 3. Levantar PostgreSQL con Docker

```powershell
docker compose up -d postgres
```

El archivo `database/init.sql` crea las tablas y deja cargada la enfermedad con sus síntomas iniciales.

### 4. Ejecutar la aplicación

```powershell
.venv\Scripts\activate
python run.py
```

Abrir en el navegador:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Configuración manual de PostgreSQL

Si no se usa Docker:

1. Crear una base de datos llamada `diabetes_expert_db`.
2. Ejecutar el script `database/init.sql`.
3. Configurar `DATABASE_URL` con el usuario, contraseña y host correctos.

Ejemplo:

```env
DATABASE_URL=postgresql+psycopg://mi_usuario:mi_password@localhost:5432/diabetes_expert_db
```

## API disponible

### `POST /api/evaluate`

Ejemplo de request:

```json
{
  "patient_name": "Paciente A",
  "notes": "Presenta síntomas desde hace una semana.",
  "symptoms": [
    "sed_excesiva",
    "orina_frecuente",
    "vision_borrosa",
    "perdida_peso"
  ]
}
```

Ejemplo de respuesta:

```json
{
  "risk_level": "Alto",
  "probable_diagnosis": "Prediagnóstico alto de diabetes mellitus...",
  "matched_rule": "regla_alta_poliuria_polidipsia"
}
```

## Base de datos y compartición

Sí, la base de datos se puede compartir de forma correcta, pero lo recomendable no es compartir archivos internos del motor de PostgreSQL. Lo correcto es compartir:

- `database/init.sql` para recrear la estructura y los datos base.
- `docker-compose.yml` para que otra persona levante PostgreSQL con la misma configuración.
- `.env.example` para que sepan cómo conectar la aplicación.

Si quieres entregar también datos de ejemplo ya capturados, puedes exportarlos con:

```powershell
pg_dump -U expert_user -d diabetes_expert_db > respaldo.sql
```

Luego otra persona puede importarlos con:

```powershell
psql -U expert_user -d diabetes_expert_db -f respaldo.sql
```

## Evidencia sugerida para el PDF

Incluye capturas de:

- Pantalla principal de la interfaz.
- Selección de síntomas.
- Resultado con nivel de riesgo y recomendaciones.
- Base de datos mostrando registros en `evaluations`.
- Repositorio con el código fuente.

## Limitaciones del sistema

- El resultado es un prediagnóstico orientativo.
- Solo evalúa una enfermedad: diabetes mellitus.
- La inferencia depende de reglas manuales, no de estudios clínicos en tiempo real.
- No reemplaza la valoración médica profesional.

>>>>>>> a708b07 (Primer commit: Docker y Postgres listos)
