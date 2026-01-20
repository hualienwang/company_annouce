<template>
  <div class="rich-editor-container">
    <QuillEditor
      v-model="content"
      :content="content"
      content-type="html"
      :toolbar="toolbar"
      theme="snow"
      :placeholder="placeholder"
      @update:modelValue="onUpdate"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

interface Props {
  modelValue: string
  placeholder?: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请输入内容...',
})

const emit = defineEmits<Emits>()

const content = ref(props.modelValue)

const toolbar = [
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  ['bold', 'italic', 'underline', 'strike'],
  [{ list: 'ordered' }, { list: 'bullet' }],
  [{ align: [] }],
  ['blockquote', 'code-block'],
  [{ color: [] }, { background: [] }],
  ['link', 'image'],
  ['clean'],
]

const onUpdate = (value: string) => {
  content.value = value
  emit('update:modelValue', value)
}
</script>

<style scoped>
.rich-editor-container {
  background-color: white;
}

.rich-editor-container :deep(.ql-editor) {
  min-height: 200px;
  font-size: 16px;
}

.rich-editor-container :deep(.ql-toolbar) {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.rich-editor-container :deep(.ql-container) {
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}
</style>
