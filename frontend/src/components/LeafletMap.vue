<template>
  <div id="leafletMap">
    <div id="map" class="rounded-4" style="height: 500px;"></div>
  </div>
</template>

<script setup>
import { onMounted, watch, computed } from 'vue';
import L from 'leaflet';
import store from '../store';

const position = computed(() => store.state.position);
const choosenPos = computed(() => store.state.choosenPos);

let map;
let currentMarker = null;
let chosenMarker = null;

onMounted(() => {
  map = L.map('map');

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);


  const customIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/5081/5081368.png', // your custom icon
    iconSize: [40, 40], // width, height
    iconAnchor: [20, 40], // where the icon "points"
    popupAnchor: [0, -35], // where popup opens relative to the icon
  });


  // Watch current position
  watch(position, (new_) => {
    if (!new_?.lat || !new_?.long) return;

    if (currentMarker) {
      map.removeLayer(currentMarker);
    }

    currentMarker = L.marker([new_.lat, new_.long])
      .addTo(map)
      .bindPopup('You are here')
      .openPopup();

    map.setView([new_.lat, new_.long], 15);
  }, { immediate: true });

  // Watch chosen position
  watch(choosenPos, (new_) => {
    if (!new_?.lat || !new_?.long) return;

    if (chosenMarker) {
      map.removeLayer(chosenMarker);
    }

    chosenMarker = L.marker([new_.lat, new_.long], {icon: customIcon})
      .addTo(map)
      .bindPopup(`Your chosen position:<br>${new_.lat.toFixed(5)}, ${new_.long.toFixed(5)}`)
      .openPopup();

  }, { immediate: true });

  // Click to set position
  map.on('click', (e) => {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    store.dispatch("choosePosition", {
      lat,
      long: lng,
    });
  });

  // ✅ Add custom control button to trigger "startTracking"
  const customControl = L.control({ position: 'topright' });

  customControl.onAdd = function () {
    const div = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
    div.style.backgroundColor = 'white';
    div.style.padding = '10px';
    div.style.cursor = 'pointer';
    div.style.borderRadius = '20px';
    div.innerHTML = '📍Your location';

    // ✅ Stop click propagation so Leaflet allows it
    L.DomEvent.disableClickPropagation(div);
    L.DomEvent.on(div, 'click', () => {
      store.dispatch('startTracking');
    });

    return div;
  };


  customControl.addTo(map);
});
</script>

<style>
#map {
  width: 100%;
}

.leaflet-control {
  font-size: 14px;
  font-weight: bold;
  text-align: center;
}
</style>
