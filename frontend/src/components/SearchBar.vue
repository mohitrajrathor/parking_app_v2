<template>
    <div id="searchBar">
        <div class="d-flex align-items-center mb-3">
            <!-- Search Bar -->
            <form @submit.prevent="search" class="input-group border border-2 border-secondary flex-grow-1 me-2 rounded-pill">
                <span class="input-group-text bg-white border-end-0 rounded-start-pill">
                    <i class="bi bi-search text-muted"></i>
                </span>
                <input type="text" v-model="query" class="form-control border-start-0 rounded-end-pill"
                    placeholder="search Parkings, addresses..." aria-label="Search input">
            </form>

            <!-- Filter Button with Dropdown -->
            <div class="dropdown">
                <button class="btn btn-outline-secondary dropdown-toggle rounded-pill btn-filter" type="button"
                    id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-filter me-1"></i> Filter
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                    <li><a class="dropdown-item" href="#">Parkings</a></li>
                    <li><a class="dropdown-item" href="#">Fee</a></li>
                    <li><a class="dropdown-item" href="#">Occupied</a></li>
                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item" href="#">Other Option</a></li>
                </ul>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "SearchBar",
    data() {
        return {
            query: ""
        }
    },
    methods: {
        async search() {
            console.log("you search", this.query);
        }
    }
}
</script>
<style lang="">

</style>