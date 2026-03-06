/* ═══════════════════════════════════════════════════
   BOQ Extractor — Frontend Logic
   ═══════════════════════════════════════════════════ */

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// ─── DOM refs ───
const dropzone = $('#dropzone');
const fileInput = $('#fileInput');
const fileInfo = $('#fileInfo');
const fileName = $('#fileName');
const fileSize = $('#fileSize');
const industrySelect = $('#industrySelect');
const extractBtn = $('#extractBtn');
const resultsSection = $('#resultsSection');
const tableBody = $('#tableBody');
const searchInput = $('#searchInput');
const csvBtn = $('#csvBtn');
const emptyState = $('#emptyState');
const toast = $('#toast');

// Pipeline steps
const stepUpload = $('#step-upload');
const stepProcess = $('#step-process');
const stepResults = $('#step-results');

// ─── State ───
let selectedFile = null;
let extractedItems = [];
let sortCol = null;
let sortAsc = true;

// ═══════════════ DROPZONE ═══════════════

dropzone.addEventListener('click', () => fileInput.click());

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});

fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

function handleFile(file) {
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['xlsx', 'xls'].includes(ext)) {
        showToast('Only .xlsx and .xls files are supported.', 'error');
        return;
    }
    if (file.size > 10 * 1024 * 1024) {
        showToast('File too large. Max 10 MB.', 'error');
        return;
    }

    selectedFile = file;
    dropzone.classList.add('has-file');
    fileName.textContent = file.name;
    fileSize.textContent = `(${formatBytes(file.size)})`;
    fileInfo.classList.add('show');
    extractBtn.disabled = false;

    // Reset results
    resultsSection.classList.remove('show');
    setPipeline('upload');
}

// ═══════════════ EXTRACT ═══════════════

extractBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    extractBtn.classList.add('loading');
    extractBtn.disabled = true;
    setPipeline('process');

    const formData = new FormData();
    formData.append('file', selectedFile);

    const industry = industrySelect.value;

    try {
        const res = await fetch(`/extract?industry=${industry}`, {
            method: 'POST',
            body: formData,
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: 'Server error' }));
            throw new Error(err.detail || `HTTP ${res.status}`);
        }

        const data = await res.json();

        // Stats
        $('#statSheets').textContent = data.total_sheets || 0;
        $('#statSheetsData').textContent = (data.sheets_with_data || []).length;
        $('#statItems').textContent = data.extracted_items || 0;

        extractedItems = data.items || [];

        renderTable(extractedItems);

        resultsSection.classList.add('show');
        setPipeline('results');

        if (extractedItems.length === 0) {
            emptyState.style.display = 'block';
            showToast('No items extracted. Check your file.', 'info');
        } else {
            emptyState.style.display = 'none';
            showToast(`Extracted ${extractedItems.length} items successfully.`, 'success');
        }

    } catch (err) {
        showToast(err.message, 'error');
        setPipeline('upload');
    } finally {
        extractBtn.classList.remove('loading');
        extractBtn.disabled = false;
    }
});

// ═══════════════ TABLE RENDER ═══════════════

function renderTable(items) {
    tableBody.innerHTML = '';

    if (items.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    emptyState.style.display = 'none';

    items.forEach((item, i) => {
        const tr = document.createElement('tr');
        tr.style.animationDelay = `${i * 20}ms`;
        const catClass = (item.category || 'misc').toLowerCase().replace(/[^a-z]/g, '-').replace(/-+/g, '-');
        tr.innerHTML = `
      <td>${esc(item.product)}</td>
      <td>${esc(item.brand)}</td>
      <td>${item.quantity}</td>
      <td><span class="cat-badge ${catClass}">${esc(item.category)}</span></td>
    `;
        tableBody.appendChild(tr);
    });
}

// ═══════════════ SEARCH ═══════════════

searchInput.addEventListener('input', () => {
    const q = searchInput.value.toLowerCase();
    const filtered = extractedItems.filter(
        (i) =>
            i.product.toLowerCase().includes(q) ||
            i.brand.toLowerCase().includes(q) ||
            i.category.toLowerCase().includes(q)
    );
    renderTable(filtered);
});

// ═══════════════ SORT ═══════════════

$$('.data-table th').forEach((th) => {
    th.addEventListener('click', () => {
        const col = th.dataset.col;
        if (sortCol === col) {
            sortAsc = !sortAsc;
        } else {
            sortCol = col;
            sortAsc = true;
        }

        // Visual
        $$('.data-table th').forEach((h) => h.classList.remove('sorted'));
        th.classList.add('sorted');
        th.querySelector('.sort-arrow').textContent = sortAsc ? '▲' : '▼';

        const sorted = [...extractedItems].sort((a, b) => {
            let va = a[col], vb = b[col];
            if (col === 'quantity') return sortAsc ? va - vb : vb - va;
            va = String(va).toLowerCase();
            vb = String(vb).toLowerCase();
            return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
        });

        renderTable(sorted);
    });
});

// ═══════════════ CSV DOWNLOAD ═══════════════

csvBtn.addEventListener('click', () => {
    if (extractedItems.length === 0) return;

    const header = 'Product,Brand,Quantity,Category\n';
    const rows = extractedItems
        .map((i) => `"${i.product}","${i.brand}",${i.quantity},"${i.category}"`)
        .join('\n');

    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'boq_extracted.csv';
    a.click();
    URL.revokeObjectURL(url);
    showToast('CSV downloaded.', 'success');
});

// ═══════════════ PIPELINE STEPS ═══════════════

function setPipeline(stage) {
    [stepUpload, stepProcess, stepResults].forEach((s) => {
        s.classList.remove('active', 'done');
    });

    if (stage === 'upload') {
        stepUpload.classList.add('active');
    } else if (stage === 'process') {
        stepUpload.classList.add('done');
        stepProcess.classList.add('active');
    } else if (stage === 'results') {
        stepUpload.classList.add('done');
        stepProcess.classList.add('done');
        stepResults.classList.add('active');
    }
}

// ═══════════════ UTILS ═══════════════

function showToast(msg, type = 'info') {
    toast.textContent = msg;
    toast.className = `toast ${type} show`;
    setTimeout(() => toast.classList.remove('show'), 4000);
}

function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

function esc(str) {
    const d = document.createElement('div');
    d.textContent = str || '';
    return d.innerHTML;
}
