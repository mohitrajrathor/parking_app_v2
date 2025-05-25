<template>
    <div class="p-3 border border-2 border-light rounded-4">
        <div class="bg-light rounded-4">
            <div class="p-4">

                <div>
                    <h3 class="text-center">
                        Signup
                    </h3>
                </div>

                <div v-html="errorTag" class="text-center">

                </div>

                <form @submit.prevent="handleSubmit">
                    <div class="responsive-box">
                        <div class="d-flex justify-content-center">
                            <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                                <li class="nav-item" role="presentation">
                                    <button ref="personalTab" class="nav-link active" id="pills-personal-tab"
                                        data-bs-toggle="pill" data-bs-target="#pills-personal" type="button" role="tab"
                                        aria-controls="pills-personal" aria-selected="true">Personal</button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button ref="contactTab" class="nav-link" id="pills-contact-tab"
                                        data-bs-toggle="pill" data-bs-target="#pills-contact" type="button" role="tab"
                                        aria-controls="pills-contact" aria-selected="false">Contact</button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button ref="securityTab" class="nav-link" id="pills-security-tab"
                                        data-bs-toggle="pill" data-bs-target="#pills-security" type="button" role="tab"
                                        aria-controls="pills-security" aria-selected="false">Security</button>
                                </li>
                            </ul>
                        </div>
                        <div class="tab-content" id="pills-tabContent">
                            <div class="tab-pane fade show active" id="pills-personal" role="tabpanel"
                                aria-labelledby="pills-personal-tab" tabindex="0">
                                <div class="my-3">
                                    <h5 class="text-center">Personal details</h5>
                                </div>
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control" v-model="name" id="name" placeholder=""
                                        required />
                                    <label for="name">Name</label>
                                </div>

                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control" v-model="age" id="age" placeholder=""
                                        required />
                                    <label for="age">Age</label>
                                </div>


                                <div v-html="personalTabError" class=" text-center">
                                </div>

                                <!-- this btn will lead to contact tab -->
                                <div class="d-flex justify-content-end mx-4">
                                    <!-- <button class="btn btn-primary rounded-pill" data-bs-target="#pills-contact" type="button">Next
                                        <i class="bi bi-arrow-right"></i></button> -->
                                    <button @click="goToContactTab" class="btn btn-outline-primary rounded-pill">
                                        Next <i class="bi bi-arrow-right"></i>
                                    </button>

                                </div>



                            </div>

                            <div class="tab-pane fade" id="pills-contact" role="tabpanel"
                                aria-labelledby="pills-contact-tab" tabindex="0">
                                <div id="contactForm">
                                    <div class="my-3">
                                        <h5 class="text-center">Contact details</h5>
                                    </div>
                                    <div class="form-floating mb-3">
                                        <input type="email" class="form-control" v-model="email" id="email"
                                            placeholder="" required />
                                        <label for="email">Email</label>
                                        <small id="helpId" class="form-text text-muted">Email will be used for
                                            login.</small>

                                    </div>


                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" v-model="address" id="address" required
                                            placeholder="" />
                                        <label for="address">Address</label>
                                    </div>

                                    <div class="row">
                                        <div class="col">
                                            <div class="form-floating mb-3">
                                                <input type="text" class="form-control" v-model="pincode" id="pincode"
                                                    required placeholder="" />
                                                <label for="pincode">Pincode</label>
                                            </div>
                                        </div>
                                        <div class="col">
                                            <div class="form-floating mb-3">
                                                <input type="tel" class="form-control" v-model="phone" id="phone"
                                                    placeholder="123-456-7890" pattern="[0-9]{10}" required />
                                                <label for="phone">phone</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div v-html="contactTabError" class=" text-center">
                                    </div>

                                    <!-- this btn will lead to contact tab -->
                                    <div class="d-flex justify-content-between mx-4">
                                        <!-- <button class="btn btn-primary rounded-pill" data-bs-target="#pills-contact" type="button">Next
                                        <i class="bi bi-arrow-right"></i></button> -->
                                        <button @click="this.$refs.personalTab.click()"
                                            class="btn btn-outline-primary rounded-pill">
                                            <i class="bi bi-arrow-left"></i> Back
                                        </button>
                                        <button @click="goToSecurityTab" class="btn btn-outline-primary rounded-pill">
                                            Next <i class="bi bi-arrow-right"></i>
                                        </button>

                                    </div>
                                </div>
                            </div>

                            <div class="tab-pane fade" id="pills-security" role="tabpanel"
                                aria-labelledby="pills-security-tab" tabindex="0">

                                <div id="securityForm">
                                    <div class="my-3">
                                        <h5 class="text-center">Security details</h5>
                                    </div>
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" v-model="password"
                                            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}"
                                            title="Must contain at least 8 characters, including uppercase, lowercase, number, and special character"
                                            id="password" placeholder="" required />
                                        <label for="password">Password</label>
                                    </div>
                                    <div class="form-floating mb-3">
                                        <input @input="checkPassword" required type="password" class="form-control"
                                            v-model="confirmPassword" id="confirmPassword" placeholder="" />
                                        <label for="confirmPassword">Confirm Password</label>
                                        <small class="text-center w-100 d-block mt-2" v-html="passHelp"></small>
                                    </div>

                                    <div class=" d-flex justify-content-center my-2">
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" value="" id="T&C" required />
                                            <label class="form-check-label" for="T&C"> Agree to Terms & Conditions
                                            </label>
                                        </div>
                                    </div>


                                    <div v-html="securityTabError" class=" text-center">
                                    </div>

                                    <!-- this btn will lead to contact tab -->
                                    <div class="d-flex justify-content-between mx-4">
                                        <!-- <button class="btn btn-primary rounded-pill" data-bs-target="#pills-contact" type="button">Next
                                        <i class="bi bi-arrow-right"></i></button> -->
                                        <button @click="this.$refs.contactTab.click()"
                                            class="btn btn-outline-primary rounded-pill">
                                            <i class="bi bi-arrow-left"></i> Back
                                        </button>
                                        <button type="submit" class="btn btn-primary rounded-pill">
                                            Signup
                                        </button>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>

                <p class="mt-3 mx-4 text-center">
                    Already Signup <router-link class=" text-decoration-none text-dark fw-bold"
                        to="/auth/login">Login</router-link> here.
                </p>

            </div>

            <div class="d-flex justify-content-center">
                <div class="bg-primary rounded-top-pill" style="height: 10px; width: 100px;">
                </div>
            </div>

        </div>
    </div>
