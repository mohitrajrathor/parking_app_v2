<template>
    <div id="feedbackBox" class="p-2">
        <div class="row px-2">
            <div class="col-9 rounded-top-4 bg-primary p-2 d-flex justify-content-center align-items-center">
                <div>
                    <p class="text-light m-0 text-center">
                        {{ shown.review }}
                    </p>
                    <div class="fw-bold text-light text-center">
                        <span v-html="shown.rateStars" class="text-warning">
                        </span>
                        {{ shown.rating }}
                    </div>
                </div>
            </div>
            <div class="col-3 rounded-top-4 light-gray p-2">
                <div class="text-center">
                    <img :src="shown.imgUrl" width="70" class=" border-secondary border-2 img-thumbnail rounded-circle p-0">
                </div>
            </div>
        </div>

        <div class="row px-2">
            <div class="col-6 rounded-bottom-4 bg-primary p-2 d-flex justify-content-center align-items-center">
                <button class="btn btn-outline-light btn-sm">
                    <img :src="shown.imgUrl" width="20" class="img-thumbnail rounded-circle p-0">
                    {{ shown.name }}
                </button>
            </div>
            <div class="col-6 p-2 rounded-bottom-4 light-gray">
                <div>
                    <button v-for="(uData, index) in restUser" :key="index" @click="changeShownUser(uData.name)"
                        class="btn btn-sm btn-outline-primary m-1">
                        {{ uData.name }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "FeedbackBox",
    data() {
        return {

            userData: [
                {
                    name: "Aarav",
                    imgUrl: "https://preview.keenthemes.com/metronic-v4/theme/assets/pages/media/profile/profile_user.jpg",
                    rating: 4.5,
                    review: `"This service really helped me stay organized. Highly recommended!"`
                },
                {
                    name: "Ishita",
                    imgUrl: "https://eliteadmin.themedesigner.in/demos/bt4/university/dist/images/users/11.jpg",
                    rating: 5,
                    review: `"Amazing experience! Everything went smoothly and efficiently."`
                },
                {
                    name: "Rohan",
                    imgUrl: "https://maintainne.com.au/wp-content/uploads/2021/03/mike.jpg",
                    rating: 4,
                    review: `"Good support and helpful staff. Minor issues but resolved quickly."`
                },
                {
                    name: "Meera",
                    imgUrl: "https://images.squarespace-cdn.com/content/v1/5a0625187131a531e03d7cf0/1642807342163-3X0Q321U13SU34JGHWHH/Sam+Breitmeyer.jpg?format=1000w",
                    rating: 4.8,
                    review: `"Loved the ease of use. Will definitely use this again."`
                },
                {
                    name: "Kabir",
                    imgUrl: "https://framerusercontent.com/images/jNIAyB2sqvuG8yHjl0evMBAio7M.png",
                    rating: 5,
                    review: `"Top-notch quality and great attention to detail. Worth every penny!"`
                }
            ],

            shown: null
        };
    },
    computed: {
        restUser() {
            return this.userData.filter(user => user.name !== this.shown?.name);
        }
    },
    created() {
        this.shown = this.userData[0];
        this.shown.rateStars = `<i class="bi bi-star-fill"></i>`.repeat(Math.floor(this.shown.rating)) + `<i class="bi bi-star-half"></i>`.repeat(this.shown.rating % 1 ? 1 : 0)
    },
    methods: {
        changeShownUser(name) {
            this.shown = this.userData.find(user => user.name === name);
            this.shown.rateStars = `<i class="bi bi-star-fill"></i>`.repeat(Math.floor(this.shown.rating)) + `<i class="bi bi-star-half"></i>`.repeat(this.shown.rating % 1 ? 1 : 0)

        }
    }
};
</script>

<style scoped></style>
