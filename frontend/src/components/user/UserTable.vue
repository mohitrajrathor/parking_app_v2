<template>
  <div class="text-light bg-primary p-3 rounded-4 mb-5">
    <div>
      <h2 class="text-center mb-3">Users</h2>
      <form class="row justify-content-center mb-3" @submit.prevent="onSearch">
        <div class="col-md-6 col-12">
          <div class="input-group">
            <input v-model="searchQuery" type="text" class="form-control rounded-start-4" placeholder="Search users by name, email, or profession...">
            <button class="btn btn-warning rounded-end-4 fw-bold" type="submit">
              <i class="bi bi-search"></i> Search
            </button>
          </div>
        </div>
      </form>
    </div>

    <div class="bg-light rounded-3 p-1">
      <div class="table-responsive mb-3">
        <table class="table rounded-3 mb-0">
          <thead>
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Email</th>
              <th>Profession</th>
              <th>DOB</th>
              <th>Joined</th>
              <th>Bookings</th>
              <th>Reviews</th>
              <th>Email Confirmed</th>
              <th>Active Bookings</th>
              <th>Total Bookings</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoading">
              <td :colspan="15" class="text-center py-5">
                <div class="d-flex justify-content-center align-items-center" style="height: 100px;">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
              </td>
            </tr>
            <UserRow v-for="u in users" :key="u.id" :user="u" v-else />
          </tbody>
        </table>
      </div>
      <div v-if="users.length">
        <Pagination :page="page" :pages="pages" @update:page="changePage" />
      </div>
      <div v-else>
        <h6 class="text-dark text-center">No users available!</h6>
      </div>
    </div>
  </div>
</template>

<script>

import UserRow from './UserRow.vue';
import Pagination from '../Pagination.vue';

export default {
  name: "UserTable",
  props: {
    users: Array,
    page: Number,
    pages: Number,
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchQuery: ''
    };
  },
  components: { UserRow, Pagination },
  emits: ['update:page', 'search:query'],
  methods: {
    changePage(newPage) {
      this.$emit('update:page', newPage);
    },
    onSearch() {
      this.$emit('search:query', this.searchQuery.trim());
    }
  }
};
</script>
