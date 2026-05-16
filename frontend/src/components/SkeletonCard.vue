<template>
  <div class="skeleton-card" :class="{ 'skeleton-dark': isDark }">
    <div class="skeleton-header">
      <div class="skeleton-block skeleton-title" />
      <div class="skeleton-block skeleton-tag" />
    </div>
    <div class="skeleton-body">
      <div v-for="n in lines" :key="n" class="skeleton-block skeleton-line" :class="{ short: n === lines }" />
      <div class="skeleton-block skeleton-btn" />
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'SkeletonCard',
  props: {
    lines: { type: Number, default: 4 }
  },
  setup() {
    const isDark = computed(() => document.documentElement.classList.contains('dark-mode'))
    return { isDark }
  }
}
</script>

<style scoped>
.skeleton-card {
  padding: 20px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.skeleton-card.skeleton-dark {
  background: rgba(30, 30, 50, 0.85);
  border-color: rgba(255, 255, 255, 0.08);
}

.skeleton-header {
  margin-bottom: 16px;
}

.skeleton-block {
  background: linear-gradient(90deg,
    rgba(200, 200, 210, 0.2) 25%,
    rgba(200, 200, 210, 0.4) 50%,
    rgba(200, 200, 210, 0.2) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease infinite;
  border-radius: 8px;
}

.skeleton-dark .skeleton-block {
  background: linear-gradient(90deg,
    rgba(100, 100, 130, 0.15) 25%,
    rgba(100, 100, 130, 0.3) 50%,
    rgba(100, 100, 130, 0.15) 75%
  );
  background-size: 200% 100%;
}

.skeleton-title {
  height: 20px;
  width: 70%;
  margin-bottom: 10px;
}

.skeleton-tag {
  height: 16px;
  width: 40%;
}

.skeleton-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-line {
  height: 14px;
  width: 100%;
}

.skeleton-line.short {
  width: 60%;
}

.skeleton-btn {
  height: 36px;
  width: 100px;
  margin-top: 8px;
  border-radius: 18px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
