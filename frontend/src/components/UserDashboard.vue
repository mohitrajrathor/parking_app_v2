<template>
    <div id="userDashboard">
        <div class=" container">
            <div class="my-3 text-light p-md-5 p-3 bg-primary rounded-5">
                <p class="mb-2 fs-5 fw-bold">Choose parking lots</p>
                <div class=" d-flex justify-content-start align-items-center">
                    <button class="mx-2 fw-bold btn btn-sm text-dark lime-green rounded-pill">
                        Nearby
                    </button>
                    <button class="fw-bold btn btn-sm btn-outline-light rounded-pill">
                        Popular
                    </button>
                </div>
                <div class=" mt-3 row">
                    <div class="col-md-4">
                        <div class=" mt-3 rounded-5">
                            <LeafletMap />
                        </div>
                    </div>

                    <div class="col-md-8 row row-gap-2 ">
                        <div class="mt-3">
                            <div class=" text-dark rounded-5 bg-success-subtle p-4">
                                <p class="fs-5 fw-bold">
                                    <span class="me-4"><i class="bi bi-pin-map-fill"></i></span>
                                    Parking Slots
                                </p>
                                <div style="height: 150px;" class=" overflow-x-auto">
                                    <table class="table table-success overflow-auto">
                                        <thead>
                                            <tr>
                                                <th scope="col">ID</th>
                                                <th scope="col">Parking</th>
                                                <th scope="col">Available Slots</th>
                                                <th scope="col">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody class=" overflow-auto">
                                            <tr>
                                                <th scope="row">1</th>
                                                <td class="">
                                                    XYZ
                                                </td>
                                                <td>4</td>
                                                <td>
                                                    <button class="btn btn-dark rounded-pill">
                                                        Book
                                                    </button>
                                                </td>

                                            </tr>
                                            <tr>
                                                <th scope="row">2</th>
                                                <td>ABC</td>
                                                <td>8</td>
                                                <td>
                                                    <button class="btn btn-dark rounded-pill">
                                                        Book
                                                    </button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>

                        <div>
                            <div class=" text-light rounded-5 bg-danger overflow-auto">
                                <div style="height: 150px;" class="my-2 p-4">
                                    <div class="mx-3 d-flex justify-content-between align-items-center">
                                        <div class="fw-bold fs-5">
                                            <span class=""><i class="bi bi-bookmark-check"></i></span>
                                            Booked Slots
                                        </div>
                                        <div class="fs-5">
                                            4
                                        </div>
                                    </div>
                                    <div class="mx-3 mt-3 d-flex justify-content-between align-items-center">
                                        <div class="fw-bold fs-5">
                                            <span class=""><i class="bi bi-bookmark-check"></i></span>
                                            Booked Slots
                                        </div>
                                        <div class="fs-5">
                                            4
                                        </div>
                                    </div>
                                </div>
                                <div class="text-dark bg-light p-4">
                                    <div class=" d-flex justify-content-around align-items-center">
                                        <h4>Manage Booking</h4>
                                        <button class="px-4 btn btn-primary rounded-pill">
                                            >
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            <div id="parkings">
                <ParkingCardContainer />
            </div>

            <div class="row row-gap-2 my-3">
                <div class="col-md-6">
                    <div class=" bg-light p-4 rounded-4">
                        <h3>
                            Copyright &copy; 2025
                        </h3>
                        <p>All right reserved</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class=" bg-light p-4 rounded-4">
                        <h3>
                            <i class="bi bi-person-check"></i> Terms & Conditions
                        </h3>
                        <p><i class="bi bi-shield-exclamation"></i> Privacy Policy</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapActions } from "vuex";
import LeafletMap from './LeafletMap.vue';
import ParkingCardContainer from './user/ParkingCardContainer.vue';

export default {
    name: "UserDashboard",
    components: {
        LeafletMap, 
        ParkingCardContainer
    }, 
    methods: {
        ...mapActions('user', ['fetchCurrentUser']),
    },
    created() {
        this.fetchCurrentUser();
    }
}
</script>
<style scoped></style>