<template>
  <div class="rich-editor">
    <!-- 工具栏 -->
    <div class="re-toolbar">
      <button type="button" @click="exec('undo')" title="撤销"><i class="bi bi-arrow-counterclockwise"></i></button>
      <button type="button" @click="exec('redo')" title="重做"><i class="bi bi-arrow-clockwise"></i></button>
      <span class="re-divider"></span>
      <button type="button" @click="exec('bold')" title="加粗" :class="{ active: activeFormats.bold }"><i class="bi bi-type-bold"></i></button>
      <button type="button" @click="exec('italic')" title="斜体" :class="{ active: activeFormats.italic }"><i class="bi bi-type-italic"></i></button>
      <span class="re-divider"></span>
      <button type="button" @click="exec('insertUnorderedList')" title="无序列表"><i class="bi bi-list-ul"></i></button>
      <button type="button" @click="exec('insertOrderedList')" title="有序列表"><i class="bi bi-list-ol"></i></button>
      <button type="button" @click="exec('outdent')" title="减少缩进"><i class="bi bi-text-indent-left"></i></button>
      <button type="button" @click="exec('indent')" title="增加缩进"><i class="bi bi-text-indent-right"></i></button>
      <span class="re-divider"></span>
      <button type="button" @click="insertLink" title="链接"><i class="bi bi-link-45deg"></i></button>
      <button type="button" @click="exec('removeFormat')" title="清除格式"><i class="bi bi-eraser"></i></button>
    </div>
    <!-- 编辑区 -->
    <div
      ref="editorRef"
      class="re-content"
      contenteditable="true"
      :data-placeholder="placeholder"
      @input="onInput"
      @keydown="onKeydown"
      @focus="onFocus"
      @blur="onBlur"
      @mouseup="updateFormats"
      @keyup="updateFormats"
    ></div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '请输入内容...' }
})

const emit = defineEmits(['update:modelValue'])

const editorRef = ref(null)
const isFocused = ref(false)
const isInternalUpdate = ref(false)

const activeFormats = ref({
  bold: false,
  italic: false
})

function exec(command, value = null) {
  editorRef.value?.focus()
  document.execCommand(command, false, value)
  syncValue()
  updateFormats()
}

function insertLink() {
  const url = prompt('请输入链接地址：', 'https://')
  if (url) {
    exec('createLink', url)
  }
}

function updateFormats() {
  activeFormats.value.bold = document.queryCommandState('bold')
  activeFormats.value.italic = document.queryCommandState('italic')
}

function onInput() {
  syncValue()
}

function syncValue() {
  if (!editorRef.value) return
  isInternalUpdate.value = true
  emit('update:modelValue', editorRef.value.innerHTML)
  nextTick(() => {
    isInternalUpdate.value = false
  })
}

function onFocus() {
  isFocused.value = true
}

function onBlur() {
  isFocused.value = false
}

function onKeydown(e) {
  // Tab 键缩进
  if (e.key === 'Tab') {
    e.preventDefault()
    if (e.shiftKey) {
      exec('outdent')
    } else {
      exec('indent')
    }
  }
}

// 外部 modelValue 变更时同步到编辑器
watch(() => props.modelValue, (val) => {
  if (isInternalUpdate.value) return
  if (!editorRef.value) return
  if (editorRef.value.innerHTML !== val) {
    editorRef.value.innerHTML = val || ''
  }
})

onMounted(() => {
  if (editorRef.value && props.modelValue) {
    editorRef.value.innerHTML = props.modelValue
  }
})
</script>

<style scoped>
.rich-editor {
  @apply rounded-lg border border-brand-border overflow-hidden;
}
.re-toolbar {
  @apply flex items-center gap-1 px-3 py-2 bg-brand-surface border-b border-brand-border;
}
.re-toolbar button {
  @apply w-7 h-7 rounded flex items-center justify-center text-brand-muted 
         hover:bg-brand-bg hover:text-brand-text transition text-sm;
}
.re-toolbar button.active {
  @apply bg-violet-500/20 text-violet-400;
}
.re-divider {
  @apply w-px h-4 bg-brand-border mx-1;
}
.re-content {
  @apply w-full min-h-32 px-3 py-3 bg-brand-bg text-sm text-brand-text focus:outline-none;
  line-height: 1.6;
  overflow-y: auto;
  max-height: 300px;
}
.re-content:empty::before {
  content: attr(data-placeholder);
  @apply text-slate-500 pointer-events-none;
}
.re-content :deep(ul) {
  @apply list-disc pl-5 my-1;
}
.re-content :deep(ol) {
  @apply list-decimal pl-5 my-1;
}
.re-content :deep(a) {
  @apply text-violet-400 underline;
}
.re-content :deep(b), .re-content :deep(strong) {
  @apply font-bold;
}
.re-content :deep(i), .re-content :deep(em) {
  @apply italic;
}
.re-content :deep(li) {
  @apply my-0.5;
}
</style>
