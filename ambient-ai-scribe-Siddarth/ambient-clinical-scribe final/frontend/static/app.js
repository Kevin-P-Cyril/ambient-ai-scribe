const patientSelect = document.getElementById('patientSelect');
const refreshPatientsBtn = document.getElementById('refreshPatients');
const newPatientName = document.getElementById('newPatientName');
const createPatientBtn = document.getElementById('createPatientBtn');
const audioInput = document.getElementById('audioInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadFileName = document.querySelector('.upload-file-name');
const saveEncounterBtn = document.getElementById('saveEncounterBtn');
const exportPdfBtn = document.getElementById('exportPdfBtn');
const statusEl = document.getElementById('status');
const progressEl = document.getElementById('uploadProgress');
const percentEl = document.getElementById('uploadPercent');
const transcriptOutput = document.getElementById('transcriptOutput');
const soapSubjective = document.getElementById('soapSubjective');
const soapObjective = document.getElementById('soapObjective');
const soapAssessment = document.getElementById('soapAssessment');
const soapPlan = document.getElementById('soapPlan');
const icdChecklist = document.getElementById('icdChecklist');
const finalizeBtn = document.getElementById('finalizeBtn');
const downloadEhrBtn = document.getElementById('downloadEhrBtn');
const signOffStatus = document.getElementById('signOffStatus');
const historyList = document.getElementById('historyList');
const navLinks = document.querySelectorAll('.nav-link');
const panels = document.querySelectorAll('.panel');
const menuToggle = document.querySelector('.menu-toggle');
const siteNav = document.querySelector('.site-nav');

let latestResult = null;
let selectedPatientId = '';
let currentEncounterId = null;
let icdApprovals = []; // [{code, description, approved}]

function setStatus(message, type = 'info') {
  statusEl.textContent = message;
  statusEl.className = `status ${type === 'error' ? 'error' : type === 'success' ? 'success' : ''}`;
}

const uploadDropzone = document.querySelector('.upload-dropzone');
const audioPreview = document.getElementById('audioPreview');

function setSelectedFile(file) {
  if (!file) {
    uploadFileName.textContent = 'No file selected';
    if (audioPreview) {
      audioPreview.src = '';
      audioPreview.hidden = true;
    }
    uploadBtn.disabled = true;
    return;
  }

  // basic validation
  if (!file.type.startsWith('audio') && !/\.(mp3|wav|m4a)$/i.test(file.name)) {
    setStatus('Unsupported file type. Please provide MP3/WAV/M4A.', 'error');
    audioInput.value = '';
    setSelectedFile(null);
    return;
  }

  uploadFileName.textContent = file.name;
  uploadBtn.disabled = false;

  if (audioPreview) {
    audioPreview.hidden = false;
    try {
      const url = URL.createObjectURL(file);
      audioPreview.src = url;
    } catch (e) {
      console.warn('Could not create audio preview', e);
      audioPreview.hidden = true;
    }
  }
}

// click to open file picker
uploadDropzone?.addEventListener('click', () => audioInput?.click());

// drag & drop support
uploadDropzone?.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadDropzone.classList.add('dragover');
});
uploadDropzone?.addEventListener('dragleave', () => uploadDropzone.classList.remove('dragover'));
uploadDropzone?.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadDropzone.classList.remove('dragover');
  const f = e.dataTransfer?.files?.[0];
  if (f) {
    // set the input's files so uploadAudio reads correctly
    try {
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(f);
      audioInput.files = dataTransfer.files;
    } catch (err) {
      // some browsers may not allow setting input.files; fall back
      console.warn('Could not set input.files programmatically', err);
    }
    setSelectedFile(f);
  }
});

audioInput?.addEventListener('change', () => {
  const file = audioInput.files?.[0];
  setSelectedFile(file);
});

function formatJson(value) {
  if (!value) return 'No results.';
  return typeof value === 'string' ? value : JSON.stringify(value, null, 2);
}

function getField(soap, key) {
  if (!soap) return '';
  return soap[key] ?? soap[key.charAt(0).toUpperCase() + key.slice(1)] ?? '';
}

function renderSoap(soap) {
  soapSubjective.value = getField(soap, 'subjective');
  soapObjective.value = getField(soap, 'objective');
  soapAssessment.value = getField(soap, 'assessment');
  soapPlan.value = getField(soap, 'plan');
}

function currentSoapFromForm() {
  return {
    subjective: soapSubjective.value,
    objective: soapObjective.value,
    assessment: soapAssessment.value,
    plan: soapPlan.value,
  };
}

function renderIcdChecklist(icdCodes) {
  icdApprovals = (icdCodes || []).map((c) => ({ ...c, approved: true }));
  if (!icdApprovals.length) {
    icdChecklist.innerHTML = '<div class="placeholder">No ICD suggestions yet.</div>';
    return;
  }
  icdChecklist.innerHTML = icdApprovals
    .map(
      (c, i) => `
      <label class="icd-item">
        <input type="checkbox" data-idx="${i}" checked />
        <span class="icd-code">${c.code}</span>
        <span class="icd-desc">${c.description || ''}</span>
      </label>`
    )
    .join('');
  icdChecklist.querySelectorAll('input[type="checkbox"]').forEach((box) => {
    box.addEventListener('change', (e) => {
      const idx = Number(e.target.dataset.idx);
      icdApprovals[idx].approved = e.target.checked;
    });
  });
}

