<template>
  <div id="leafletMap" class=" text-black">
    <div id="map" class="rounded-4" style="height: 500px;"></div>
  </div>
</template>

<script setup>
import { onMounted, watch, computed } from 'vue';
import L from 'leaflet';
import store from '../store';

const props = defineProps({
  parkingToShow: { type: Object }
})

const position = computed(() => store.state.position);
const choosenPos = computed(() => store.state.choosenPos);
const parkings = computed(() => store.state.parking.parkings);


let map;
let currentMarker = null;
let chosenMarker = null;
let parkingMarker = null;
let carparkingMarker = null;

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


  const paddingIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/1788/1788637.png', // parking icon
    iconSize: [40, 40], // width, height
    iconAnchor: [20, 40], // where the icon "points"
    popupAnchor: [0, -35], // where popup opens relative to the icon
  });

  const currentParkingIcon = L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/421/421836.png', // parking icon
    iconSize: [60, 60], // width, height
    iconAnchor: [20, 40], // where the icon "points"
    popupAnchor: [0, -35], // where popup opens relative to the icon
  });



  // function to update car parkings available in parkings
  const updateCarParkings = () => {
    if (carparkingMarker) {
      map.removeLayer(carparkingMarker);
    }

    if (parkings.value.length > 0) {
      carparkingMarker = L.layerGroup(
        parkings.value.map(parking => {
          return L.marker([parseFloat(parking.lat), parseFloat(parking.long)], { icon: paddingIcon })
            .bindPopup(
              `<strong style="text-transform:uppercase;">${parking.name}</strong><br>
               <strong style="color:green;font-weight:bold;">
                 ${parking.slots_num - parking.booked} free
               </strong> parking spaces`
            )
            // .bindTooltip(`${parking.name}`, {
            //   permanent: true,
            //   direction: "top",
            //   offset: [5, -40],
            //   className: "leaflet-tooltip-own"
            // });
        })
      ).addTo(map);
    }
  };

  // Initial car parkings setup
  updateCarParkings();





  // Function to update given parking parking marker
  const updateParkingMarker = () => {
    if (props.parkingToShow?.lat && props.parkingToShow?.long) {
      const lat = parseFloat(props.parkingToShow.lat);
      const lng = parseFloat(props.parkingToShow.long);

      // Remove existing parking marker
      if (parkingMarker) {
        map.removeLayer(parkingMarker);
      }

      // Add new parking marker
      parkingMarker = L.marker([lat, lng], { icon: currentParkingIcon })
        .addTo(map)
        .bindPopup(`${props.parkingToShow.name}`)
        .bindTooltip(`${props.parkingToShow.name}`, {
          permanent: true,
          direction: "top",
          offset: [10, -40],
          className: "leaflet-tooltip-own"
        })
        // instead bind popup use something that shows the name with out clicking on it
        .openPopup();

      map.setView([lat, lng], 16);
    }
  };

  // Initial parking marker setup
  updateParkingMarker();




  // Watch for parkings changes
  watch(parkings, (newParkings) => {
    if (newParkings && newParkings.length > 0) {
      updateCarParkings();
    } else {
      if (carparkingMarker) {
        map.removeLayer(carparkingMarker);
        carparkingMarker = null;
      }
    }
  }, { immediate: true });  




  // Watch for parkingToShow changes
  watch(() => props.parkingToShow, (newParking) => {
    if (newParking?.lat && newParking?.long) {
      updateParkingMarker();
    }
  }, { deep: true });

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

    chosenMarker = L.marker([new_.lat, new_.long], { icon: customIcon })
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
