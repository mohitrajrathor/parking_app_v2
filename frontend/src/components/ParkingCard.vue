<template>
    <div id="ParkingCard" class="bg-light rounded-4 text-dark border-bottom border-2 p-2 pb-2"> 
        <div class="mx-1 d-flex justify-content-end align-items-center">
            <div class=" rounded-pill badge bg-success text-light">
                Available
            </div>
            <div class="mx-1 rounded-pill badge bg-primary text-light">
                Pick Ready
            </div>
        </div>

        <h4 class="m-2 fw-semibold">
            XYZ Parking
        </h4>
        <p class=" text-end">
            Cost <span class="text-success fw-bold"><i class="bi bi-currency-rupee"></i>400</span>
        </p>
        <button class="btn btn-outline-dark rounded-pill w-100">Book Slot <i class="bi bi-caret-right-fill"></i></button>
    </div>
</template>
<script>
export default {
    name: "ParkingCard"
}
</script>
<style lang="">
    
</style>