function approvedIcdCodes() {
  return icdApprovals.filter((c) => c.approved).map(({ approved, ...rest }) => rest);
}

function updateActionButtons() {
  saveEncounterBtn.disabled = !latestResult || !selectedPatientId;
  exportPdfBtn.disabled = !latestResult || !latestResult.soap_note;
  finalizeBtn.disabled = !currentEncounterId;
  downloadEhrBtn.disabled = !currentEncounterId;
}

async function apiRequest(method, path, body = null, asBlob = false) {
  const options = { method, headers: {} };
  if (body && !(body instanceof FormData)) {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(body);
  } else if (body instanceof FormData) {
    options.body = body;
  }
  const res = await fetch(path, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `${res.status} ${res.statusText}`);
  }
  return asBlob ? res.blob() : res.json();
}

async function loadPatients() {
  try {
    const data = await apiRequest('GET', '/patients');
    patientSelect.innerHTML = '<option value="">Select existing patient</option>';
    if (data.length === 0) {
      patientSelect.innerHTML += '<option value="" disabled>No patients available</option>';
    }
    data.forEach((patient) => {
      const option = document.createElement('option');
      option.value = patient.id;
      option.textContent = `${patient.name} (${new Date(patient.created_at).toLocaleDateString()})`;
      patientSelect.append(option);
    });
    if (data.length > 0 && !selectedPatientId) {
      patientSelect.value = '';
    }
  } catch (err) {
    console.error(err);
    setStatus('Failed to load patients', 'error');
  }
}

async function createPatient() {
  const name = newPatientName.value.trim();
  if (!name) {
    setStatus('Enter a patient name first', 'error');
    return;
  }
  try {
    await apiRequest('POST', '/patients', { name });
    newPatientName.value = '';
    setStatus('Patient created', 'success');
    await loadPatients();
  } catch (err) {
    console.error(err);
    setStatus('Patient creation failed', 'error');
  }
}

