<template>
    <div class="p-3 border border-2 border-light rounded-4">
        <div class="bg-light rounded-4">
            <div class="p-4">
                <div>
                    <h3 class="text-center">Signup</h3>
                </div>

                <div v-if="errorTag" class="text-center text-danger" v-html="errorTag"></div>

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
                                    <div v-if="personalTabError.name" class="text-danger mt-1">{{ personalTabError.name
                                        }}
                                    </div>
                                </div>

                                <div class="form-floating mb-3">
                                    <input type="date" class="form-control" v-model="dob" id="dob"
                                        placeholder="mm-dd-yyyy" required />
                                    <label for="dob">Date of Birth</label>
                                    <div v-if="personalTabError.dob" class="text-danger mt-1">{{ personalTabError.dob }}
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Profession</label>
                                    <select class="form-select form-select-lg" name="profession" id="profession"
                                        v-model="profession" required>
                                        <option selected value="">Select one</option>
                                        <option value="employee">Employee (Manager or clerk)</option>
                                        <option value="business">Business</option>
                                        <option value="medical">Medical</option>
                                        <option value="driver">Driver (Taxi, Truck and Public Transport)</option>
                                        <option value="construction">Construction</option>
                                        <option value="self-employed">Self-Employed</option>
                                    </select>
                                    <div v-if="personalTabError.profession" class="text-danger mt-1">{{
                                        personalTabError.profession }}</div>
                                </div>

                                <div class="d-flex justify-content-end mx-4">
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
                                        <div v-if="contactTabError.email" class="text-danger mt-1">{{ contactTabError.email
                                            }}</div>
                                    </div>

                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" v-model="address" id="address" required
                                            placeholder="" />
                                        <label for="address">Address</label>
                                        <div v-if="contactTabError.address" class="text-danger mt-1">{{
                                            contactTabError.address }}</div>
                                    </div>

                                    <div class="row">
                                        <div class="col">
                                            <div class="form-floating mb-3">
                                                <input type="text" class="form-control" v-model="pincode" id="pincode"
                                                    required placeholder="" />
                                                <label for="pincode">Pincode</label>
                                                <div v-if="contactTabError.pincode" class="text-danger mt-1">{{
                                                    contactTabError.pincode }}</div>
                                            </div>
                                        </div>
                                        <div class="col">
                                            <div class="form-floating mb-3">
                                                <input type="tel" class="form-control" v-model="phone" id="phone"
                                                    placeholder="123-456-7890" pattern="[0-9]{10}" required />
                                                <label for="phone">Phone</label>
                                                <div v-if="contactTabError.phone" class="text-danger mt-1">{{
                                                    contactTabError.phone }}</div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="d-flex justify-content-between mx-4">
                                        <button @click="personalTab.click()" class="btn btn-outline-primary rounded-pill">
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
                                        <input type="password" class="form-control" v-model="password"
                                            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}"
                                            title="Must contain at least 8 characters, including uppercase, lowercase, number, and special character"
                                            id="password" placeholder="" required />
                                        <label for="password">Password</label>
                                        <div v-if="securityTabError.password" class="text-danger mt-1">{{
                                            securityTabError.password }}</div>
                                    </div>
                                    <div class="form-floating mb-3">
                                        <input @input="checkPassword" required type="password" class="form-control"
                                            v-model="confirmPassword" id="confirmPassword" placeholder="" />
                                        <label for="confirmPassword">Confirm Password</label>
                                        <small class="text-center w-100 d-block mt-2" :class="passHelpClass">{{
                                            passHelp }}</small>
                                        <div v-if="securityTabError.confirmPassword" class="text-danger mt-1">{{
                                            securityTabError.confirmPassword }}</div>
                                    </div>

                                    <div class="d-flex justify-content-center my-2">
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" v-model="termsAgreed"
                                                id="T&C" required />
                                            <label class="form-check-label" for="T&C"> Agree to Terms & Conditions
                                            </label>
                                            <div v-if="securityTabError.termsAgreed" class="text-danger mt-1">{{
                                                securityTabError.termsAgreed }}</div>
                                        </div>
                                    </div>

                                    <div class="d-flex justify-content-between mx-4">
                                        <button @click="contactTab.click()" class="btn btn-outline-primary rounded-pill">
                                            <i class="bi bi-arrow-left"></i> Back
                                        </button>
                                        <button type="submit" class="btn btn-primary rounded-pill" :disabled="isLoading">
                                            {{ isLoading ? 'Signing up...' : 'Signup' }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>

                <p class="mt-3 mx-4 text-center">
                    Already have an account? <router-link class="text-decoration-none text-dark fw-bold"
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

<script setup>
import { ref, computed, reactive, inject } from 'vue';
import { useStore } from 'vuex'; 
import { useRouter } from 'vue-router'; 


const store = useStore();
const router = useRouter();
const notify = inject("notify");

// Form data
const name = ref('');
const dob = ref('');
const profession = ref('');
const email = ref('');
const address = ref('');
const pincode = ref('');
const phone = ref('');
const password = ref('');
const confirmPassword = ref('');
const termsAgreed = ref(false);

// UI state
const isLoading = ref(false);
const errorTag = ref('');
const passHelp = ref('');

// Template refs
const personalTab = ref(null);
const contactTab = ref(null);
const securityTab = ref(null);

// Error messages for each tab, using reactive for multiple properties
const personalTabError = reactive({
    name: '',
    dob: '',
    profession: '',
});
const contactTabError = reactive({
    email: '',
    address: '',
    pincode: '',
    phone: '',
});
const securityTabError = reactive({
    password: '',
    confirmPassword: '',
    termsAgreed: '',
});


// Computed property for password help message styling
const passHelpClass = computed(() => {
    return passHelp.value.includes('matched') ? 'text-success' : 'text-danger';
});

// --- Methods ---

const validatePersonalTab = () => {
    let isValid = true;
    personalTabError.name = '';
    personalTabError.dob = '';
    personalTabError.profession = '';

    if (!name.value) {
        personalTabError.name = 'Name is required.';
        isValid = false;
    }
    if (!dob.value) {
        personalTabError.dob = 'Date of Birth is required.';
        isValid = false;
    }
    if (!profession.value) {
        personalTabError.profession = 'Profession is required.';
        isValid = false;
    }
    return isValid;
};

const validateContactTab = () => {
    let isValid = true;
    contactTabError.email = '';
    contactTabError.address = '';
    contactTabError.pincode = '';
    contactTabError.phone = '';

    if (!email.value) {
        contactTabError.email = 'Email is required.';
        isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        contactTabError.email = 'Invalid email format.';
        isValid = false;
    }

    if (!address.value) {
        contactTabError.address = 'Address is required.';
        isValid = false;
    }
    if (!pincode.value) {
        contactTabError.pincode = 'Pincode is required.';
        isValid = false;
    } else if (!/^\d{6}$/.test(pincode.value)) { // Basic 6-digit pincode validation
        contactTabError.pincode = 'Pincode must be 6 digits.';
        isValid = false;
    }

    if (!phone.value) {
        contactTabError.phone = 'Phone number is required.';
        isValid = false;
    } else if (!/^\d{10}$/.test(phone.value)) { // Basic 10-digit phone validation
        contactTabError.phone = 'Phone number must be 10 digits.';
        isValid = false;
    }
    return isValid;
};

const validateSecurityTab = () => {
    let isValid = true;
    securityTabError.password = '';
    securityTabError.confirmPassword = '';
    securityTabError.termsAgreed = '';

    if (!password.value) {
        securityTabError.password = 'Password is required.';
        isValid = false;
    } else if (!/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}$/.test(password.value)) {
        securityTabError.password = 'Password must be at least 8 characters, including uppercase, lowercase, number, and special character.';
        isValid = false;
    }

    if (!confirmPassword.value) {
        securityTabError.confirmPassword = 'Confirm password is required.';
        isValid = false;
    } else if (password.value !== confirmPassword.value) {
        securityTabError.confirmPassword = 'Passwords do not match.';
        isValid = false;
    }

    if (!termsAgreed.value) {
        securityTabError.termsAgreed = 'You must agree to the Terms & Conditions.';
        isValid = false;
    }
    return isValid;
};


