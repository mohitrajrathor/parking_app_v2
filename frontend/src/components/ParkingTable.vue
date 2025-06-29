<template>
  <div class="text-light bg-primary p-3 rounded-4 mb-5">
    <h2 class="text-center">Parkings</h2>
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
              <th>Fee</th>
              <th>Slots_num</th>
              <th>Booked</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <ParkingRow v-for="p in parkings" :key="p.id" :parking="p" />
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
  },
  components: { ParkingRow, Pagination },
  emits: ['update:page'],
  methods: {

    changePage(newPage) {
      this.$emit('update:page', newPage);
    }
  }
};
</script>
