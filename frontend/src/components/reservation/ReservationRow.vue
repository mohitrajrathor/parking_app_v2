<template>
  <tr>
    <th scope="row">{{ reservation.id }}</th>
    <td class="text-capitalize">{{ reservation.parking?.name || 'Deleted' }}</td>
    <td v-if="reservation.slot">{{ reservation.slot.serial_id }}</td>
    <td v-else><span class="badge bg-danger-subtle text-danger">Deleted</span></td>
    <td>{{ formatDate(reservation.start_time) }}</td>
    <td>{{ formatDate(reservation.leave_time) }}</td>
    <td>{{ reservation.hours_used ? reservation.hours_used : '-' }}</td>
    <td>
      <span v-if="reservation.is_booked" class="badge bg-success">Active</span>
      <span v-else class="badge bg-secondary">Completed</span>
    </td>
    <td>
      <ul class="list-unstyled mb-0">
        <li v-for="charge in reservation.charges" :key="charge.id">
          <span class="badge bg-primary-subtle text-primary me-1">{{ capitalize(charge.pay_for) }}</span>
          ₹{{ charge.amount }}
          <span class="text-muted small ms-1">({{ formatDate(charge.paid_at) }})</span>
        </li>
      </ul>
    </td>
    <td>
      <span v-if="reservation.review">
        <span class="badge bg-warning text-dark me-1">{{ reservation.review.rating }}★</span>
        <span class="text-muted small">{{ reservation.review.feedback }}</span>
      </span>
      <span v-else class="text-muted small">No review</span>
    </td>
    <td>{{ reservation.user.name }}</td>
    <td>
      <router-link
        :to="`/profile?user_id=${reservation.user.id}`"
        class="btn btn-sm btn-primary"
      >
        View
      </router-link>
    </td>
  </tr>
</template>

<script>
export default {
  name: "ReservationRow",
  props: {
    reservation: Object
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '-';
      const d = new Date(dateStr);
      if (isNaN(d)) return dateStr;
      return d.toLocaleString('en-IN', {
        year: '2-digit', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', hour12: true
      });
    },
    capitalize(str) {
      if (!str) return '';
      return str.charAt(0).toUpperCase() + str.slice(1);
    }
  }
};
</script>
