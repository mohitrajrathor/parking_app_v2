<template>
  <div id="main">
    <Notification />

    <router-view></router-view>

  </div>
</template>
<script setup>
import store from './store';
import Notification from './components/Notification.vue';
import { onMounted } from 'vue';


onMounted(() => {
  store.dispatch("startTracking")
});


</script>

<style scoped></style>
