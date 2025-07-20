<template>
  <div class="text-light bg-warning p-3 rounded-4 mb-5">
    <h2 class="text-center">Reservations</h2>
    <form class="row justify-content-center mb-3" @submit.prevent="onSearch">
      <div class="col-md-6 col-12">
        <div class="input-group">
          <input v-model="searchQuery" type="text" class="form-control rounded-start-4"
            placeholder="Search Reservation by parking name">
          <button class="btn btn-primary rounded-end-4 fw-bold" type="submit">
            <i class="bi bi-search"></i> Search
          </button>
        </div>
      </div>
    </form>
    <div class="bg-light rounded-3 p-1">
      <div class="table-responsive mb-3">
        <table class="table rounded-3 mb-0">
          <thead>
            <tr>
              <th>#</th>
              <th>Parking</th>
              <th>Slot</th>
              <th>Start Time</th>
              <th>Leave Time</th>
              <th>Hours Used</th>
              <th>Status</th>
              <th>Charges</th>
              <th>Review</th>
              <th>User</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoading">
              <td :colspan="11" class="text-center py-5">
                <div class="d-flex justify-content-center align-items-center" style="height: 100px;">
                  <div class="spinner-border text-warning" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
              </td>
            </tr>
            <ReservationRow v-else v-for="r in reservations" :key="r.id" :reservation="r" />
          </tbody>
        </table>
      </div>
      <div v-if="reservations.length">
        <Pagination :page="page" :pages="pages" @update:page="changePage" />
      </div>
      <div v-else>
        <h6 class="text-dark text-center">No reservations available!</h6>
      </div>
    </div>
  </div>
</template>

<script>
import ReservationRow from './ReservationRow.vue';
import Pagination from '../Pagination.vue';

export default {
  name: "ReservationTable",
  props: {
    reservations: Array,
    page: Number,
    pages: Number,
    isLoading: Boolean,
  },
  data() {
    return {
      searchQuery: "",
    }
  },
  components: { ReservationRow, Pagination },
  emits: ['update:page'],
  methods: {
    changePage(newPage) {
      this.$emit('update:page', newPage);
    },
    onSearch() {
      this.$emit('search:query', this.searchQuery);
    }
  }
};
</script>
