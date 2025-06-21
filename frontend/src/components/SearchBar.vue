<template>
    <div id="searchBar">
        <div class="">
            <form @submit.prevent="console.log(query)">
                <div class="mb-3">
                    <label for="search" class="form-label">Search</label>
                    <input type="text" class="form-control" name="query" id="query" v-model="query"
                        aria-describedby="helpId" placeholder="" />

                    <button
                        type="submit"
                        class="btn btn-primary"
                    >
                        Submit
                    </button>
                    
                </div>
            </form>

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
    }
}
</script>
<style lang="">

</style>