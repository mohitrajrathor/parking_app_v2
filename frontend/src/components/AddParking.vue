<template>
	<div id="addParking" class="mb-5">
		<div class="card card-custom rounded-5 p-4 p-md-5 w-100">
			<h2 class="card-title text-center mb-4 mb-md-5 fw-bold text-dark">
				Parking Spot Details
			</h2>
			<form @submit.prevent="submitForm">
				<!-- Name Input -->
				<div class="mb-3">
					<label for="name" class="form-label text-muted">Parking Name</label>
					<input v-model="parking.name" type="text" class="form-control" id="name"
						placeholder="e.g., City Parking Lot A" required />
				</div>

				<!-- Address Input -->
				<div class="mb-3">
					<label for="address" class="form-label text-muted">Address</label>
					<input v-model="parking.address" type="text" class="form-control" id="address"
						placeholder="e.g., 123 Main St, Anytown" required />
				</div>

				<div class="row g-3 mb-3">



				</div>

				<div class="row g-4 mb-4">
					<!-- Latitude Input -->
					<div class="col-md-4">

						<!-- Pincode Input -->
						<div class="row">
							<label for="pincode" class="form-label text-muted">Pincode</label>
							<input v-model="parking.pincode" type="text" class="form-control" id="pincode"
								placeholder="e.g., 123456" required />
						</div>


						<!-- Phone Input -->
						<div class="row">
							<label for="phone" class="form-label text-muted">Phone Number</label>
							<input v-model="parking.phone" type="tel" class="form-control" id="phone"
								placeholder="e.g., 9876543210" required />
						</div>

						<div class="row">
							<label for="lat" class="form-label text-muted">Latitude</label>
							<input v-model="parking.lat" type="number" class="form-control" id="lat"
								placeholder="e.g., 34.0522" step="any" readonly />
						</div>

						<!-- Longitude Input -->
						<div class="row">
							<label for="long" class="form-label text-muted">Longitude</label>
							<input v-model="parking.long" type="number" class="form-control" id="long"
								placeholder="e.g., -118.2437" step="any" readonly />
						</div>


						<!-- Fee Input -->
						<div class="row">
							<label for="fee" class="form-label text-muted">Booking Fee</label>
							<input v-model="parking.booking_fee" type="number" class="form-control" id="fee"
								placeholder="e.g., 50" min="0" required />
						</div>

						<div class="row">
							<label for="fee" class="form-label text-muted">Parking Fee (per hour)</label>
							<input v-model="parking.hourly_fee" type="number" class="form-control" id="fee"
								placeholder="e.g., 50" min="0" required />
						</div>

						<!-- Number of Slots Input -->
						<div class="row">
							<label for="slots_num" class="form-label text-muted">Number of Slots</label>
							<input v-model="parking.slots_num" type="number" class="form-control" id="slots_num"
								placeholder="e.g., 100" min="10" max="200" required />
						</div>
					</div>

					<div class="col-md-8 g-3 mt-4">
						<h6 class="text-muted">Choose on map</h6>
						<LeafletMap />
					</div>
				</div>



				<div class="row g-3 mb-4">

				</div>

				<!-- Submit Button -->
				<div class="d-grid">
					<button type="submit" :disabled="isLoadling" class="btn btn-primary btn-lg">
						<span v-if="!isLoadling">
							Add Parking Spot
						</span>
						<span v-else>
							<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
							adding data...
						</span>
					</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import LeafletMap from './LeafletMap.vue';
import api from '../api';



export default {
	name: "AddParking",
	components: {
		LeafletMap,
	},
	data() {
		return {
			parking: {
				name: "",
				address: "",
				pincode: "",
				hourly_fee: "",
				booking_fee: "",
				phone: "",
				lat: null,
				long: null,
				slots_num: "",
			},
			isLoadling: false,
		};
	},

	inject: ["notify"],

	computed: {
		choosenPos() {
			return this.$store.getters.getChoosenPos;
		}
	},
	watch: {
		choosenPos: {
			immediate: true,
			handler(newVal) {
				if (newVal && newVal.lat && newVal.long) {
					this.parking.lat = newVal.lat;
					this.parking.long = newVal.long;
				}
			}
		}
	},
	methods: {
		async submitForm() {
			try {
				const { hourly_fee, booking_fee, name, address, lat, long, pincode, phone, slots_num } = this.parking;

				if (!hourly_fee || !booking_fee || !name || !address || !lat || !long || !pincode || !phone || !slots_num) {
					this.notify("All fields are required!");
					throw new Error("All fields are required!");
				}

				this.isLoading = true; 

				const response = await api.post(
					"/api_v1/parking",
					this.parking,
					{
						headers: {
							"Content-Type": "application/json"
						}
					}
				);

				const data = await response.data;
				this.notify({
					message: data.message
				});

				this.parking = {
					name: "",
					address: "",
					pincode: "",
					hourly_fee: "",
					booking_fee: "",
					phone: "",
					lat: null,
					long: null,
					slots_num: "",
				};

			} catch (err) {
				if (err.response && err.response.status === 409) {
					// Only notify on 409 Conflict

					console.error(err.response.data?.message);

					this.notify(
						{ message: err.response.data?.message || "Resource already exists", title: "Conflict" }
					);
				} else {
					console.error("Unhandled error:", err);
				}
			} finally {
				this.isLoading = false;


				
			}
		}

	}
};
</script>

<style></style>
