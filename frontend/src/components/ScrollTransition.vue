<template>
  <div ref="section" :class="['scroll-transition', { 'in-view': inView }]">
    <slot />
  </div>
</template>

<script>
export default {
  name: 'ScrollTransition',
  data() {
    return {
      inView: false
    }
  },
  mounted() {
    const observer = new IntersectionObserver(
      ([entry]) => {
        this.inView = entry.isIntersecting;
      },
      { threshold: 0.15 }
    );
    observer.observe(this.$refs.section);
  }
}
</script>

<style scoped>
.scroll-transition {
  opacity: 0;
  transform: translateY(60px) scale(0.98);
  transition: opacity 0.8s cubic-bezier(.77,0,.18,1), transform 0.8s cubic-bezier(.77,0,.18,1);
  will-change: opacity, transform;
}
.scroll-transition.in-view {
  opacity: 1;
  transform: translateY(0) scale(1);
}
</style>
