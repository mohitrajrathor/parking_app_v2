<template>
    <footer class="d-flex justify-content-center">
        <div
            id="footer"
            class="bg-black bg-gradient text-light m-3 pb-3 container rounded-4"
        >
            <div class="container pt-4">
                <div class="row g-3 pt-3">
                    <div class="col-sm-12">
                        <div class="row ms-5 g-3">
                            <!-- Quick Links -->
                            <div class="col-lg-4 col-md-6 col-sm-12">
                                <h5>Quick Links</h5>
                                <ul class="list-unstyled">
                                    <li>
                                        <a
                                            href="#services"
                                            class="text-light text-decoration-none"
                                            >Our Services</a
                                        >
                                    </li>
                                    <li>
                                        <a
                                            href="#contact"
                                            class="text-light text-decoration-none"
                                            >Contact Us</a
                                        >
                                    </li>
                                    <li>
                                        <a
                                            href="#faq"
                                            class="text-light text-decoration-none"
                                            >FAQs</a
                                        >
                                    </li>
                                    <li>
                                        <a
                                            href="#terms"
                                            class="text-light text-decoration-none"
                                            >Terms & Conditions</a
                                        >
                                    </li>
                                    <li>
                                        <a
                                            href="#privacy"
                                            class="text-light text-decoration-none"
                                            >Privacy Policy</a
                                        >
                                    </li>
                                </ul>
                            </div>

                            <!-- Contact Information -->
                            <div class="col-lg-4 col-md-6 col-sm-12">
                                <h5>Contact Us</h5>
                                <p>
                                    <i class="bi bi-envelope-fill"></i>
                                    support@parkly.com<br />
                                    <i class="bi bi-phone-fill"></i> +91 (123)
                                    456-7890<br />
                                    <i class="bi bi-geo-alt-fill"></i> 123
                                    Service Street, HomeCity, HC PIN-123456
                                </p>
                                <div class="fs-3">
                                    <a
                                        href="https://facebook.com"
                                        class="text-light me-3"
                                        ><i class="bi bi-facebook"></i
                                    ></a>
                                    <a
                                        href="https://X.com"
                                        class="text-light me-3"
                                        ><i class="bi bi-twitter"></i
                                    ></a>
                                    <a
                                        href="https://instagram.com"
                                        class="text-light"
                                        ><i class="bi bi-instagram"></i
                                    ></a>
                                </div>
                            </div>

                            <!-- Admin Information -->

                            <div class="col-lg-4 col-md-6">
                                <h5>Admin Section</h5>
                                <router-link
                                    class="text-decoration-none text-light"
                                    to="/auth/admin-login"
                                    ><i class="bi bi-shield-check"></i> Admin
                                    Panel</router-link
                                >
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row justfiy-content-center align-items-center">
                <div class="p-3">
                    <p class="display-1 text-center">
                        <router-link
                            to="/"
                            class="text-decoration-none brand-font text-light"
                            >parkly</router-link
                        >
                    </p>
                    <p class="text-center">Quick, Relieble & Hassele free</p>
                </div>
            </div>
            <div class="container text-light">
                <hr />
            </div>
            <p class="text-center text-light mb-0">
                &copy; 2025 parkly.com | All rights reserved.
            </p>
        </div>
    </footer>
</template>

<script>
export default {
    name: "FooterView",
};
</script>

<style scoped></style>