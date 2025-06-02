<template>
    <div id="userComplaint">
        <div class=" container">
            <div class="row row-gap-3">
                <div class="col-lg-8">
                    <div class=" bg-warning-subtle p-4 rounded-5">
                        <h3 class="mb-4">
                            Support
                        </h3>
                        <div class="row row-gap-2 column-gap-2">
                            <div class="col">
                                <div class="rounded-5 bg-light border border-2 border-warning">
                                    <div class="m-4">
                                        <div class="fs-1">

                                        </div>
                                        <h5>Request Yearly Report</h5>
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <div class="rounded-5 bg-light border border-2 border-warning">
                                    <div class="m-4">
                                        <div class="fs-1">

                                        </div>
                                        <h5>Request Monthly Report</h5>
                                    </div>
                                </div>
                            </div>

                            <div class="col">
                                <div class="rounded-5 bg-light border border-2 border-warning">
                                    <div class="m-4">
                                        <div class="fs-1">

                                        </div>
                                        <h3>Contact</h3>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class=" bg-primary text-light p-3 rounded-5">
                        <h3 class="text-center">
                            Register Complaints
                        </h3>

                        <form @submit.prevent="" class="p-2">
                            <div class="form-floating mb-3">
                                <input type="text" class="form-control rounded-4" name="parkingId" id="parkingId"
                                    placeholder="" />
                                <label for="parkingId">Parking Id</label>
                            </div>

                            <div class="form-floating mb-3">
                                <input type="text" class="form-control  rounded-4" name="issue" id="issue"
                                    placeholder="" />
                                <label for="issue">Issue Title</label>
                            </div>

                            <div class="form-floating mb-3">
                                <input type="text" class="form-control rounded-4" name="description" id="description"
                                    placeholder="" />
                                <label for="description">Description</label>
                            </div>

                            <div class="d-flex justify-content-center mt-3">
                                <button type="submit" class="btn btn-warning fw-bold w-100 rounded-pill">
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "UserComplaints",
}
</script>
<style lang="">

</style>