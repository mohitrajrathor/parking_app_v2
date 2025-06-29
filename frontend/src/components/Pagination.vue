<template>
  <nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
      <!-- Previous -->
      <li class="page-item" :class="{ disabled: page === 1 }">
        <button class="page-link" @click="goToPage(page - 1)" :disabled="page === 1">
          Previous
        </button>
      </li>

      <!-- Page numbers -->
      <li
        v-for="n in pages"
        :key="n"
        class="page-item"
        :class="{ active: n === page }"
      >
        <button class="page-link" @click="goToPage(n)">{{ n }}</button>
      </li>

      <!-- Next -->
      <li class="page-item" :class="{ disabled: page === pages }">
        <button class="page-link" @click="goToPage(page + 1)" :disabled="page === pages">
          Next
        </button>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  props: {
    page: {
      type: Number,
      required: true,
    },
    pages: {
      type: Number,
      required: true,
    },
  },
  methods: {
    goToPage(newPage) {
      if (newPage >= 1 && newPage <= this.pages && newPage !== this.page) {
        this.$emit('update:page', newPage);
      }
    },
  },
};
</script>

<style scoped>
/* No custom styling needed; using Bootstrap only */
</style>
