/**
 * AeroResilience Spatial Antigravity Client Logic
 * 3D Interactive Gauges, Weightless Cursor Physics, and GenAI Resilience Planner.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Application State
  const state = {
    location: "Delhi-NCR",
    severity: "Severe",
    aqi: 420,
    pm2_5: 285.0,
    pm10: 460.0,
    no2: 118.0,
    so2: 45.0,
    co: 4.8,
    o3: 14.0,
    temperature: 14.2,
    humidity: 86,
    wind_speed: 2.4,
    who_multiplier: 19.0,
    cigarette_equiv: 13.0,
    source: "Preset Scenario",
    commute_mode: "public_bus_metro",
    housing_type: "apartment",
    cooking_heating: "lpg_gas",
    budget_tier: "low_cost",
    vulnerable_members: ["children", "asthma"],
    recommendations: null,
    loading: false
  };

  // DOM Elements - Hero & Telemetry
  const locationInput = document.getElementById("location-input");
  const fetchLiveAqiBtn = document.getElementById("fetch-live-aqi-btn");
  const heroAqiNumber = document.getElementById("hero-aqi-number");
  const heroStatusBadge = document.getElementById("hero-status-badge");
  const heroStatusTitle = document.getElementById("hero-status-title");
  const statusIcon = document.getElementById("status-icon");
  const heroStatusDesc = document.getElementById("hero-status-desc");
  const whoMultiplierText = document.getElementById("who-multiplier-text");
  const cigaretteEquivText = document.getElementById("cigarette-equiv-text");
  const spectrumPin = document.getElementById("spectrum-pin");
  const pinBadgeVal = document.getElementById("pin-badge-val");
  const stationLabel = document.getElementById("station-label");
  const liveTelemetryText = document.getElementById("live-telemetry-text");
  const gaugeFillPath = document.getElementById("gauge-fill-path");
  const orb1 = document.getElementById("orb-1");

  // Weather Elements
  const weatherTemp = document.getElementById("weather-temp");
  const weatherCondition = document.getElementById("weather-condition");
  const weatherWind = document.getElementById("weather-wind");
  const weatherHumidity = document.getElementById("weather-humidity");

  // 6 Pollutants Elements
  const pm25Val = document.getElementById("pm25-val");
  const pm25Badge = document.getElementById("pm25-badge");
  const pm25Excess = document.getElementById("pm25-excess");
  const pm10Val = document.getElementById("pm10-val");
  const pm10Badge = document.getElementById("pm10-badge");
  const pm10Excess = document.getElementById("pm10-excess");
  const no2Val = document.getElementById("no2-val");
  const no2Badge = document.getElementById("no2-badge");
  const no2Excess = document.getElementById("no2-excess");
  const so2Val = document.getElementById("so2-val");
  const so2Badge = document.getElementById("so2-badge");
  const so2Excess = document.getElementById("so2-excess");
  const coVal = document.getElementById("co-val");
  const coBadge = document.getElementById("co-badge");
  const coExcess = document.getElementById("co-excess");
  const o3Val = document.getElementById("o3-val");
  const o3Badge = document.getElementById("o3-badge");

  // Hotspots Container
  const hotspotsContainer = document.getElementById("hotspots-container");

  // Presets & Planner
  const presetPills = document.querySelectorAll(".preset-pill");
  const assistantForm = document.getElementById("assistant-form");
  const generateBtn = document.getElementById("generate-btn");
  const btnSpinner = document.getElementById("btn-spinner");
  const btnText = document.getElementById("btn-text");
  const engineStatusText = document.getElementById("engine-status-text");
  const printChecklistBtn = document.getElementById("print-checklist-btn");

  // Blueprint Tabs
  const blueprintTabs = document.querySelectorAll(".blueprint-tab");
  const tabPanels = document.querySelectorAll(".tab-panel");

  // Results Containers
  const riskSummaryCard = document.getElementById("risk-summary-card");
  const riskBadgeText = document.getElementById("risk-badge-text");
  const generatorTagText = document.getElementById("generator-tag-text");
  const riskWarningText = document.getElementById("risk-warning-text");
  const priorityActionsList = document.getElementById("priority-actions-list");
  const routinesList = document.getElementById("routines-list");
  const iaqList = document.getElementById("iaq-list");
  const swapsList = document.getElementById("swaps-list");

  // Regional Hotspots Benchmark
  const DEFAULT_HOTSPOTS = [
    { station: "Anand Vihar, Delhi", aqi: 488, pm25: 340.2, status: "Hazardous", mult: "22x WHO" },
    { station: "Jahangirpuri, Delhi", aqi: 465, pm25: 315.0, status: "Hazardous", mult: "21x WHO" },
    { station: "Wazirpur, Delhi", aqi: 452, pm25: 298.5, status: "Hazardous", mult: "20x WHO" },
    { station: "RK Puram, Delhi", aqi: 418, pm25: 272.0, status: "Severe", mult: "18x WHO" },
    { station: "IGI Airport (T3), Delhi", aqi: 376, pm25: 242.0, status: "Severe", mult: "16x WHO" },
    { station: "Lodhi Road (Clean Corridor)", aqi: 295, pm25: 168.0, status: "Very Poor", mult: "11x WHO" }
  ];

  // 1. Calculate Spectrum Track Pin Position (0% to 100%)
  function calculatePinLeft(aqi) {
    if (aqi <= 50) return Math.max(3, (aqi / 50) * 16.6);
    if (aqi <= 100) return 16.6 + ((aqi - 50) / 50) * 16.6;
    if (aqi <= 150) return 33.2 + ((aqi - 100) / 50) * 16.6;
    if (aqi <= 200) return 49.8 + ((aqi - 150) / 50) * 16.6;
    if (aqi <= 300) return 66.4 + ((aqi - 200) / 100) * 16.6;
    return Math.min(96, 83.0 + (Math.min(200, aqi - 300) / 200) * 15.0);
  }

  // 2. Animate SVG Gauge Arc
  function updateGaugeArc(aqi) {
    if (!gaugeFillPath) return;
    const maxAqi = 500;
    const totalArc = 267; // Circumference of semicircle radius 85
    const ratio = Math.min(maxAqi, Math.max(0, aqi)) / maxAqi;
    const offset = totalArc * (1 - ratio);
    gaugeFillPath.style.strokeDashoffset = `${offset}`;
  }

  // 3. Render Regional Hotspots
  function renderHotspots(hotspots) {
    const list = hotspots && hotspots.length > 0 ? hotspots : DEFAULT_HOTSPOTS;
    hotspotsContainer.innerHTML = "";

    list.forEach(item => {
      const card = document.createElement("div");
      card.className = "hotspot-card tilt-card";
      card.setAttribute("role", "button");
      card.setAttribute("tabindex", "0");
      card.setAttribute("aria-label", `Select station ${item.station || item.name}, AQI ${item.aqi}`);

      const left = document.createElement("div");
      const name = document.createElement("h4");
      name.className = "hotspot-station-name";
      name.textContent = item.station || item.name;

      const meta = document.createElement("p");
      meta.className = "hotspot-meta";
      meta.textContent = `PM2.5: ${item.pm2_5 || item.pm25} µg/m³ · ${item.multiplier || item.mult || ""}`;

      left.appendChild(name);
      left.appendChild(meta);

      const pill = document.createElement("div");
      const isSevere = item.aqi >= 400;
      pill.className = `hotspot-score-pill ${isSevere ? "" : "very-poor"}`;
      pill.innerHTML = `<span aria-hidden="true">🛑</span><span>${item.aqi}</span>`;

      card.appendChild(left);
      card.appendChild(pill);

      const triggerSelect = () => {
        locationInput.value = item.station || item.name;
        updateDashboardFromData({
          location: item.station || item.name,
          aqi: item.aqi,
          pm2_5: item.pm2_5 || item.pm25,
          pm10: Math.round((item.pm2_5 || item.pm25) * 1.6),
          no2: Math.round((item.pm2_5 || item.pm25) * 0.4),
          so2: Math.round((item.pm2_5 || item.pm25) * 0.15),
          co: Math.round((item.pm2_5 || item.pm25) * 0.015 * 10) / 10,
          o3: 15.0,
          temperature: 15.0,
          humidity: 82,
          wind_speed: 2.8,
          who_multiplier: Math.round(((item.pm2_5 || item.pm25) / 15.0) * 10) / 10,
          cigarette_equiv: Math.round(((item.pm2_5 || item.pm25) / 22.0) * 10) / 10,
          severity_tier: item.aqi >= 400 ? "Severe" : item.aqi >= 300 ? "Severe" : item.aqi >= 200 ? "Very Poor" : "Poor",
          source: "Regional Station"
        });
        assistantForm.dispatchEvent(new Event("submit"));
      };

      card.addEventListener("click", triggerSelect);
      card.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          triggerSelect();
        }
      });

      hotspotsContainer.appendChild(card);
    });

    init3DTilt();
  }

  // 4. Update Dashboard Telemetry & Visual State
  function updateDashboardFromData(data) {
    state.location = data.location || state.location;
    state.aqi = data.aqi || state.aqi;
    state.pm2_5 = data.pm2_5 || state.pm2_5;
    state.pm10 = data.pm10 || state.pm10;
    state.no2 = data.no2 || state.no2;
    state.so2 = data.so2 || state.so2;
    state.co = data.co || state.co;
    state.o3 = data.o3 || state.o3;
    state.temperature = data.temperature || state.temperature;
    state.humidity = data.humidity || state.humidity;
    state.wind_speed = data.wind_speed || state.wind_speed;
    state.who_multiplier = data.who_multiplier || Math.round((state.pm2_5 / 15.0) * 10) / 10;
    state.cigarette_equiv = data.cigarette_equiv || Math.round((state.pm2_5 / 22.0) * 10) / 10;
    state.severity = data.severity_tier || state.severity;
    state.source = data.source || state.source;

    // Body Theme class
    document.body.className = `theme-${state.severity.toLowerCase().replace(" ", "-")}`;

    // Update Ambient Glow Orb color
    if (orb1) {
      if (state.aqi >= 400) {
        orb1.style.background = "radial-gradient(circle, rgba(225, 29, 72, 0.45) 0%, transparent 70%)";
      } else if (state.aqi >= 300) {
        orb1.style.background = "radial-gradient(circle, rgba(168, 85, 247, 0.45) 0%, transparent 70%)";
      } else if (state.aqi >= 200) {
        orb1.style.background = "radial-gradient(circle, rgba(249, 115, 22, 0.4) 0%, transparent 70%)";
      } else {
        orb1.style.background = "radial-gradient(circle, rgba(16, 185, 129, 0.35) 0%, transparent 70%)";
      }
    }

    // Hero AQI & Speedometer Arc
    heroAqiNumber.textContent = state.aqi;
    pinBadgeVal.textContent = state.aqi;
    spectrumPin.style.left = `${calculatePinLeft(state.aqi)}%`;
    updateGaugeArc(state.aqi);

    // Meta Labels
    stationLabel.textContent = `Active Telemetry: ${state.location}`;
    liveTelemetryText.textContent = `TELEMETRY: ${state.source.toUpperCase()} · CPCB & US-EPA`;

    const sev = state.severity.toLowerCase();
    heroStatusBadge.className = `status-badge ${sev === "severe" ? (state.aqi >= 400 ? "hazardous" : "severe") : sev} float-badge`;
    
    if (state.aqi >= 400) {
      statusIcon.textContent = "🛑";
      heroStatusTitle.textContent = "Severe (Hazardous Emergency)";
      heroStatusDesc.textContent = "Critical winter inversion episode. Extreme respiratory toxicity for all individuals.";
    } else if (state.aqi >= 300) {
      statusIcon.textContent = "🚨";
      heroStatusTitle.textContent = "Severe (Hazardous)";
      heroStatusDesc.textContent = "Surface particulate lid trapped near ground level. Severe health impact across population.";
    } else if (state.aqi >= 200) {
      statusIcon.textContent = "⚠️";
      heroStatusTitle.textContent = "Very Poor (Unhealthy)";
      heroStatusDesc.textContent = "High smog concentration. Prolonged outdoor exertion triggers bronchial distress.";
    } else if (state.aqi >= 100) {
      statusIcon.textContent = "⚠️";
      heroStatusTitle.textContent = "Poor (Sensitive Warning)";
      heroStatusDesc.textContent = "Unhealthy for sensitive individuals, infants, seniors, and asthmatic patients.";
    } else {
      statusIcon.textContent = "🌤️";
      heroStatusTitle.textContent = "Moderate (Acceptable)";
      heroStatusDesc.textContent = "Acceptable air quality with mild winter haze during morning hours.";
    }

    // Impact Multipliers
    whoMultiplierText.innerHTML = `<strong>${state.who_multiplier}x</strong> Above WHO 24h Safe Limit`;
    cigaretteEquivText.innerHTML = `<strong>~${state.cigarette_equiv}</strong> Cigarettes/Day Inhalation`;

    // Weather Metrics
    weatherTemp.textContent = `${state.temperature}°C`;
    weatherHumidity.textContent = `${state.humidity}%`;
    weatherWind.textContent = `${state.wind_speed} km/h ${state.wind_speed < 4 ? "Calm" : "Breeze"}`;
    weatherCondition.textContent = state.aqi >= 300 ? "Dense Winter Smog" : state.aqi >= 200 ? "Smog Inversion" : "Winter Haze";

    // 6 Pollutants Card Updates
    pm25Val.textContent = state.pm2_5.toFixed(1);
    pm25Excess.textContent = `${(state.pm2_5 / 15.0).toFixed(1)}x limit`;
    pm25Badge.textContent = state.pm2_5 > 250 ? "Hazardous" : state.pm2_5 > 120 ? "Severe" : state.pm2_5 > 60 ? "Poor" : "Moderate";

    pm10Val.textContent = state.pm10.toFixed(1);
    pm10Excess.textContent = `${(state.pm10 / 45.0).toFixed(1)}x limit`;
    pm10Badge.textContent = state.pm10 > 350 ? "Severe" : state.pm10 > 200 ? "Very Poor" : "Moderate";

    no2Val.textContent = state.no2.toFixed(1);
    no2Excess.textContent = `${(state.no2 / 25.0).toFixed(1)}x limit`;
    no2Badge.textContent = state.no2 > 80 ? "Elevated" : "Moderate";

    so2Val.textContent = state.so2.toFixed(1);
    so2Excess.textContent = `${(state.so2 / 40.0).toFixed(1)}x limit`;
    so2Badge.textContent = state.so2 > 40 ? "Elevated" : "Moderate";

    coVal.textContent = state.co.toFixed(1);
    coExcess.textContent = `${(state.co / 4.0).toFixed(1)}x limit`;
    coBadge.textContent = state.co > 4.0 ? "High" : "Moderate";

    o3Val.textContent = state.o3.toFixed(1);
    o3Badge.textContent = state.o3 > 100 ? "Elevated" : "Low / Good";

    // Sync Preset buttons
    presetPills.forEach(pill => {
      const match = pill.getAttribute("data-severity").toLowerCase() === state.severity.toLowerCase();
      pill.classList.toggle("active", match);
      pill.setAttribute("aria-pressed", match ? "true" : "false");
    });
  }

  // 5. Interactive 3D Tilt Effect on Cursor Movement (Antigravity Vibe)
  function init3DTilt() {
    // Respect reduced motion
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      return;
    }

    const cards = document.querySelectorAll(".tilt-card");
    cards.forEach(card => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -6; // Max 6 deg
        const rotateY = ((x - centerX) / centerX) * 6;  // Max 6 deg

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-2px)`;
      });

      card.addEventListener("mouseleave", () => {
        card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)";
      });
    });
  }

  // 6. Check Server Health
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
          engineStatusText.textContent = "AI Hybrid Engine Ready";
        }
      }
    } catch {
      engineStatusText.textContent = "Offline Simulation Mode";
    }
  }

  // 7. Preset Pill Selection
  presetPills.forEach(pill => {
    pill.addEventListener("click", async () => {
      presetPills.forEach(p => {
        p.classList.remove("active");
        p.setAttribute("aria-pressed", "false");
      });
      pill.classList.add("active");
      pill.setAttribute("aria-pressed", "true");

      const sev = pill.getAttribute("data-severity");
      try {
        const res = await fetch("/api/presets");
        if (res.ok) {
          const presets = await res.json();
          const target = presets[sev];
          if (target) {
            updateDashboardFromData({
              location: locationInput.value.trim() || "Delhi-NCR",
              ...target,
              source: "Preset Scenario"
            });
            assistantForm.dispatchEvent(new Event("submit"));
          }
        }
      } catch {
        state.severity = sev;
        assistantForm.dispatchEvent(new Event("submit"));
      }
    });
  });

  // 8. Live Sync from Open-Meteo
  fetchLiveAqiBtn.addEventListener("click", async () => {
    const city = locationInput.value.trim() || "Delhi";
    fetchLiveAqiBtn.disabled = true;
    fetchLiveAqiBtn.textContent = "Syncing...";

    try {
      const res = await fetch(`/api/aqi?city=${encodeURIComponent(city)}`);
      if (res.ok) {
        const data = await res.json();
        updateDashboardFromData(data);
        renderHotspots(data.hotspots);
        assistantForm.dispatchEvent(new Event("submit"));
      } else {
        alert("Unable to reach air telemetry for this city. Falling back to regional preset.");
      }
    } catch {
      alert("Network timeout syncing live AQI. Using cached regional telemetry.");
    } finally {
      fetchLiveAqiBtn.disabled = false;
      fetchLiveAqiBtn.textContent = "Live Sync";
    }
  });

  // 9. Blueprint Tab Navigation
  blueprintTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.getAttribute("aria-controls");

      blueprintTabs.forEach(t => {
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

  // 10. Form Submission & Recommendations
  assistantForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (state.loading) return;

    const checkedVulns = Array.from(document.querySelectorAll('input[name="vulnerable"]:checked')).map(el => el.value);
    const payload = {
      location: locationInput.value.trim() || "Delhi-NCR",
      aqi_input_type: state.source === "live" ? "live" : "preset",
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
        alert("Failed to synthesize resilience plan. Please retry.");
      }
    } catch (err) {
      console.error(err);
      alert("Error contacting assistant server.");
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

  // 11. Render Generated Blueprint
  function renderResults(data) {
    state.recommendations = data;

    // Risk Summary Card
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

    // Daily Routines
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

    // IAQ Hacks
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

    // Sustainable Alternatives
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
    resultsContainer.setAttribute("aria-label", "Resilience blueprint updated successfully");
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

  // 12. Print / Save Checklist
  printChecklistBtn.addEventListener("click", () => {
    window.print();
  });

  // Initialize
  checkHealth();
  updateGaugeArc(state.aqi);
  renderHotspots(DEFAULT_HOTSPOTS);
  init3DTilt();
  assistantForm.dispatchEvent(new Event("submit"));
});
