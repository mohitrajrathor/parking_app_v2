<template>
	<tr>
		<th scope="row">{{ parking.id }}</th>
		<td>
			<span v-if="mode === 'edit'">
				<input type="text" class="form-control" v-model="updateData.name" />
			</span>
			<span v-else class=" text-capitalize">{{ parking.name }}</span>
		</td>
		<td>
			<span v-if="mode === 'edit'">
				<input type="text" class="form-control" v-model="updateData.address" />
			</span>
			<span v-else>{{ parking.address }}</span>
		</td>
		<td>
			<span v-if="mode === 'edit'">
				<input type="text" class="form-control" v-model="updateData.pincode" />
			</span>
			<span v-else>{{ parking.pincode }}</span>
		</td>
		<td>
			<span v-if="mode === 'edit'">
				<input type="text" class="form-control" v-model="updateData.phone" />
			</span>
			<span v-else>{{ parking.phone }}</span>
		</td>
		<td>
			<span v-if="mode === 'edit'">
				<input type="number" class="form-control" v-model="updateData.booking_fee" />
			</span>
			<span v-else>{{ parking.booking_fee }}</span>
		</td>
		<td>
			<span v-if="mode === 'edit'">
				<input type="number" class="form-control" v-model="updateData.hourly_fee" />
			</span>
			<span v-else>{{ parking.hourly_fee }}</span>
		</td>
		<td>
			<span v-if="mode === 'edit'">
				<input type="number" class="form-control" v-model="updateData.slots_num" />
			</span>
			<span v-else>{{ parking.slots_num }}</span>
		</td>
		<td>
			{{ parking.booked }}
		</td>
		<td>
			{{ parking.reviews_count }}
		</td>

		<td>
			<span>
				<button v-if="mode === 'normal'" @click="redirectToParking(parking.id)"
					class="me-1 btn btn-sm btn-primary rounded-pill"><i class="bi bi-box-arrow-up-right"></i></button>
				<button v-if="mode === 'normal'" @click="mode = 'edit'"
					class="me-1 btn btn-sm rounded-pill btn-success"><i class="bi bi-pencil-square"></i></button>
				<button v-if="mode === 'edit'" @click="updateParking"
					class="me-1 btn btn-sm rounded-pill btn-success"><i class="bi bi-check-lg"></i></button>

				<button v-if="mode === 'edit'" @click="mode = 'normal'"
					class="me-1 btn btn-sm rounded-pill btn-danger"><i class="bi bi-x-lg"></i></button>

				<button v-if="mode === 'normal'" @click="deleteParking"
					class="me-1 btn btn-sm rounded-pill btn-danger"><i class="bi bi-trash3-fill"></i></button>
			</span>
		</td>
	</tr>
</template>

<script>
import api from "../api";


export default {
	name: "ParkingRow",
	props: {
		parking: Object
	},
	data() {
		return {
			mode: "normal",
			isLoading: false,
			updateData: { ...this.parking },
		}
	},
	computed: {

		newParking() {
			const rawDate = new Date(this.parking.created_at);
			if (isNaN(rawDate)) return false;

			const now = new Date();
			const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

			return rawDate >= sevenDaysAgo && rawDate <= now;
		}
	},

	inject: ["notify"],


	methods: {

		redirectToParking(id) {
			try {
				this.$router.push(`/parking/${id}`)
			} catch (err) {
				this.notify({
					message: "Can't view parking right now !",
					title: "Error",
					icon: "https://cdn-icons-png.flaticon.com/512/1680/1680012.png"
				})

				console.error(err);
			}
		},

		async updateParking() {
			try {
				this.isLoading = true;

				const { booked, slots, reviews_count, reviews, ...toUpdate } = this.updateData;

				const response = await api.put("/api_v1/parking", toUpdate);


				const data = await response.data;

				console.log(data);

				this.notify({
					message: data.message
				});

				this.$store.dispatch("parking/fetchParkings");


			} catch (err) {

				console.error(err);


			} finally {
				this.isLoading = false;
				this.mode = 'normal';
			}
		},

		async deleteParking() {
			try {

				if (confirm("Are you sure deleting this parking?")) {
					const response = await api.delete(`/api_v1/parking?id=${this.parking.id}`);

					this.$store.dispatch("parking/fetchParkings");

					this.notify({
						message: "Parking Deleted successfully!"
					});
				}
			} catch (err) {
				const data = await err.response.data;
				this.notify({
						message: data?.message || "Can not delete parking!",
						title: "Unable to Delete",
						icon: "https://cdn-icons-png.flaticon.com/512/190/190406.png",
						duration: 5000,
					});

					console.error(err);
			} finally {
				this.isLoading = false;
				this.mode = 'normal';
			}
		}
	}
};
</script>
