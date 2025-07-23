<template>
  <div class="min-vh-100 d-flex flex-column bg-white">
    <NavBar />
    <div class="container flex-grow-1 d-flex align-items-center justify-content-center py-5">
      <div class="col-12 col-md-8 col-lg-6">
        <div class="card shadow-lg border-0 rounded-4 p-4">
          <h2 class="text-primary fw-bold mb-3 text-center">
            <i class="bi bi-envelope-at me-2"></i>Contact Us
          </h2>
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input v-model="form.name" type="text" class="form-control rounded-pill" id="name" placeholder="Your Name" required />
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input v-model="form.email" type="email" class="form-control rounded-pill" id="email" placeholder="you@example.com" required />
            </div>
            <div class="mb-3">
              <label for="message" class="form-label">Message</label>
              <textarea v-model="form.message" class="form-control rounded-4" id="message" rows="4" placeholder="Type your message here..." required></textarea>
            </div>
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary rounded-pill fw-bold">
                <i class="bi bi-send me-1"></i>Send Message
              </button>
            </div>
            <div v-if="submitted" class="alert alert-success mt-3 rounded-4 text-center" role="alert">
              Thank you for contacting us! We'll get back to you soon.
            </div>
          </form>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';

export default {
  name: 'ContactPage',
  components: {
    NavBar,
    Footer
  },
  data() {
    return {
      form: {
        name: '',
        email: '',
        message: ''
      },
      submitted: false
    };
  },
  methods: {
    submitForm() {
      // Simulate form submission
      this.submitted = true;
      setTimeout(() => {
        this.submitted = false;
        this.form = { name: '', email: '', message: '' };
      }, 3000);
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 1.5rem !important;
}
</style>
