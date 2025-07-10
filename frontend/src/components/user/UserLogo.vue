<template>
  <div
    :class="['d-flex', 'align-items-center', 'justify-content-center', 'rounded-circle', 'fw-bold', 'text-white', customClass]"
    :style="logoStyle"
    :title="name"
  >
    {{ initials }}
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  name: {
    type: String,
    default: 'User'
  },
  size: {
    type: [Number, String],
    default: 48 // px
  },
  customClass: {
    type: String,
    default: ''
  }
});

// Generate initials from first two words
const initials = computed(() => {
  if (!props.name) return '';
  const words = props.name.trim().split(' ').filter(Boolean);
  return words.slice(0, 2).map(w => w[0]?.toUpperCase() || '').join('');
});

// Generate a random color based on the name (so it's consistent)
function stringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  const color = `hsl(${hash % 360}, 70%, 55%)`;
  return color;
}

const logoStyle = computed(() => ({
  width: typeof props.size === 'number' ? `${props.size}px` : props.size,
  height: typeof props.size === 'number' ? `${props.size}px` : props.size,
  background: stringToColor(props.name || 'User'),
  border: '2px solid #fff',
  fontSize: `calc(${typeof props.size === 'number' ? props.size : parseInt(props.size)}px / 2)`,
  userSelect: 'none'
}));
</script>