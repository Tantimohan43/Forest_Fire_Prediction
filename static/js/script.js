const map = L.map('map').setView([20.5937, 78.9629], 5); 

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  
}).addTo(map);

let marker = null;

map.on('click', (event) => {
  if (marker !== null) {
    map.removeLayer(marker);
  }

  const latitude = event.latlng.lat;
  const longitude = event.latlng.lng;

  marker = L.marker([latitude, longitude]).addTo(map);

  document.getElementById('latitude').value = latitude;
  document.getElementById('longitude').value = longitude;
});
