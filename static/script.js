// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.scan-panel').forEach(p => p.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
    });
});

// File upload handling
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const uploadScanBtn = document.getElementById('uploadScanBtn');

uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--accent-primary)';
});
uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = 'var(--border-color)';
});
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border-color)';
    const file = e.dataTransfer.files[0];
    if (file) handleFileSelect(file);
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) handleFileSelect(e.target.files[0]);
});

function handleFileSelect(file) {
    const allowedTypes = ['.py', '.js', '.php', '.java', '.cpp', '.c', '.go', '.rb', '.rs', '.swift', '.kt', '.ts'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(ext)) {
        alert('File type not allowed');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
        alert('File too large (max 5MB)');
        return;
    }
    
    fileInfo.style.display = 'block';
    fileInfo.innerHTML = `
        <i class="fas fa-file-code"></i>
        <span>${file.name} (${(file.size / 1024).toFixed(2)} KB)</span>
        <button onclick="removeFile()" class="icon-btn">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    uploadScanBtn.disabled = false;
    window.selectedFile = file;
}

function removeFile() {
    fileInfo.style.display = 'none';
    uploadScanBtn.disabled = true;
    fileInput.value = '';
    window.selectedFile = null;
}

// Scan functions
async function scanUpload() {
    if (!window.selectedFile) return;
    
    const formData = new FormData();
    formData.append('file', window.selectedFile);
    
    showLoading();
    
    try {
        const response = await fetch('/api/scan/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            displayResults(data);
        }
    } catch (error) {
        hideLoading();
        alert('Error: ' + error.message);
    }
}

async function scanPaste() {
    const code = document.getElementById('codeTextarea').value;
    const language = document.getElementById('languageSelect').value;
    
    if (!code.trim()) {
        alert('Please paste some code');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/scan/paste', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code, language})
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            displayResults(data);
        }
    } catch (error) {
        hideLoading();
        alert('Error: ' + error.message);
    }
}

async function scanGitHub() {
    const url = document.getElementById('githubUrl').value;
    
    if (!url) {
        alert('Please enter a GitHub URL');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/scan/github', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url})
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            displayResults(data);
        }
    } catch (error) {
        hideLoading();
        alert('Error: ' + error.message);
    }
}

function displayResults(data) {
    // Update summary cards
    document.getElementById('totalVulns').textContent = data.total_vulnerabilities || 0;
    document.getElementById('criticalCount').textContent = data.severity_counts?.CRITICAL || 0;
    document.getElementById('highCount').textContent = data.severity_counts?.HIGH || 0;
    document.getElementById('mediumCount').textContent = data.severity_counts?.MEDIUM || 0;
    document.getElementById('lowCount').textContent = data.severity_counts?.LOW || 0;
    document.getElementById('infoCount').textContent = data.severity_counts?.INFO || 0;
    
    // Update table
    const tbody = document.getElementById('vulnerabilitiesBody');
    
    if (!data.vulnerabilities || data.vulnerabilities.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No vulnerabilities found</td></tr>';
    } else {
        tbody.innerHTML = data.vulnerabilities.map(v => `
            <tr class="severity-${v.severity.toLowerCase()}">
                <td><span class="severity-badge ${v.severity.toLowerCase()}">${v.severity}</span></td>
                <td>${v.name}</td>
                <td>Line ${v.line}</td>
                <td>${v.description}<br><small><code>${v.code || ''}</code></small></td>
                <td>${v.fix}</td>
            </tr>
        `).join('');
    }
    
    // Show results
    document.getElementById('resultsDashboard').style.display = 'block';
    document.querySelector('.scan-tabs').scrollIntoView({behavior: 'smooth'});
}

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function copyCode() {
    const textarea = document.getElementById('codeTextarea');
    textarea.select();
    document.execCommand('copy');
    
    const btn = event.currentTarget;
    btn.innerHTML = '<i class="fas fa-check"></i>';
    setTimeout(() => btn.innerHTML = '<i class="fas fa-copy"></i>', 2000);
}

function clearCode() {
    document.getElementById('codeTextarea').value = '';
}

function downloadJSON() {
    // Implementation for downloading results as JSON
    alert('Download feature coming soon!');
}

// Load initial stats
fetch('/api/stats')
    .then(r => r.json())
    .then(stats => {
        document.getElementById('todayScans').textContent = stats.today || 0;
        document.getElementById('totalScans').textContent = stats.total || 0;
    });
