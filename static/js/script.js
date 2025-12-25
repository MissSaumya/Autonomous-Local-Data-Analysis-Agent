async function startProcess() {
    const file = document.getElementById('csvFile').files[0];
    if(!file) return alert("Select a file!");

    const status = document.getElementById('statusContainer');
    status.classList.remove('hidden');
    
    try {
        updateStatus('s1', '🔵 Preparing Data...');
        const fd = new FormData(); fd.append('file', file);
        await fetch('/upload', {method: 'POST', body: fd});
        updateStatus('s1', '✅ Data Ready');

        updateStatus('s2', '🔵 Recognizing Dataset...');
        const idRes = await fetch('/identify', {method: 'POST'});
        const idData = await idRes.json();
        document.getElementById('datasetInfo').innerHTML = idData.info;
        updateStatus('s2', '✅ Identity Found');

        updateStatus('s4', '🔵 Finalizing (Max 60s)...');
        const anaRes = await fetch('/analyze', {method: 'POST'});
        if (!anaRes.ok) throw new Error("Backend timeout. Retrying...");
        const anaData = await anaRes.json();
        
        updateStatus('s4', '✅ Analysis Complete');
        document.getElementById('resultSection').classList.remove('hidden');
        document.getElementById('edaPlot').src = anaData.plot + "?t=" + Date.now();
        document.getElementById('edaContent').innerHTML = anaData.eda;

    } catch (e) {
        alert("CRITICAL ERROR: " + e.message);
        document.querySelector('.loading-circle').style.display = 'none';
    }
}

function updateStatus(id, text) {
    const el = document.getElementById(id);
    el.innerText = text;
    if(text.includes('✅')) el.style.color = "#28a745";
}