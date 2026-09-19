<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { delJSON, getJSON, postJSON } from '../api'
const route = useRoute()
const router = useRouter()
const rec = ref(null)
const missing = ref(false)
const trial = ref(null)
const load = async () => {
  rec.value = null; trial.value = null; missing.value = false
  try { rec.value = await getJSON(`/api/history/${route.params.id}`) }
  catch { missing.value = true }
}
onMounted(load)
watch(() => route.params.id, load)
// 只读再试算：走当前图重算（persist:false），不写回本记录
const retrial = async () => {
  trial.value = await postJSON('/api/quote', { start: rec.value.start, end: rec.value.end, persist: false })
}
const remove = async () => {
  await delJSON(`/api/history/${route.params.id}`)
  router.push('/history')
}
</script>
<template>
  <div class="page">
    <p v-if="missing" class="muted">记录不存在或已删除</p>
    <template v-if="rec">
      <h1>记录 #{{ rec.id }}</h1>
      <div class="panel">
        <h2>锁定快照</h2>
        <p class="muted">{{ rec.start }} → {{ rec.end }} · {{ rec.created_at }}</p>
        <p>锁定途经：{{ rec.path ? rec.path.join(' → ') : '—' }}</p>
        <p>站数 {{ rec.hops }} · 票价 <span class="hero-num">¥{{ rec.fare }}</span></p>
        <button @click="retrial">按当前图只读再试算</button>
        <button class="danger" @click="remove">删除记录</button>
      </div>
      <div v-if="trial" class="panel">
        <h2>当前图试算（只读）</h2>
        <template v-if="trial.reachable">
          <p>当前途经：{{ trial.path.join(' → ') }}</p>
          <p>站数 {{ trial.hops }} · 票价 ¥{{ trial.fare }}</p>
          <p class="muted">按当前图实时重算，与上方锁定快照互不影响，不会写回记录</p>
        </template>
        <p v-else class="muted">当前图不可达</p>
      </div>
    </template>
  </div>
</template>
