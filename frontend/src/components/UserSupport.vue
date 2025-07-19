<template>
    <div id="userComplaint">
        <div class=" container">
            <div class="row row-gap-3">
                <div class="col-lg-8">
                    <div class=" bg-warning-subtle p-4 rounded-5">
                        <h3 class="mb-4">
                            Support
                        </h3>
                        <div class="row g-3">
                            <div class="col-md-4 col-12">
                                <button type="button" @click="requestData('send_all_data_report')" class="btn btn-outline-warning w-100 py-4 rounded-5 shadow-sm d-flex flex-column align-items-center justify-content-center gap-2 fw-bold">
                                    <span class="fs-1"><i class="bi bi-calendar3"></i></span>
                                    Request All Data
                                </button>
                            </div>
                            <div class="col-md-4 col-12">
                                <button type="button" @click="requestData('send_monthly_report')" class="btn btn-warning w-100 py-4 rounded-5 shadow-sm d-flex flex-column align-items-center justify-content-center gap-2 fw-bold text-dark">
                                    <span class="fs-1"><i class="bi bi-calendar2-month"></i></span>
                                    Request Monthly Report
                                </button>
                            </div>
                            <div class="col-md-4 col-12">
                                <button type="button" class="btn btn-outline-primary w-100 py-4 rounded-5 shadow-sm d-flex flex-column align-items-center justify-content-center gap-2 fw-bold">
                                    <span class="fs-1"><i class="bi bi-headset"></i></span>
                                    Contact
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="card border-0 shadow-sm rounded-5 bg-white">
                        <div class="card-body p-4">
                            <div class="d-flex flex-column align-items-center mb-3">
                                <span class="fs-1 text-primary mb-2"><i class="bi bi-chat-dots"></i></span>
                                <h4 class="fw-bold text-primary text-center mb-0">Register Complaints</h4>
                            </div>
                            <form @submit.prevent="" class="">
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control rounded-4" name="parkingId" id="parkingId"
                                        placeholder="" />
                                    <label for="parkingId">Parking Id</label>
                                </div>
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control rounded-4" name="issue" id="issue"
                                        placeholder="" />
                                    <label for="issue">Issue Title</label>
                                </div>
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control rounded-4" name="description" id="description"
                                        placeholder="" />
                                    <label for="description">Description</label>
                                </div>
                                <div class="d-flex justify-content-center mt-3">
                                    <button type="submit" class="btn btn-warning fw-bold w-100 rounded-pill py-2">
                                        <i class="bi bi-send me-2"></i>Submit
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import api from '../api';


export default {
    name: "UserComplaints",
    inject: ['notify'],
    methods: {
        async requestData(report) {
            try {
                const response = await api.get(`/api_v1/tasks/${report}`, {
                    withCredentials: true
                })

                const data = await response.data;
                this.notify({
                    message: data?.message || "You will recieve report on mail shortly."
                })
            } 
            catch (err) {
                console.error(err);
                const data = await err.response.data;
                this.notify({
                    message: data?.message || "Oops! Cannot process your request now."
                })
            }
            
            
        }
    }
}
</script>
<style lang="">

</style>