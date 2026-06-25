var map = new ol.Map({
  target: 'map',
  layers: [new ol.layer.Tile({source: new ol.source.OSM()})],
  view: new ol.View({center: ol.proj.fromLonLat([113.2644, 23.1291]), zoom: 12})
});

var poiSource = new ol.source.Vector();
var poiLayer = new ol.layer.Vector({
  source: poiSource,
  style: new ol.style.Style({
    image: new ol.style.Circle({radius: 8, fill: new ol.style.Fill({color: '#1a73e8'}), stroke: new ol.style.Stroke({color: '#fff', width: 2})})
  })
});
map.addLayer(poiLayer);

var popupOverlay = null;

map.on('click', function(evt) {
  if (popupOverlay) { map.removeOverlay(popupOverlay); popupOverlay = null; }
});

function addPOIsToMap(pois) {
  poiSource.clear();
  pois.forEach(function(p) {
    var feature = new ol.Feature({
      geometry: new ol.geom.Point(ol.proj.fromLonLat([p.lng, p.lat])),
      name: p.name,
      id: p.id,
      category_id: p.category_id,
      rating: p.rating
    });
    poiSource.addFeature(feature);
  });
}

map.on('pointermove', function(evt) {
  map.getTargetElement().style.cursor = map.hasFeatureAtPixel(evt.pixel) ? 'pointer' : '';
});

map.on('singleclick', function(evt) {
  var feature = map.forEachFeatureAtPixel(evt.pixel, function(f) { return f; });
  if (feature) {
    var props = feature.getProperties();
    if (popupOverlay) map.removeOverlay(popupOverlay);
    var el = document.createElement('div');
    el.style.cssText = 'background:#fff;padding:8px 12px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.3);font-size:13px;white-space:nowrap;';
    el.innerHTML = '<strong>' + (props.name || '') + '</strong><br>? ' + (props.rating || '-');
    popupOverlay = new ol.Overlay({element: el, positioning: 'bottom-center', stopEvent: false});
    map.addOverlay(popupOverlay);
    popupOverlay.setPosition(feature.getGeometry().getCoordinates());
    if (typeof showDetail === 'function') showDetail(props.id);
  }
});

function flyTo(lng, lat, zoom) {
  zoom = zoom || 15;
  map.getView().animate({center: ol.proj.fromLonLat([lng, lat]), zoom: zoom, duration: 800});
}
