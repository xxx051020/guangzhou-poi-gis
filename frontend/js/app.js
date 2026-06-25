var currentPOIs = [];

document.addEventListener('DOMContentLoaded', initApp);

async function initApp() {
  document.getElementById('search-btn').addEventListener('click', handleSearch);
  document.getElementById('keyword').addEventListener('keyup', function(e) { if (e.key === 'Enter') handleSearch(); });
  document.getElementById('detail-modal').querySelector('.close').addEventListener('click', function() { document.getElementById('detail-modal').classList.add('hidden'); });
  document.getElementById('detail-modal').addEventListener('click', function(e) { if (e.target === this) this.classList.add('hidden'); });
  await loadCategories();
  await loadPOIs();
  await loadStats();
}

async function loadCategories() {
  try {
    var cats = await api.categories();
    var sel = document.getElementById('category-filter');
    cats.forEach(function(c) {
      var opt = document.createElement('option');
      opt.value = c.id;
      opt.textContent = c.name;
      sel.appendChild(opt);
    });
  } catch(e) { toast('Failed to load categories', 'error'); }
}

async function loadPOIs(skip) {
  skip = skip || 0;
  showLoading();
  try {
    var data = await api.listPOIs(skip, 100);
    currentPOIs = Array.isArray(data) ? data : [];
    renderPOIList();
    if (typeof addPOIsToMap === 'function') addPOIsToMap(currentPOIs);
  } catch(e) { toast('Failed to load POIs', 'error'); }
  hideLoading();
}

async function handleSearch() {
  var keyword = document.getElementById('keyword').value.trim();
  var catId = document.getElementById('category-filter').value;
  showLoading();
  try {
    if (catId && !keyword) {
      currentPOIs = await api.filterByCategory(parseInt(catId));
    } else if (keyword) {
      var result = await api.searchPOIs(keyword);
      currentPOIs = result.results || [];
    } else {
      var data = await api.listPOIs(0, 100);
      currentPOIs = Array.isArray(data) ? data : [];
    }
    renderPOIList();
    if (typeof addPOIsToMap === 'function') addPOIsToMap(currentPOIs);
  } catch(e) { toast('Search failed', 'error'); }
  hideLoading();
}

function renderPOIList() {
  var container = document.getElementById('poi-list');
  container.innerHTML = currentPOIs.map(function(p) {
    return '<div class="poi-card" onclick="showDetail(' + p.id + '); flyTo(' + p.lng + ',' + p.lat + ')">' +
      '<h4>' + escapeHtml(p.name) + '</h4>' +
      '<div class="meta"><span class="rating">? ' + (p.rating || '-') + '</span><span>' + (p.address || '') + '</span></div>' +
      '</div>';
  }).join('');
}

async function showDetail(id) {
  try {
    var poi = await api.getPOI(id);
    var reviews = [];
    try { reviews = await api.reviews(id); } catch(e) {}
    var modal = document.getElementById('modal-body');
    modal.innerHTML = '<h3>' + escapeHtml(poi.name) + '</h3>' +
      '<p><span class="tag">cat:' + poi.category_id + '</span> ? ' + (poi.rating || '-') + '</p>' +
      '<p>?? ' + escapeHtml(poi.address || 'No address') + '</p>' +
      '<p>?? ' + escapeHtml(poi.phone || 'No phone') + '</p>' +
      '<p>' + escapeHtml(poi.description || 'No description') + '</p>' +
      '<hr><h4>Reviews</h4>' +
      (reviews.length ? reviews.map(function(r) { return '<p><strong>' + escapeHtml(r.user_name) + '</strong> ?' + r.rating + ': ' + escapeHtml(r.comment || '') + '</p>'; }).join('') : '<p>No reviews yet</p>');
    document.getElementById('detail-modal').classList.remove('hidden');
  } catch(e) { toast('Failed to load details', 'error'); }
}

async function loadStats() {
  try {
    var s = await api.stats();
    document.getElementById('stats-bar').textContent = 'Total: ' + s.total + ' POIs | Avg Rating: ?' + s.avg_rating;
  } catch(e) {}
}

function toast(msg, type) {
  type = type || 'info';
  var el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'show ' + type;
  setTimeout(function() { el.className = ''; }, 3000);
}

function showLoading() { document.getElementById('poi-list').innerHTML = '<div style="padding:20px;text-align:center;color:#999">Loading...</div>'; }
function hideLoading() {}

function escapeHtml(str) {
  if (!str) return '';
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}
