<script>
export default {
  inject: ['notify'],
  methods: {
    showCustomToast() {
      this.notify({
        message: 'Data saved successfully!',
        title: 'Success',
        icon: 'https://cdn-icons-png.flaticon.com/512/190/190411.png',
        duration: 5000
      })
    }
  }
}
</script>

<template>
  <button class="btn btn-primary" @click="showCustomToast">Show Toast</button>
</template>
