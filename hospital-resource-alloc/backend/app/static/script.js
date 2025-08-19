// === Clock ===
function updateClock() {
  document.getElementById("clock").innerText = new Date().toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

// === API + WebSocket ===
const API_BASE = "http://127.0.0.1:8000";
const HOSPITAL_ID = 1;
let ws;

function connectWebSocket() {
  ws = new WebSocket(API_BASE.replace(/^http/, "ws") + "/ws/resources");
  ws.onopen = () => console.log("WS connected");
  ws.onclose = () => setTimeout(connectWebSocket, 2000);
  ws.onerror = (e) => console.error(e);

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    if (msg.type === "resource_update") updateHospitalDOM(msg.summary);
    else if (msg.type === "active_patients") updateActivePatientsTable(msg.patients);
    else if (msg.type === "waiting_patients") updateWaitingPatientsTable(msg.patients);
  };
}
connectWebSocket();

// === Update Hospital DOM & Summary Cards ===
function updateHospitalDOM(h) {
  // --- Resource Text + Progress Bars ---
  const bedsEl = document.getElementById("beds");
  bedsEl.innerText = `${h.available_beds ?? h.total_beds ?? 0} / ${h.total_beds ?? 0}`;
  const bedOcc = (h.total_beds - h.available_beds) / h.total_beds;
  bedsEl.style.color = bedOcc >= 0.8 ? "red" : bedOcc >= 0.5 ? "orange" : "green";
  const bedsBar = document.getElementById("beds-bar");
  bedsBar.style.width = `${bedOcc * 100}%`;
  bedsBar.style.backgroundColor = bedsEl.style.color;

  const ventsEl = document.getElementById("ventilators");
  ventsEl.innerText = `${h.available_ventilators ?? h.ventilators ?? 0} / ${h.ventilators ?? 0}`;
  const ventOcc = (h.ventilators - h.available_ventilators) / h.ventilators;
  ventsEl.style.color = ventOcc >= 0.8 ? "red" : ventOcc >= 0.5 ? "orange" : "green";
  const ventsBar = document.getElementById("vents-bar");
  ventsBar.style.width = `${ventOcc * 100}%`;
  ventsBar.style.backgroundColor = ventsEl.style.color;

  const oxyEl = document.getElementById("oxygen");
  oxyEl.innerText = h.oxygen_cylinders ?? 0;
  oxyEl.style.color = (h.oxygen_cylinders ?? 0) <= 5 ? "red" : "green";
  oxyEl.className = (h.oxygen_cylinders ?? 0) <= 5 ? "blink" : "";

  const staffEl = document.getElementById("staff");
  staffEl.innerText = h.staff ?? 0;
  staffEl.style.color = (h.staff ?? 0) < 5 ? "red" : "green";
  staffEl.className = (h.staff ?? 0) < 5 ? "blink" : "";

  // --- Summary Cards ---
  const totalPatients = (h.active_patients?.length ?? 0) + (h.waiting_patients?.length ?? 0);
  document.getElementById("total-patients").innerText = `Total Patients: ${totalPatients}`;

  const occupiedBeds = (h.total_beds ?? 0) - (h.available_beds ?? 0);
  document.getElementById("occupied-beds").innerText = `Occupied Beds: ${occupiedBeds}`;

  document.getElementById("available-vents").innerText = `Available Ventilators: ${h.available_ventilators ?? h.ventilators ?? 0}`;
  document.getElementById("available-oxygen").innerText = `Oxygen Cylinders: ${h.oxygen_cylinders ?? 0}`;
}

// === Update Active Patients Table ===
function updateActivePatientsTable(patients) {
  const tbody = document.getElementById("active-patients");
  tbody.innerHTML = "";
  patients.forEach(p => {
    let color = "black";
    const res = p.resource?.toLowerCase() || "";
    if (res.includes("icu") || res.includes("ventilator")) color = "red";
    else if (res.includes("bed")) color = "orange";
    const row = document.createElement("tr");
    row.innerHTML = `<td>${p.id}</td><td>${p.condition}</td><td style="color:${color}">${p.resource}</td>
                     <td><button onclick="dischargePatient(${p.id})">Discharge</button></td>`;
    tbody.appendChild(row);
  });
}

// === Update Waiting Patients Table ===
function updateWaitingPatientsTable(patients) {
  const tbody = document.getElementById("waiting-patients");
  tbody.innerHTML = "";
  patients.forEach(p => {
    let color = "black";
    const res = p.requested_resource?.toLowerCase() || "";
    if (res.includes("icu") || res.includes("ventilator")) color = "red";
    else if (res.includes("bed")) color = "orange";
    const row = document.createElement("tr");
    row.innerHTML = `<td>${p.id}</td><td>${p.condition}</td><td style="color:${color}">${p.requested_resource}</td>`;
    tbody.appendChild(row);
  });
}

// === Register Patient ===
document.getElementById("patient-form").addEventListener("submit", async e => {
  e.preventDefault();
  const condition = document.getElementById("condition").value;
  try {
    const res = await fetch(`${API_BASE}/requests/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ hospital_id: HOSPITAL_ID, condition })
    });
    if (res.ok) {
      logAction(`New patient registered (${condition})`);
      document.getElementById("condition").value = "";
    }
  } catch (e) { console.error(e); }
});

// === Discharge Patient ===
async function dischargePatient(id) {
  try {
    const res = await fetch(`${API_BASE}/allocations/discharge/${id}`, { method: "POST" });
    if (res.ok) logAction(`Patient #${id} discharged`);
  } catch (e) { console.error(e); }
}

// === Logs ===
function logAction(msg) {
  const logs = document.getElementById("logs");
  const li = document.createElement("li");
  li.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
  logs.prepend(li);
}

// === Initial Load Fallback ===
async function initialLoad() {
  try {
    const res = await fetch(`${API_BASE}/hospitals/`);
    const h = await res.json();
    updateHospitalDOM(h);

    const aRes = await fetch(`${API_BASE}/allocations/active/${HOSPITAL_ID}`);
    const ap = await aRes.json();
    updateActivePatientsTable(ap);

    const wRes = await fetch(`${API_BASE}/requests/waiting/${HOSPITAL_ID}`);
    const wp = await wRes.json();
    updateWaitingPatientsTable(wp);
  } catch (e) { console.error(e); }
}
initialLoad();
