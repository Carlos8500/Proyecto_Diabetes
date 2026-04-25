const form = document.getElementById("evaluation-form");
const resultsPanel = document.getElementById("results-panel");
const resultsContent = document.getElementById("results-content");

function riskClass(riskLevel) {
  return `risk-${riskLevel.toLowerCase().replace(/\s+/g, "-")}`;
}

function renderList(items, emptyMessage) {
  if (!items || items.length === 0) {
    return `<p class="empty-state">${emptyMessage}</p>`;
  }

  return `<ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>`;
}

function renderResult(data) {
  const symptomNames = data.selected_symptoms.map((item) => item.name);
  const confidence = `${Math.round(Number(data.confidence_score) * 100)}%`;

  resultsContent.innerHTML = `
    <div class="result-grid">
      <article class="metric-card ${riskClass(data.risk_level)}">
        <span class="metric-label">Nivel de riesgo</span>
        <span class="metric-value">${data.risk_level}</span>
      </article>
      <article class="metric-card">
        <span class="metric-label">Confianza</span>
        <span class="metric-value">${confidence}</span>
      </article>
      <article class="metric-card">
        <span class="metric-label">Síntomas detectados</span>
        <span class="metric-value">${data.selected_count}</span>
      </article>
      <article class="metric-card">
        <span class="metric-label">Peso acumulado</span>
        <span class="metric-value">${data.symptom_weight}</span>
      </article>
    </div>

    <div class="details-grid">
      <article class="detail-card">
        <h3>Posible diagnóstico</h3>
        <p>${data.probable_diagnosis}</p>
      </article>
      <article class="detail-card">
        <h3>Regla activada</h3>
        <p><strong>${data.rule_name}</strong></p>
        <p>${data.explanation}</p>
      </article>
      <article class="detail-card">
        <h3>Síntomas seleccionados</h3>
        ${renderList(symptomNames, "No se registraron síntomas válidos.")}
      </article>
      <article class="detail-card">
        <h3>Síntomas clave faltantes</h3>
        ${renderList(data.missing_key_symptoms, "No faltan síntomas clave en la evaluación actual.")}
      </article>
      <article class="detail-card">
        <h3>Recomendaciones</h3>
        ${renderList(data.recommendations, "No hay recomendaciones adicionales.")}
      </article>
      <article class="detail-card">
        <h3>Registro</h3>
        <p class="result-note">ID de evaluación: ${data.evaluation_id ?? "No registrado"}</p>
        <p class="result-note">Motor: ${data.disease.name}</p>
      </article>
    </div>
  `;

  if (data.storage_warning) {
    resultsContent.insertAdjacentHTML(
      "beforeend",
      `<div class="alert-message">${data.storage_warning}</div>`,
    );
  }

  resultsPanel.hidden = false;
  resultsPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function handleSubmit(event) {
  event.preventDefault();

  const formData = new FormData(form);
  const symptoms = formData.getAll("symptoms");

  if (symptoms.length === 0) {
    resultsPanel.hidden = false;
    resultsContent.innerHTML = `<p class="alert-message">Selecciona al menos un síntoma para ejecutar la evaluación.</p>`;
    return;
  }

  const payload = {
    patient_name: formData.get("patient_name"),
    notes: formData.get("notes"),
    symptoms,
  };

  const response = await fetch(form.dataset.endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    resultsPanel.hidden = false;
    resultsContent.innerHTML = `<p class="alert-message">${data.error ?? "No se pudo procesar la evaluación."}</p>`;
    return;
  }

  renderResult(data);
}

if (form) {
  form.addEventListener("submit", handleSubmit);
  form.addEventListener("reset", () => {
    resultsPanel.hidden = true;
    resultsContent.innerHTML = "";
  });
}