</template>
<script>
export default {
    name: "Signup",
    data() {
        return {
            name: "",
            age: "",
            email: "",
            address: "",
            pincode: "",
            phone: "",
            password: "",
            confirmPassword: "",
            passHelp: "",
            errorTag: "",
            personalTabError: "",
            contactTabError: "",
            securityTabError: "",

        }
    },
    methods: {
        goToContactTab() {
            if (this.name && this.age) {
                this.$refs.contactTab.click()
            } else {
                this.personalTabError = `<span class="text-danger fw-bold">Fill all the required fields!</span>`
            }
        },

        goToSecurityTab() {
            if (this.email && this.address && this.pincode && this.phone) {
                this.$refs.securityTab.click()
            } else {
                this.contactTabError = `<span class="text-danger fw-bold">Fill all the required fields!</span>`
            }
        },

        checkPassword() {
            if (this.password !== this.confirmPassword) {
                this.passHelp = `<span class="text-danger">Password not matched!</span>`;
            } else if (this.password === this.confirmPassword) {
                this.passHelp = `<span class="text-success">Password matched!</span>`;
            } else {
                this.passHelp = '';
            }
        },

        async handleSubmit() {
            console.log("form submitted!")
            console.log(this.password);
            alert("form submitted");
        }
    }
}
</script>
<style>
.responsive-box {
    min-width: 100%;
    min-height: 320px;
}

@media (min-width: 768px) {
    .responsive-box {
        min-width: 500px;
        min-height: 400px;
    }
}
</style>