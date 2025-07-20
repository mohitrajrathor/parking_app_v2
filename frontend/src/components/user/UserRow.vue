<template>
  <tr>
    <th scope="row">{{ user.id }}</th>
    <td>{{ user.name }}</td>
    <td>{{ user.email }}</td>
    <td>{{ user.profession }}</td>
    <td>{{ user.dob }}</td>
    <td>{{ formatJoinTime(user.join_time) }}</td>
    <td>{{ user.total_bookings }}</td>
    <td>{{ user.total_reviews }}</td>
    <td>
      <span class="badge" :class="user.email_confirmed ? 'bg-success' : 'bg-secondary'">
        {{ user.email_confirmed ? 'Yes' : 'No' }}
      </span>
    </td>
    <td>{{ user.active_bookings }}</td>
    <td>{{ user.total_bookings }}</td>
    <td>
      <router-link
        :to="`/admin/user-profile?user_id=${user.id}`"
        class="btn btn-sm btn-primary"
      >
        View
      </router-link>
    </td>
  </tr>
</template>

<script>
export default {
  name: "UserRow",
  props: {
    user: Object
  },
  methods: {
    formatJoinTime(joinTime) {
      if (!joinTime) return '';
      const date = new Date(joinTime);
      return date.toLocaleDateString();
    }
  }
};
</script> 