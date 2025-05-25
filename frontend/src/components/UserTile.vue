<template>
    <div id="userTile" class="m-2">
        <div class="p-3 bg-light text-black rounded-3">
            <div class=" d-flex justify-content-between align-items-center">
            <small class="rounded-pill bg-success badge">{{ user.status ? "Active" : "Blocked" }}</small>
            <small class="rounded-pill bg-success badge">{{ user.joinTime }}</small>
            </div>
            
            <div class=" d-flex justify-content-between align-items-center">
                <p class="m-0 fw-medium">{{ user.name }}</p>
                <p class="m-0 fw-medium">{{ user.email }}</p>
                <p class="m-0 fw-medium">{{ user.phone }}</p>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "UserTile",
    props: {
        user: {
            type: Object,
            required: true
        }
    }
}
</script>
<style scoped>
    
</style>