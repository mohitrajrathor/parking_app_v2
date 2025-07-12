<template>
    <div id="Stats" class="m-4">
        <div class="p-4 bg-light rounded-4">
            <div class="row px-4 column-gap-4 row-gap-4">
                <template v-for="(item, idx) in statItems" :key="item.key">
                    <div
                        class="col p-3 rounded-4 stat-card d-flex flex-column align-items-center justify-content-center mb-3"
                        :class="item.bgClass"
                        style="min-width: 200px; min-height: 140px;"
                    >
                        <div class="stat-icon mb-2">
                            <i :class="item.icon"></i>
                        </div>
                        <h4 class="fw-medium text-white">{{ item.label }}</h4>
                        <h1 class="fw-bold text-white text-center">
                            {{ stats[item.key] }}
                        </h1>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>
<script>
import api from '../api';

export default {
    name: "Stats",
    data() {
        return {
            loading: false,
            stats: {
                total_parkings: 0,
                total_slots: 0,
                occupied_slots: 0,
                total_users: 0,
            },
            statItems: [
                {
                    key: "total_parkings",
                    label: "Total Parkings",
                    bgClass: "bg-primary shadow stat-card-hover",
                    icon: "bi bi-car-front-fill fs-1"
                },
                {
                    key: "total_slots",
                    label: "Total Slots",
                    bgClass: "bg-success shadow stat-card-hover",
                    icon: "bi bi-grid-3x3-gap-fill fs-1"
                },
                {
                    key: "occupied_slots",
                    label: "Occupied Slots",
                    bgClass: "bg-warning shadow stat-card-hover",
                    icon: "bi bi-cone-striped fs-1"
                },
                {
                    key: "total_users",
                    label: "Total Users",
                    bgClass: "bg-info shadow stat-card-hover",
                    icon: "bi bi-people-fill fs-1"
                }
            ]
        }
    },
    mounted() {
        this.fetchStats();
    },
    methods: {
        async fetchStats() {
            this.loading = true;
            try {
                const response = await api.get("/api_v1/analytics/quick_stats");
                this.stats = response.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>
<style scoped>
.stat-card {
    transition: transform 0.15s, box-shadow 0.15s;
    cursor: pointer;
}
.stat-card-hover:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 8px 32px rgba(0,0,0,0.18);
    opacity: 0.95;
}
.stat-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2rem;
    color: #fff;
    background: rgba(0,0,0,0.10);
    border-radius: 50%;
}
</style>