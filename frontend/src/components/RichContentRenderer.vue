<template>
  <div
    class="rich-content"
    v-html="sanitizedContent"
  ></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  content: string
}

const props = defineProps<Props>()

// 简单的 XSS 过滤（生产环境建议使用 DOMPurify 等库）
const sanitizeHtml = (html: string): string => {
  return html
    .replace(/<script\b[^>]*>([\s\S]*?)<\/script>/gim, '')
    .replace(/<iframe\b[^>]*>([\s\S]*?)<\/iframe>/gim, '')
    .replace(/on\w+="[^"]*"/g, '')
}

const sanitizedContent = computed(() => {
  return sanitizeHtml(props.content || '')
})
</script>

<style scoped>
.rich-content {
  line-height: 1.8;
  color: #374151;
}

.rich-content :deep(h1) {
  font-size: 2em;
  font-weight: bold;
  margin: 0.8em 0 0.4em 0;
}

.rich-content :deep(h2) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 0.8em 0 0.4em 0;
}

.rich-content :deep(h3) {
  font-size: 1.25em;
  font-weight: bold;
  margin: 0.8em 0 0.4em 0;
}

.rich-content :deep(p) {
  margin: 0.5em 0;
}

.rich-content :deep(ul),
.rich-content :deep(ol) {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.rich-content :deep(li) {
  margin: 0.25em 0;
}

.rich-content :deep(blockquote) {
  border-left: 4px solid #e5e7eb;
  padding-left: 1em;
  margin: 1em 0;
  color: #6b7280;
  font-style: italic;
}

.rich-content :deep(pre) {
  background-color: #1f2937;
  color: #f9fafb;
  padding: 1em;
  border-radius: 0.5em;
  overflow-x: auto;
  margin: 1em 0;
}

.rich-content :deep(code) {
  background-color: #f3f4f6;
  color: #1f2937;
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  font-family: monospace;
}

.rich-content :deep(pre code) {
  background-color: transparent;
  color: inherit;
  padding: 0;
}

.rich-content :deep(a) {
  color: #3b82f6;
  text-decoration: underline;
}

.rich-content :deep(a:hover) {
  color: #1d4ed8;
}

.rich-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.5em;
  margin: 1em 0;
}

.rich-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}

.rich-content :deep(th),
.rich-content :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.5em;
  text-align: left;
}

.rich-content :deep(th) {
  background-color: #f9fafb;
  font-weight: bold;
}
</style>
