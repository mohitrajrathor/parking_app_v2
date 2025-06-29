<template>
    <div id="parkingCard">
        <div class="card card-cover h-100 overflow-hidden text-bg-dark rounded-5 shadow-lg">
            <div class="d-flex flex-column h-100 p-5 pb-3 text-white text-shadow-1">
                <div class=" d-flex justify-content-between">
                    <div class="px-2 rounded-pill lime-green text-success">
                        ₹ {{ parking.fee }}
                    </div>
                    <div>
                        <router-link :to="`/parking?id=${parking.id}`">
                            <span class="badge text-bg-primary rounded-pill p-2">visit <i
                                    class="bi bi-box-arrow-up-right"></i></span>
                        </router-link>
                    </div>
                </div>
                <h3 class="pt-5 mt-5 mb-4 display-6 lh-1 fw-bold">{{ parking.name }}</h3>
                <ul class="d-flex list-unstyled mt-auto">
                    <li class="d-flex align-items-center me-3"> <svg class="bi me-2" width="1em" height="1em" role="img"
                            aria-label="Location">
                            <use xlink:href="#geo-fill"></use>
                        </svg> <small>{{ parking.address }}</small> </li>
                    <li class="d-flex align-items-center"> <svg class="bi me-2" width="1em" height="1em" role="img"
                            aria-label="Duration">

                        </svg><i class="bi bi-calendar-week"></i> <small>{{ parking.slots_num }}</small> </li>
                </ul>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "ParkingCard",
    props: {
        parking: {
            type: Object,
            required: true,
        },
    }
}
</script>
<style lang="">

</style>