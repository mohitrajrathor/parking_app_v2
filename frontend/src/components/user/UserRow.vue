<template>
  <tr>
    <th scope="row">{{ user.id }}</th>
    <td>{{ user.name }}</td>
    <td>{{ user.email }}</td>
    <td>{{ user.phone }}</td>
    <td>{{ user.profession }}</td>
    <td>{{ user.address }}</td>
    <td>{{ user.pincode }}</td>
    <td>{{ user.dob }}</td>
    <td>{{ user.join_time }}</td>
    <td>{{ user.total_bookings }}</td>
    <td>{{ user.total_reviews }}</td>
    <td>
      <span class="badge" :class="user.email_confirmed ? 'bg-success' : 'bg-secondary'">
        {{ user.email_confirmed ? 'Yes' : 'No' }}
      </span>
    </td>
    <td>{{ user.active_bookings }}</td>
    <td>{{ user.total_bookings }}</td>
    <td>{{ user.total_reviews }}</td>
  </tr>
</template>

<script>
export default {
  name: "UserRow",
  props: {
    user: Object
  }
};
</script> 