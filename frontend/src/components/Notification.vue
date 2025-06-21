<template>
  <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 9999">
    <div
      v-for="(toast, index) in toasts"
      :key="index"
      class="toast show"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div class="toast-header">
        <img
          v-if="toast.icon"
          :src="toast.icon"
          class="rounded me-2"
          alt="icon"
          width="20"
          height="20"
        />
        <strong class="me-auto">{{ toast.title || 'Notification' }}</strong>
        <small class="text-muted">Just now</small>
        <button
          type="button"
          class="btn-close"
          @click="removeToast(index)"
          aria-label="Close"
        ></button>
      </div>
      <div class="toast-body">
        {{ toast.message }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Notification',
  data() {
    return {
      toasts: []
    }
  },
  created() {
    this.$.appContext.provides.notify = this.notify
  },

  computed: {
    ...mapGetters['isAuthenticated']
  },

  watch: {
    isAuthenticated(newAuth, prevAuth) {
      if (!newAuth) {
        this.notify({message: 'Logging out, please login again!', title: "Logout", icon: null, duration: 5000});
      }
    }
  },

  methods: {
    notify({ message, title = 'Notification', icon = null, duration = 3000 }) {
      const toast = { message, title, icon }
      this.toasts.push(toast)

      setTimeout(() => {
        const index = this.toasts.indexOf(toast)
        if (index !== -1) this.toasts.splice(index, 1)
      }, duration)
    },
    removeToast(index) {
      this.toasts.splice(index, 1)
    }
  }
}
</script>
