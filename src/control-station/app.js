const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Request failed: ${res.status}`);
  }
  return res.json();
}

function badgeClass(status) {
  return status === 'CRITICAL' ? 'critical' : status === 'WARNING' ? 'warning' : 'safe';
}

function renderSummary(workers, alerts, rover) {
  const counts = workers.reduce((a, w) => {
    a[w.status] = (a[w.status] || 0) + 1;
    return a;
  }, {});
  const critical = alerts.filter(a => a.status === 'CRITICAL' && !a.acknowledged).length;
  $('summaryCards').innerHTML = [
    ['WORKERS', workers.length, `${counts.SAFE || 0} safe`],
    ['WARNING', counts.WARNING || 0, 'workers require attention'],
    ['CRITICAL', counts.CRITICAL || 0, 'active critical condition'],
    ['ROVER', rover.status || 'READY', rover.target_zone ? `Target ${rover.target_zone}` : 'Standing by'],
  ].map(([label, value, detail]) => `<div class="card"><div class="label">${label}</div><div class="value">${value}</div><div class="detail">${detail}</div></div>`).join('');
  $('criticalBadge').textContent = `${critical} CRITICAL`;
  $('criticalBadge').className = `badge ${critical ? 'critical' : 'safe'}`;
}

function renderWorkers(workers) {
  $('workers').innerHTML = workers.length ? workers.map(w => `
    <div class="worker-row">
      <div><div class="worker-name">${w.name}</div><div class="muted">${w.worker_id}</div></div>
      <div><span class="pill ${badgeClass(w.status)}">${w.status}</span></div>
      <div>📍 ${w.zone}</div>
      <div>❤ ${w.heart_rate ?? '--'} bpm</div>
    </div>`).join('') : '<div class="muted">No workers reported.</div>';

  document.querySelectorAll('.node').forEach(n => n.classList.remove('warning', 'critical'));
  workers.forEach(w => {
    const node = document.querySelector(`[data-zone="${w.zone}"]`);
    if (node && w.status !== 'SAFE') node.classList.add(w.status === 'CRITICAL' ? 'critical' : 'warning');
  });
}

function renderAlerts(alerts) {
  $('alerts').innerHTML = alerts.length ? alerts.map(a => `
    <div class="alert">
      <div class="alert-head"><span>🚨 ${a.alert_type} — ${a.worker_id || 'SYSTEM'}</span><span class="pill ${badgeClass(a.status)}">${a.status} ${a.risk_score}%</span></div>
      <small>📍 ${a.location || 'UNKNOWN'} · ${a.message}</small>
      <small>${new Date(a.created_at).toLocaleString()} ${a.acknowledged ? '· Acknowledged' : ''}</small>
      ${!a.acknowledged ? `<button class="btn ghost" style="margin-top:8px;padding:6px 9px;font-size:11px" onclick="ack(${a.id})">Acknowledge</button>` : ''}
    </div>`).join('') : '<div class="muted">No active alerts. System clear.</div>';
}

function renderEnvironment(env) {
  $('environment').innerHTML = [
    ['Gas indication', env.gas ?? '--', 'sensor units'],
    ['Temperature', env.temperature ?? '--', '°C'],
    ['Humidity', env.humidity ?? '--', '%'],
  ].map(([l,v,u]) => `<div class="metric"><div class="m-label">${l}</div><div class="m-value">${v}</div><div class="muted">${u}</div></div>`).join('');
}

function renderRover(rover) {
  const cls = rover.status === 'DEPLOYED' ? 'critical' : 'safe';
  $('roverStatus').textContent = rover.status || 'READY';
  $('roverStatus').className = `badge ${cls}`;
  $('roverData').innerHTML = [
    ['Status', rover.status || 'READY'],
    ['Target', rover.target_zone || '--'],
    ['Camera', rover.camera_online ? 'ONLINE' : 'OFFLINE'],
    ['Gas', rover.gas ?? '--'],
    ['Temp', rover.temperature ?? '--'],
    ['Obstacle', rover.obstacle ? 'DETECTED' : 'CLEAR'],
  ].map(([k,v]) => `<div class="kv"><span>${k}</span><b>${v}</b></div>`).join('');
}

async function refresh() {
  try {
    const [workers, alerts, env, rover] = await Promise.all([
      api('/api/workers'), api('/api/alerts'), api('/api/environment'), api('/api/rover')
    ]);
    renderSummary(workers, alerts, rover);
    renderWorkers(workers);
    renderAlerts(alerts);
    renderEnvironment(env);
    renderRover(rover);
    $('workerUpdated').textContent = `Updated ${new Date().toLocaleTimeString()}`;
  } catch (err) {
    console.error(err);
  }
}

window.ack = async (id) => {
  await api(`/api/alerts/${id}/acknowledge`, { method: 'POST', body: '{}' });
  refresh();
};

$('resetBtn').onclick = async () => {
  await api('/api/demo/reset', { method: 'POST', body: '{}' });
  refresh();
};

$('emergencyBtn').onclick = async () => {
  await api('/api/demo/emergency', { method: 'POST', body: '{}' });
  refresh();
};

$('deployBtn').onclick = async () => {
  const worker = (await api('/api/workers')).find(w => w.status === 'CRITICAL') || (await api('/api/workers'))[0];
  await api('/api/rover/deploy', { method: 'POST', body: JSON.stringify({ target_zone: worker?.zone || 'N4' }) });
  refresh();
};

$('resetRoverBtn').onclick = async () => {
  await api('/api/rover/reset', { method: 'POST', body: '{}' });
  refresh();
};

refresh();
setInterval(refresh, 2500);
