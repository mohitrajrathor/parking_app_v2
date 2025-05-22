<template>
    <div id="Perks">
        <div class="p-2 row">
            <div class="col-md-4 p-2">
                <div class="m-1 p-4 rounded-4 lime-green">
                    <div class="d-flex justify-content-between align-items-center">
                        <h6><span class="me-3"><i
                                    class=" border border-2 border-black rounded-circle px-2 py-1 bi bi-buildings-fill"></i></span>
                            Parking Spots</h6>
                        <div>
                            <span><i class="bi bi-arrow-down-circle"></i></span>
                        </div>
                    </div>
                    <h4 class="my-4 fw-semibold">Total Parking Spots</h4>
                    <h2 class=" fw-bold">170K</h2>
                    <small class="text-muted fw-semibold">Nearby (in 50km<sup>2</sup> range)</small>
                    <h4 class="fw-bold">2141</h4>
                </div>
            </div>

            <div class="col-md-4 p-2">
                <div class="m-1 p-4 rounded-4 tomato-red bg-gradient">
                    <div class="d-flex justify-content-between">
                        <h5><span class="me-3"><i
                                    class=" border border-2 border-black rounded-circle px-2 py-1 bi bi-car-front-fill"></i></span>
                            <span class=" text-light">Bookings</span>
                        </h5>
                        <div>
                            <span><i class="bi bi-arrow-down-circle"></i></span>
                        </div>
                    </div>
                    <h4 class="my-4 fw-semibold">Today's Bookings</h4>
                    <h2 class=" fw-bold">140K</h2>
                    <small class="text-muted fw-semibold">Nearby (in 50km<sup>2</sup> range)</small>
                    <h4 class="fw-bold">1758</h4>
                </div>
            </div>

            <div class="col-md-4 p-2">
                <div class="m-1 p-4 rounded-4 text-light bg-primary bg-gradient">
                    <div class="d-flex justify-content-between">
                        <h5><span class="me-3"><i
                                    class=" border border-2 border-light rounded-circle px-2 py-1 bi bi-coin"></i></span>
                            Revenue</h5>
                        <div>
                            <span><i class="bi bi-arrow-down-circle"></i></span>
                        </div>
                    </div>
                    <h4 class="my-4 fw-semibold">Total Revenue</h4>
                    <h2 class=" fw-bold">28M</h2>
                    <small class="text-light fw-semibold">Nearby (in 50km<sup>2</sup> range)</small>
                    <h4 class="fw-bold">351K</h4>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "Perks"
}
</script>
<style scoped></style>