async function loadHistory() {
  if (!selectedPatientId) {
    historyList.innerHTML = '<div class="placeholder">Select a patient and click refresh to see history.</div>';
    return;
  }
  try {
    const data = await apiRequest('GET', `/patients/${selectedPatientId}/encounters`);
    if (!data.length) {
      historyList.innerHTML = '<div class="placeholder">No encounters found for this patient.</div>';
      return;
    }
    historyList.innerHTML = data.map((enc) => {
      const soap = enc.soap ? JSON.stringify(enc.soap, null, 2) : 'No SOAP note';
      const icd = enc.icd_codes ? JSON.stringify(enc.icd_codes, null, 2) : 'No ICD codes';
      return `
        <div class="history-item">
          <h4>Encounter ${enc.id}</h4>
          <p>${new Date(enc.created_at).toLocaleString()}</p>
          <strong>Transcript</strong>
          <pre>${enc.transcript || 'No transcript available.'}</pre>
          <strong>SOAP</strong>
          <pre>${soap}</pre>
          <strong>ICD Codes</strong>
          <pre>${icd}</pre>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error(err);
    historyList.innerHTML = '<div class="placeholder">Failed to load history.</div>';
  }
}

async function uploadAudio(file) {
  if (!file || !file.type.startsWith('audio')) {
    setStatus('Please upload a valid audio file', 'error');
    return;
  }

  const form = new FormData();
  form.append('file', file, file.name);

  setStatus('Uploading audio...', 'info');
  progressEl.value = 0;
  percentEl.textContent = '0%';

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload-audio');

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const pct = Math.round((event.loaded / event.total) * 100);
        progressEl.value = pct;
        percentEl.textContent = `${pct}%`;
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const data = JSON.parse(xhr.responseText);
          latestResult = data;
          currentEncounterId = null;
          signOffStatus.textContent = '';
          transcriptOutput.textContent = data.transcript || 'No transcript generated.';
          renderSoap(data.soap_note);
          renderIcdChecklist(data.icd_codes);
          setStatus('Processing complete', 'success');
          progressEl.value = 100;
          percentEl.textContent = '100%';
          updateActionButtons();
          resolve(data);
        } catch (parseErr) {
          console.error(parseErr);
          setStatus('Could not parse server response', 'error');
          reject(parseErr);
        }
      } else {
        console.error(xhr.responseText || xhr.statusText);
        setStatus(`Upload failed: ${xhr.status} ${xhr.statusText}`, 'error');
        reject(new Error(xhr.statusText || 'Upload failed'));
      }
    };

    xhr.onerror = () => {
      setStatus('Network error during upload', 'error');
      reject(new Error('Network error'));
    };

    xhr.send(form);
  });
}

async function saveEncounter() {
  if (!selectedPatientId) {
    setStatus('Select a patient before saving', 'error');
    return;
  }
  if (!latestResult) {
    setStatus('No transcription result to save', 'error');
    return;
  }
  try {
    const result = await apiRequest('POST', `/patients/${selectedPatientId}/encounters`, {
      transcript: latestResult.transcript,
      soap: currentSoapFromForm(),
      icd_codes: approvedIcdCodes()
    });
    currentEncounterId = result.id;
    signOffStatus.textContent = 'Saved (not yet finalized)';
    updateActionButtons();
    setStatus('Encounter saved', 'success');
    loadHistory();
  } catch (err) {
    console.error(err);
    setStatus('Failed to save encounter', 'error');
  }
}

async function finalizeEncounter() {
  if (!currentEncounterId) {
    setStatus('Save the encounter before signing off', 'error');
    return;
  }
  try {
    await apiRequest('PUT', `/encounters/${currentEncounterId}`, {
      soap: currentSoapFromForm(),
      icd_codes: approvedIcdCodes(),
      transcript: latestResult?.transcript,
      status: 'Finalized'
    });
    signOffStatus.textContent = '✅ Finalized & signed off';
    setStatus('Encounter finalized', 'success');
    loadHistory();
  } catch (err) {
    console.error(err);
    setStatus('Finalize failed', 'error');
  }
}

function downloadEhrJson() {
  if (!currentEncounterId) {
    setStatus('Save the encounter before exporting to EHR', 'error');
    return;
  }
  const payload = {
    encounter_id: currentEncounterId,
    patient_id: selectedPatientId,
    transcript: latestResult?.transcript || '',
    soap_note: currentSoapFromForm(),
    icd_10_codes: approvedIcdCodes(),
    signed_off: signOffStatus.textContent.includes('Finalized'),
    exported_at: new Date().toISOString()
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `encounter_${currentEncounterId}_ehr_payload.json`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  setStatus('EHR JSON downloaded', 'success');
}

async function exportPdf() {
  if (!latestResult || !latestResult.soap_note) {
    setStatus('No SOAP note available for export', 'error');
    return;
  }
  try {
    setStatus('Generating PDF...', 'info');
    const pdfBlob = await apiRequest('POST', '/export?format=pdf', { soap_note: currentSoapFromForm() }, true);
    const url = URL.createObjectURL(pdfBlob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'soap_note.pdf';
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
    setStatus('PDF downloaded', 'success');
  } catch (err) {
    console.error(err);
    setStatus('Export failed', 'error');
  }
}

function handleNavigation(event) {
  const target = event.currentTarget.dataset.target;
  navLinks.forEach((link) => link.classList.toggle('active', link.dataset.target === target));
  panels.forEach((panel) => panel.classList.toggle('hidden', panel.id !== target));
  const section = document.getElementById(target);
  section?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  closeMenu();
}

function updateActiveNav() {
  const offset = window.innerHeight * 0.15;
  let currentSection = 'upload-section';

  panels.forEach((panel) => {
    const rect = panel.getBoundingClientRect();
    if (rect.top - offset <= 0 && rect.bottom - offset > 0) {
      currentSection = panel.id;
    }
  });

  navLinks.forEach((link) => {
    link.classList.toggle('active', link.dataset.target === currentSection);
  });
}

patientSelect.addEventListener('change', () => {
  selectedPatientId = patientSelect.value;
  updateActionButtons();
  loadHistory();
});
refreshPatientsBtn.addEventListener('click', loadPatients);
createPatientBtn.addEventListener('click', createPatient);
uploadBtn.addEventListener('click', async () => {
  const file = audioInput.files[0];
  if (!file) {
    setStatus('Please select an audio file', 'error');
    return;
  }
  await uploadAudio(file);
});
saveEncounterBtn.addEventListener('click', saveEncounter);
exportPdfBtn.addEventListener('click', exportPdf);
finalizeBtn.addEventListener('click', finalizeEncounter);
downloadEhrBtn.addEventListener('click', downloadEhrJson);
function closeMenu() {
  if (siteNav) {
    siteNav.classList.remove('open');
  }
  if (menuToggle) {
    menuToggle.classList.remove('active');
    menuToggle.setAttribute('aria-expanded', 'false');
  }
  document.body.classList.remove('menu-open');
}

menuToggle?.addEventListener('click', () => {
  if (!siteNav) return;
  const isOpen = siteNav.classList.toggle('open');
  menuToggle.classList.toggle('active', isOpen);
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  document.body.classList.toggle('menu-open', isOpen);
});

navLinks.forEach((link) => link.addEventListener('click', handleNavigation));
window.addEventListener('scroll', updateActiveNav, { passive: true });
window.addEventListener('resize', updateActiveNav);

window.addEventListener('load', async () => {
  await loadPatients();
  updateActionButtons();
  updateActiveNav();
  setStatus('Ready');
});
