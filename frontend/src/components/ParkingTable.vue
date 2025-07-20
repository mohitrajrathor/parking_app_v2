<template>
  <div class="text-light bg-primary p-3 rounded-4 mb-5">
    <h2 class="text-center">Parkings</h2>
    <form class="row justify-content-center mb-3" @submit.prevent="onSearch">
      <div class="col-md-6 col-12">
        <div class="input-group">
          <input v-model="searchQuery" type="text" class="form-control rounded-start-4"
            placeholder="Search parking by name, address, or pincode...">
          <button class="btn btn-warning rounded-end-4 fw-bold" type="submit">
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
              <th>Name</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Phone</th>
              <th>Booking Fee</th>
              <th>hourly Fee</th>
              <th>Slots_num</th>
              <th>Booked</th>
              <th>Reviews</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoading">
              <td :colspan="11" class="text-center py-5">
                <div class="d-flex justify-content-center align-items-center" style="height: 100px;">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
              </td>
            </tr>
            <ParkingRow v-else v-for="p in parkings" :key="p.id" :parking="p" />
          </tbody>
        </table>
      </div>



      <div v-if="parkings.length">
        <Pagination :page="page" :pages="pages" @update:page="changePage" />

      </div>
      <div v-else>
        <h6 class="text-dark text-center">No parking available!</h6>

      </div>
    </div>
  </div>
</template>


<script>
import ParkingRow from './ParkingRow.vue';
import Pagination from './Pagination.vue';

export default {
  name: "ParkingTable",
  props: {
    parkings: Array,
    page: Number,
    pages: Number,
    isLoading: Boolean,
  },
  data() {
    return {
      searchQuery: "",
    }
   },
  components: { ParkingRow, Pagination },
  emits: ['update:page'],
  methods: {
    changePage(newPage) {
      this.$emit('update:page', newPage);
    },
    onSearch(query) {
      this.$emit("search:query", this.searchQuery);
    }
  }
};
</script>
