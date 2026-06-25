const API_BASE = 'http://localhost:8000';

const api = {
  async fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return res.json();
  },

  async listPOIs(skip, limit) {
    skip = skip || 0;
    limit = limit || 50;
    return this.fetchJSON(API_BASE + '/api/pois?skip=' + skip + '&limit=' + limit);
  },

  async getPOI(id) {
    return this.fetchJSON(API_BASE + '/api/pois/' + id);
  },

  async searchPOIs(keyword) {
    return this.fetchJSON(API_BASE + '/api/pois/search/?keyword=' + encodeURIComponent(keyword));
  },

  async filterByCategory(catId) {
    return this.fetchJSON(API_BASE + '/api/pois/filter/category/' + catId);
  },

  async nearby(lng, lat, radius) {
    radius = radius || 3000;
    return this.fetchJSON(API_BASE + '/api/pois/nearby/?lng=' + lng + '&lat=' + lat + '&radius=' + radius);
  },

  async bbox(west, south, east, north) {
    return this.fetchJSON(API_BASE + '/api/pois/bbox/?west=' + west + '&south=' + south + '&east=' + east + '&north=' + north);
  },

  async geojsonAll() {
    return this.fetchJSON(API_BASE + '/api/pois/geojson/all');
  },

  async stats() {
    return this.fetchJSON(API_BASE + '/api/pois/stats/');
  },

  async categories() {
    return this.fetchJSON(API_BASE + '/api/categories');
  },

  async reviews(poiId) {
    return this.fetchJSON(API_BASE + '/api/pois/' + poiId + '/reviews');
  }
};