const goToContactTab = () => {
    if (validatePersonalTab()) {
        contactTab.value.click();
        errorTag.value = ''; // Clear overall error
    } else {
        errorTag.value = `<span class="text-danger fw-bold">Please fill all required fields in the Personal tab.</span>`;
    }
};

const goToSecurityTab = () => {
    if (validateContactTab()) {
        securityTab.value.click();
        errorTag.value = ''; // Clear overall error
    } else {
        errorTag.value = `<span class="text-danger fw-bold">Please fill all required fields in the Contact tab.</span>`;
    }
};

const checkPassword = () => {
    if (password.value && confirmPassword.value && password.value === confirmPassword.value) {
        passHelp.value = 'Password matched!';
    } else if (password.value && confirmPassword.value && password.value !== confirmPassword.value) {
        passHelp.value = 'Password not matched!';
    } else {
        passHelp.value = '';
    }
};

const handleSubmit = async () => {
    // Validate all tabs before submitting
    const isPersonalValid = validatePersonalTab();
    const isContactValid = validateContactTab();
    const isSecurityValid = validateSecurityTab();

    if (!isPersonalValid) {
        personalTab.value.click();
        errorTag.value = `<span class="text-danger fw-bold">Please complete the Personal details.</span>`;
        return;
    }

    if (!isContactValid) {
        contactTab.value.click();
        errorTag.value = `<span class="text-danger fw-bold">Please complete the Contact details.</span>`;
        return;
    }

    if (!isSecurityValid) {
        securityTab.value.click();
        errorTag.value = `<span class="text-danger fw-bold">Please complete the Security details.</span>`;
        return;
    }

    isLoading.value = true;
    errorTag.value = '';

    try {
        const response = await fetch(`http://127.0.0.1:1234/api_v1/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.value,
                password: password.value,
                name: name.value,
                dob: dob.value,
                profession: profession.value,
                address: address.value,
                pincode: pincode.value,
                phone: phone.value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || "Failed to signup!");
        }

        const data = await response.json();

        // Dispatch login action to Vuex store
        store.dispatch("login", {
            role: data.role,
            token: data.token,
            refreshToken: data.refresh_token
        });

        // Redirect to user dashboard
        router.push({ name: "User" });

        // Notifications (assuming 'notify' function is available globally or imported)
        // If you don't have a global `notify` function, you'll need to implement one
        // or use a dedicated notification library.
        if (typeof notify !== 'undefined') {
            notify({
                message: 'You are successfully logged in as user!',
                title: 'Login Success',
                icon: 'https://cdn-icons-png.flaticon.com/512/190/190411.png',
                duration: 5000
            });

            notify({
                message: 'A confirmation email has been sent to your email. Please confirm to access all services. Thank you!',
                title: 'Confirm your email!',
                icon: 'https://cdn-icons-png.flaticon.com/512/4616/4616073.png',
                duration: 5000
            });
        } else {
            console.warn("Notification function 'notify' is not defined. Please implement it for user feedback.");
            alert('Signup successful! Please check your email for confirmation.');
        }

    } catch (e) {
        console.error("Signup error:", e.message);
        errorTag.value = `<span class="text-danger fw-bold">Error: ${e.message}</span>`;
        
        notify({
                message: 'unable to signup',
                title: 'Signup failed',
                icon: 'https://cdn-icons-png.flaticon.com/512/190/190411.png',
                duration: 5000
            });

    } finally {
        isLoading.value = false;
    }
};

</script>

<style scoped>
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