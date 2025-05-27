<template>
  <div id="leafletMap">
    <div id="map" class=" rounded-5 shadow-lg" style="height: 500px;"></div>
  </div>

</template>

<script>
import L from 'leaflet';

export default {
  name: "LeafletMap",
  mounted() {
    const map = L.map('map').setView([12.9716, 77.5946], 13); // Default: Bangalore

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Get current user location
    navigator.geolocation.getCurrentPosition(pos => {
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      L.marker([lat, lon]).addTo(map).bindPopup('You are here').openPopup();
      map.setView([lat, lon], 15);
    });

    // Add example parking locations (could be dynamic)
    const parkingSpots = [
      { name: "Mall Parking", lat: 12.975, lon: 77.59 },
      { name: "Street Parking", lat: 12.972, lon: 77.598 }
    ];

    parkingSpots.forEach(spot => {
      L.marker([spot.lat, spot.lon])
        .addTo(map)
        .bindPopup(`<b>${spot.name}</b>`);
    });
  }
};
</script>

<style>
#map {
  width: 100%;
}
</style>
