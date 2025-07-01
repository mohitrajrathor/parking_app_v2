<template>
  <div class="card mb-3 rounded-4 border-0 parking-card-responsive">
    <div class="card-body">
      <h5 class="card-title mb-3 text-capitalize">{{ name }}</h5>
      <div class="mb-2 d-flex flex-column flex-sm-row gap-2">
        <span class="p-2 bg-primary-subtle rounded-2 text-primary fw-bold me-2">Booking Fee: ₹{{ bookingFee }}</span>
        <span class="p-2 bg-success-subtle rounded-2 text-success fw-bold me-2">Hourly Fee: ₹{{ hourlyFee }}</span>
      </div>
      <p class="mb-3 text-success">Available Slots: <strong>{{ availableSlots }}</strong></p>
      <div class="d-flex justify-content-end">
        <button class="btn btn-primary rounded-pill" @click="$emit('view', id)">View Parking</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ParkingCard",
  props: {
    id: {
      type: [String, Number],
      required: true
    },
    name: {
      type: String,
      required: true
    },
    bookingFee: {
      type: [String, Number],
      required: true
    },
    hourlyFee: {
      type: [String, Number],
      required: true
    },
    availableSlots: {
      type: [String, Number],
      required: true
    }
  }
}
</script>

<style scoped>
.parking-card-responsive {
  max-width: 100%;
  width: 100%;
}
@media (min-width: 576px) {
  .parking-card-responsive {
    max-width: 350px;
  }
}
.card-body {
  padding: 1.25rem;
}
@media (max-width: 575.98px) {
  .card-body {
    padding: 0.75rem;
  }
  .card-title {
    font-size: 1.1rem;
  }
}
</style>