/**
 * AeroResilience Frontend Client Logic
 * Accessible, responsive, and XSS-safe DOM manipulation.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Application State
  const state = {
    location: "Delhi-NCR",
    severity: "Severe",
    aqi: 420,
    pm2_5: 285.0,
    source: "Preset Scenario",
    commute_mode: "public_bus_metro",
    housing_type: "apartment",
    cooking_heating: "lpg_gas",
    budget_tier: "low_cost",
    vulnerable_members: ["children", "asthma"],
    recommendations: null,
    loading: false
  };

  // DOM Elements
  const locationInput = document.getElementById("location-input");
  const fetchLiveAqiBtn = document.getElementById("fetch-live-aqi-btn");
  const presetButtons = document.querySelectorAll(".preset-btn");
  const aqiDisplayBox = document.getElementById("aqi-display-box");
  const aqiTierIcon = document.getElementById("aqi-tier-icon");
  const aqiTierText = document.getElementById("aqi-tier-text");
  const aqiMetricVal = document.getElementById("aqi-metric-val");
  const pm25MetricVal = document.getElementById("pm25-metric-val");
  const aqiSourceVal = document.getElementById("aqi-source-val");
  const aqiDescText = document.getElementById("aqi-desc-text");
  const assistantForm = document.getElementById("assistant-form");
  const generateBtn = document.getElementById("generate-btn");
  const btnSpinner = document.getElementById("btn-spinner");
  const btnText = document.getElementById("btn-text");
  const engineStatusText = document.getElementById("engine-status-text");
  const printChecklistBtn = document.getElementById("print-checklist-btn");

  // Tab Elements
  const tabs = document.querySelectorAll(".tab-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");

  // Output Containers
  const riskSummaryCard = document.getElementById("risk-summary-card");
  const riskBadgeText = document.getElementById("risk-badge-text");
  const generatorTagText = document.getElementById("generator-tag-text");
  const riskWarningText = document.getElementById("risk-warning-text");
  const priorityActionsList = document.getElementById("priority-actions-list");
  const routinesList = document.getElementById("routines-list");
  const iaqList = document.getElementById("iaq-list");
  const swapsList = document.getElementById("swaps-list");

  // Preset Definitions
  const PRESET_MAP = {
    Moderate: {
      aqi: 85,
      pm25: 28.5,
      icon: "🌤️",
      label: "Moderate (Acceptable)",
      desc: "Acceptable winter air quality. Morning exercise permissible; sensitive groups should observe mild symptoms."
    },
    Poor: {
      aqi: 165,
      pm25: 82.0,
      icon: "⚠️",
      label: "Poor (Unhealthy for Sensitive Groups)",
      desc: "Surface temperature inversion trapping vehicular and industrial smoke. Discomfort likely with prolonged exposure."
    },
    "Very Poor": {
      aqi: 265,
      pm25: 145.0,
      icon: "🚨",
      label: "Very Poor (Unhealthy for Everyone)",
      desc: "Hazardous stagnant smog. High risk of airway inflammation. Move all workouts and children's recreation indoors."
    },
    Severe: {
      aqi: 420,
      pm25: 285.0,
      icon: "🛑",
      label: "Severe (Hazardous Emergency)",
      desc: "Emergency winter smog episode. Thermal boundary layer trapping particulate soot. Strict indoor lockdown recommended."
    }
  };

  // 1. Check Server Health
  async function checkHealth() {
    try {
      const resp = await fetch("/api/health");
      if (resp.ok) {
        const data = await resp.json();
        if (data.has_gemini) {
          engineStatusText.textContent = "Gemini AI Hybrid Active";
        } else if (data.has_openai) {
          engineStatusText.textContent = "OpenAI Hybrid Active";
        } else {
          engineStatusText.textContent = "Deterministic Rule Matrix Active";
        }
      }
    } catch {
      engineStatusText.textContent = "Offline Simulation Mode";
    }
  }

  // 2. Update AQI Visual Box (Ensuring Multi-Modal Indicators)
  function updateAqiBox(severity, aqi, pm25, source) {
    const info = PRESET_MAP[severity] || PRESET_MAP["Severe"];
    state.severity = severity;
    state.aqi = aqi;
    state.pm2_5 = pm25;
    state.source = source;

    // Reset severity classes
    aqiDisplayBox.className = `aqi-card ${severity.toLowerCase().replace(" ", "-")}`;
    aqiTierIcon.textContent = info.icon;
    aqiTierText.textContent = `${severity} (${aqi >= 300 ? "Hazardous" : aqi >= 200 ? "Unhealthy" : aqi >= 100 ? "Poor" : "Moderate"})`;
    aqiMetricVal.textContent = aqi;
    pm25MetricVal.textContent = `${pm25} µg/m³`;
    aqiSourceVal.textContent = source;
    aqiDescText.textContent = info.desc;
  }

  // 3. Preset Button Click Handler
  presetButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      presetButtons.forEach(b => {
        b.classList.remove("active");
        b.setAttribute("aria-pressed", "false");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");

      const sev = btn.getAttribute("data-severity");
      const info = PRESET_MAP[sev];
      updateAqiBox(sev, info.aqi, info.pm25, "Preset Scenario");
    });
  });

  // 4. Fetch Live AQI from Open-Meteo
  fetchLiveAqiBtn.addEventListener("click", async () => {
    const city = locationInput.value.trim() || "Delhi";
    fetchLiveAqiBtn.disabled = true;
    fetchLiveAqiBtn.textContent = "Fetching...";

    try {
      const res = await fetch(`/api/aqi?city=${encodeURIComponent(city)}`);
      if (res.ok) {
        const data = await res.json();
        updateAqiBox(data.severity_tier, data.aqi, data.pm2_5, "Live Open-Meteo");

        // Sync preset buttons
        presetButtons.forEach(b => {
          const match = b.getAttribute("data-severity").toLowerCase() === data.severity_tier.toLowerCase();
          b.classList.toggle("active", match);
          b.setAttribute("aria-pressed", match ? "true" : "false");
        });
      } else {
        alert("Unable to fetch live data for this location. Using cached preset.");
      }
    } catch {
      alert("Network error fetching live AQI. Falling back to preset scenario.");
    } finally {
      fetchLiveAqiBtn.disabled = false;
      fetchLiveAqiBtn.textContent = "Fetch Live AQI";
    }
  });

  // 5. Tab Navigation
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.getAttribute("aria-controls");

      tabs.forEach(t => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      tabPanels.forEach(p => {
        p.classList.add("hidden");
        p.classList.remove("active");
      });

      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");

      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.remove("hidden");
        targetPanel.classList.add("active");
      }
    });
  });

  // 6. Form Submission & Recommendations Fetch
  assistantForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (state.loading) return;

    // Gather inputs
    const checkedVulns = Array.from(document.querySelectorAll('input[name="vulnerable"]:checked')).map(el => el.value);
    const payload = {
      location: locationInput.value.trim() || "Delhi-NCR",
      aqi_input_type: state.source === "Live Open-Meteo" ? "live" : "preset",
      preset_severity: state.severity,
      custom_aqi: state.aqi,
      commute_mode: document.getElementById("commute-select").value,
      housing_type: document.getElementById("housing-select").value,
      cooking_heating: document.getElementById("cooking-select").value,
      budget_tier: document.getElementById("budget-select").value,
      vulnerable_members: checkedVulns,
      user_question: document.getElementById("question-input").value.trim()
    };

    setLoading(true);

    try {
      const response = await fetch("/api/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        const data = await response.json();
        renderResults(data);
      } else {
        alert("Failed to generate recommendations. Please try again.");
      }
    } catch (err) {
      alert("Error contacting assistant server. Check console for details.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  });

  function setLoading(isLoading) {
    state.loading = isLoading;
    generateBtn.disabled = isLoading;
    if (isLoading) {
      btnSpinner.classList.remove("hidden");
      btnText.textContent = "Synthesizing Science-Backed Plan...";
    } else {
      btnSpinner.classList.add("hidden");
      btnText.textContent = "Generate Tailored Resilience Plan";
    }
  }

  // 7. Render Recommendations (XSS-Safe DOM manipulation)
  function renderResults(data) {
    state.recommendations = data;

    // A. Render Risk Summary
    const risk = data.risk_summary;
    riskBadgeText.textContent = `🚨 ${risk.severity_tier} Smog Priority (AQI ${risk.aqi})`;
    generatorTagText.textContent = `Engine: ${data.generated_by}`;
    riskWarningText.textContent = risk.health_warning;

    priorityActionsList.innerHTML = "";
    risk.priority_actions.forEach(action => {
      const li = document.createElement("li");
      li.textContent = action;
      priorityActionsList.appendChild(li);
    });

    // B. Render Daily Routines
    routinesList.innerHTML = "";
    data.daily_routines.forEach(item => {
      const card = document.createElement("article");
      card.className = "rec-card";

      const header = document.createElement("div");
      header.className = "rec-card-header";

      const title = document.createElement("h4");
      title.className = "rec-card-title";
      title.textContent = item.title;

      const chip = document.createElement("span");
      chip.className = "rec-chip low-cost";
      chip.textContent = item.time_window;

      header.appendChild(title);
      header.appendChild(chip);

      const body = document.createElement("p");
      body.className = "rec-card-body";
      body.textContent = item.description;

      const impactBox = document.createElement("div");
      impactBox.className = "impact-badge-box";

      const impactTitle = document.createElement("div");
      impactTitle.className = "impact-badge-title";
      impactTitle.innerHTML = `<span aria-hidden="true">🔬</span> Direct Physical Impact`;

      const impactDesc = document.createElement("p");
      impactDesc.className = "impact-badge-desc";
      impactDesc.textContent = item.direct_impact;

      impactBox.appendChild(impactTitle);
      impactBox.appendChild(impactDesc);

      card.appendChild(header);
      card.appendChild(body);
      card.appendChild(impactBox);
      routinesList.appendChild(card);
    });

    // C. Render IAQ Hacks
    iaqList.innerHTML = "";
    data.iaq_hacks.forEach(hack => {
      const card = document.createElement("article");
      card.className = "rec-card";

      const header = document.createElement("div");
      header.className = "rec-card-header";

      const title = document.createElement("h4");
      title.className = "rec-card-title";
      title.textContent = hack.title;

      const chip = document.createElement("span");
      const costClass = hack.cost_tier.toLowerCase().includes("free") ? "free" :
                        hack.cost_tier.toLowerCase().includes("low") ? "low-cost" : "equipment";
      chip.className = `rec-chip ${costClass}`;
      chip.textContent = hack.cost_tier;

      header.appendChild(title);
      header.appendChild(chip);

      const body = document.createElement("div");
      body.className = "rec-card-body";
      body.innerHTML = `<strong>Materials:</strong> ${escapeHtml(hack.materials_needed)}<br><br><strong>Implementation Steps:</strong><br>${escapeHtml(hack.implementation_steps)}`;

      const impactBox = document.createElement("div");
      impactBox.className = "impact-badge-box";

      const impactTitle = document.createElement("div");
      impactTitle.className = "impact-badge-title";
      impactTitle.innerHTML = `<span aria-hidden="true">💨</span> Particulate Removal Mechanism`;

      const impactDesc = document.createElement("p");
      impactDesc.className = "impact-badge-desc";
      impactDesc.textContent = hack.direct_impact;

      impactBox.appendChild(impactTitle);
      impactBox.appendChild(impactDesc);

      card.appendChild(header);
      card.appendChild(body);
      card.appendChild(impactBox);
      iaqList.appendChild(card);
    });

    // D. Render Sustainable Alternatives
    swapsList.innerHTML = "";
    data.sustainable_alternatives.forEach(alt => {
      const card = document.createElement("article");
      card.className = "rec-card";

      const header = document.createElement("div");
      header.className = "rec-card-header";

      const title = document.createElement("h4");
      title.className = "rec-card-title";
      title.textContent = alt.title;

      const chip = document.createElement("span");
      chip.className = "rec-chip free";
      chip.textContent = alt.scope;

      header.appendChild(title);
      header.appendChild(chip);

      const body = document.createElement("div");
      body.className = "rec-card-body";
      body.innerHTML = `<strong>Replaces High-Polluting Habit:</strong><br>${escapeHtml(alt.replaces_activity)}`;

      const impactBox = document.createElement("div");
      impactBox.className = "impact-badge-box";

      const impactTitle = document.createElement("div");
      impactTitle.className = "impact-badge-title";
      impactTitle.innerHTML = `<span aria-hidden="true">🌱</span> Community Airshed Benefit`;

      const impactDesc = document.createElement("p");
      impactDesc.className = "impact-badge-desc";
      impactDesc.textContent = alt.direct_impact;

      impactBox.appendChild(impactTitle);
      impactBox.appendChild(impactDesc);

      card.appendChild(header);
      card.appendChild(body);
      card.appendChild(impactBox);
      swapsList.appendChild(card);
    });

    // Announce update to screen readers
    const resultsContainer = document.getElementById("results-container");
    resultsContainer.setAttribute("aria-label", "Recommendations updated successfully");
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // 8. Print Checklist Button
  printChecklistBtn.addEventListener("click", () => {
    window.print();
  });

  // Initial Run
  checkHealth();
  // Trigger initial render with default preset
  assistantForm.dispatchEvent(new Event("submit"));
});
